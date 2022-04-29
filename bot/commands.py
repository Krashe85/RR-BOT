from telegram import Update
from telegram.ext import CallbackContext

from common.api.customer.customer import Customer
from common.models.customer import CustomerModel
from engine.user.inviter import InviteUserToClient
from engine.user.user import BotUser


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!'
    )


def create_invite(update: Update, context: CallbackContext) -> None:
    user = BotUser(update.effective_user.id)

    if not user.permissions.check_perm("invite.create"):
        update.message.reply_markdown_v2(text=f"У вас недостаточно прав")
        return

    if len(context.args) < 1:
        update.message.reply_markdown_v2(text="Неостаочоно аргументов _invite title_")
        return

    customer_username = context.args[0]
    try:
        customer = Customer(CustomerModel.get_from_title(customer_username))
    except RuntimeError:
        update.message.reply_markdown_v2(f"**Клиент не найден!**")
        return
    hash_invite = InviteUserToClient().create_invite(customer)

    update.message.reply_text(text=f"Успешно!"
                                   f"Для подключения пользователя он должен отправить сообщение /reg {hash_invite}",
                              reply_to_message_id=update.message.message_id)


def user_registrate(update: Update, context: CallbackContext) -> None:
    user = BotUser(update.effective_user.id)

    try:
        market_customer = user.market_customer
        update.message.reply_text(text=f"ОШИБКА!!Ваш аккаунт уже привязан к {market_customer.username}")
    except RuntimeError:
        pass

    if len(context.args) < 1:
        update.message.reply_text(text="Неостаочоно аргументов /reg <invite>")
        return

    invite = context.args[0]

    customer = InviteUserToClient().get_invite_customer_from_id(invite)
    user.market_customer = customer
    update.message.reply_text(text=f"Успешно!")
