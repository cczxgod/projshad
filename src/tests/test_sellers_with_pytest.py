import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books

@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "Name Test", "last_name": "Test Last Name", "email": "dsfasdfa@mail.ru","books": [], "password": "sasdadasd1231sada"}
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()
    seller_id = response.json()["id"]

    assert result_data == {
       "first_name": "Name Test",
        "last_name": "Test Last Name", 
        "email": "dsfasdfa@mail.ru",
        "books": [], 
        "id": seller_id
    }


@pytest.mark.asyncio
async def test_get_sells(db_session, async_client):
    seller = books.Seller(first_name="First", last_name="Last", email="slasdada", password="asdadadada")
    seller_2 = books.Seller(first_name="First2", last_name="Last2", email="slasd2ada", password="as2dadadada")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    assert response.json() == {
        "sellers": [
            {"first_name": "First2", "last_name": "Last2", "email":"slasd2ada", "id": seller_2.id, "books":[]},
            {"first_name": "First", "last_name": "Last", "email":"slasdada", "id": seller.id, "books":[]},
        ]
    }


@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller = books.Seller(first_name="First", last_name="Last", email="slasdada", password="asdadadada", books=[])
    seller_2 = books.Seller(first_name="First2", last_name="Last2", email="slasd2ada", password="as2dadadada", books=[])

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK
    print(response)
    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "first_name": "First", 
        "last_name": "Last", 
        "email":"slasdada", 
        "id": seller.id, 
        "books": []
    }


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = books.Seller(first_name="First", last_name="Last", email="slasdada", password="asdadadada")

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(books.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = books.Seller(first_name="First", last_name="Last", email="slasdada", password="asdadadada", books=[])

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/sellers/{seller.id}",
        json={"first_name": "First2", "last_name": "Last2", "email":"slasd2ada", "id": seller.id, "books":[]},
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(books.Seller, seller.id)
    assert res.first_name == "First2"
    assert res.last_name == "Last2"
    assert res.email == "slasd2ada"
    assert res.books == []
    assert res.id == seller.id
