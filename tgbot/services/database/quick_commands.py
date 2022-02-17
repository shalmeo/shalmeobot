from asyncio.log import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from tgbot.services.database.models import Items, User


async def delete_item(session: AsyncSession, item_id):
    try:
        await session.execute(delete(Items).where(Items.id==item_id))
        await session.commit()
        return True
    except Exception as err:
        logger.info(err)


async def add_referal(session: AsyncSession, ref_id: User, user: User):
    ref: User = await session.get(User, ref_id)
    
    if user.user_id not in ref.referals:
        ref.referals = list(ref.referals)
        ref.referals.append(user.user_id)
        ref.points += 10

    
    if not user.referal:
        user.referal = ref.user_id
    
    await session.commit()