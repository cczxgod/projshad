from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.models.books import Seller
from src.schemas import BaseSeller, NewSeller, ReturnedSeller, ReturnedAllSells

sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)  
async def create_sel(
    seller: NewSeller, session: DBSession
): 
    new_sel = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        email=seller.email,
        password=seller.password,
        books=seller.books
    )
    session.add(new_sel)
    await session.flush()

    return new_sel

@sellers_router.get("/", response_model=ReturnedAllSells)
async def get_all_sells(session: DBSession):
    query = select(Seller)
    res = await session.execute(query)
    sellers = res.unique().scalars().all()
    return {"sellers": sellers}

@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_sell(seller_id: int, session: DBSession):
    res = await session.get(Seller, seller_id)
    return res


@sellers_router.delete("/{seller_id}")
async def delete_sell(seller_id: int, session: DBSession):
    deleted_sell = await session.get(Seller, seller_id)
    ic(deleted_sell)  
    if deleted_sell:
        await session.delete(deleted_sell)

    return Response(status_code=status.HTTP_204_NO_CONTENT)  

@sellers_router.put("/{seller_id}")
async def update_sell(seller_id: int, new_data: BaseSeller, session: DBSession):
    if updated_sell := await session.get(Seller, seller_id):
        updated_sell.first_name=new_data.first_name
        updated_sell.last_name=new_data.last_name
        updated_sell.email=new_data.email

        await session.flush()

        return updated_sell

    return Response(status_code=status.HTTP_404_NOT_FOUND)
