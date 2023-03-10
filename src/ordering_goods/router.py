from typing import List

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, load_only

from src.auth.base_config import current_active_user
from src.database import get_async_session
from src.db.models import Shop, Category, User, ShopCategory
from src.ordering_goods.schemas import ShopRead, ShopCreate, CategoryCreate, CategoryRead
from src.ordering_goods.utils import create_categories_from_list

router_category = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@router_category.get("/all")  # , response_model=List[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    query = select(Category)
    result = await session.execute(query)
    return result.all()


@router_category.post("/")  # , response_model=CategoryRead)
async def add_category(new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    create_category = insert(Category).values(**new_category.dict())
    await session.execute(create_category)
    try:
        await session.commit()
        return {"status": f"Category {new_category.name} created"}
    except UniqueViolationError:
        raise UniqueViolationError.code


router_shop = APIRouter(
    prefix="/shop",
    tags=["Shop"]
)


@router_shop.get("/all")  # , response_model=List[ShopRead])
async def get_shops(session: AsyncSession = Depends(get_async_session)):
    query = select(Shop).options(selectinload(Shop.categories),
                                 load_only(Shop.name, Shop.state, Shop.url),
                                 )
    result = await session.execute(query)
    return result.all()


@router_shop.post("/", status_code=201)
async def add_shop(new_shop: ShopCreate,
                   session: AsyncSession = Depends(get_async_session)):
                   # user: User = Depends(current_active_user)):
    new_shop_dict = new_shop.dict()
    categories = new_shop_dict.pop('categories')
    await create_categories_from_list(session, categories)
    stmt_shop = insert(Shop).values(**new_shop_dict,
                                    # user_id=user.id,
                                    ).returning(Shop.id)
    result = await session.execute(stmt_shop)
    await session.commit()
    shop_id = result.scalar_one()
    for category in categories:
        stmt = insert(ShopCategory).values(shop_id=shop_id,
                                           category_id=category["id"])
        await session.execute(stmt)
    await session.commit()
    return {"status": f"Shop {new_shop.name} created"}
