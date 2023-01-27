from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.db.models import Shop, Category
from src.ordering_goods.schemas import ShopRead, ShopCreate, CategoryCreate, CategoryRead

router_shop = APIRouter(
    prefix="/shops",
    tags=["Shop"]
)


@router_shop.get("/", response_model=List[ShopRead])
async def get_shops(session: AsyncSession = Depends(get_async_session)):
    query = select(Shop)
    result = await session.execute(query)
    return result.all()


@router_shop.post("/")
async def add_shop(new_shop: ShopCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Shop).values(**new_shop.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": f"Shop {new_shop.name} created"}


router_category = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router_category.get("/", response_model=List[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    query = select(Category)
    result = await session.execute(query)
    return result.all()


@router_category.post("/")
async def add_category(new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    shops_id = new_category.dict().pop("shops_id", None)
    if shops_id:
        query = select(Shop).where(Shop.id in shops_id)
        shops = await session.execute(query)
        create_category = Category(**new_category.dict(), shops=shops)
    else:
        create_category = Category(**new_category.dict())
    await session.add(create_category)
    await session.commit()
    return {"status": f"Shop {new_category.name} created"}