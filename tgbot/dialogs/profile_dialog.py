from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from tgbot.handlers.private.plug import plug

from tgbot.handlers.private.profile import feedback, go_back, referal
from tgbot.misc.widgets.switch_current_chat import SwitchCurrentChat
from tgbot.services.database.models import User
from tgbot.states.profile_dialog import ProfileSG


async def info_getter(dialog_manager: DialogManager, **kwargs):
    user: User = dialog_manager.data.get('user')
    
    return {
        "tg_id": user.user_id,
        "points": user.points,
        "amount": user.amount,
        "purchases": user.purchases,
    }
    

async def referal_getter(dialog_manager: DialogManager, **kwargs):
    user: User = dialog_manager.data.get('user')
    
    return {
        "referals": len(user.referals),
        "link": f't.me/finshalm_bot?start={user.user_id}',
    }
    

dialog = Dialog(
    Window(
        Format('<b>Ваш ID:</b> <code>{tg_id}</code>\n'
               '<b>Внутренние баллы:</b> <code>{points}</code>\n\n'
               '🔎 Статистика\n'
               '├ Сумма покупок: <code>{amount}</code>₽\n'
               '└ Количество покупок: <code>{purchases}</code> шт.'),
        SwitchCurrentChat(Const('🛒 Каталог'), id="shop"),
        Button(Const("🌐 Рефералочка"), id="ref", on_click=referal),
        Button(Const("📨 Обратная связь"), id="fb", on_click=feedback),
        MessageInput(plug),
        state=ProfileSG.profile,
        getter=info_getter,
    ),
    
    Window(
        Format('Если вам нравится наш сервис, вы можете порекомендовать его своим друзьям,'
               'чтобы у нас была мотивация дальше радовать вас приятными ценами.\n\n'
               '<b>В качестве вознаграждения вы будете получать 10 баллов '
               'со всех приглашенных вами пользователей.</b>\n\n'
               '🔎 Всего приглашено вами: <code>{referals} чел.</code>\n'
               '🔗 Ссылка для приглашения — <code>{link}</code>'),
        Row(
            Button(Const("⬅️ Назад"), id="back2", on_click=go_back),
        ),
        state=ProfileSG.referal,
        getter=referal_getter
    ),
    
    Window(
        Const('Контакты:\n'
              'email: example@email.com\n'
              'telegram: @zshalm'),
        Row(
            Button(Const("⬅️ Назад"), id="back2", on_click=go_back),
        ),
        state=ProfileSG.feedback,
    ),
)


def setup(registry: DialogRegistry):
    registry.register(dialog)