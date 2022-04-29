import datetime
import os
import gspread

from telegram import Chat
from telegram.ext import CallbackContext

from common.api.collector.product_processor import ProductProcessor
from common.api.customer.customer import Customer
from common.helpers.enum import Marketplace
from engine.user.user import BotUser


def jon_send_stock(context: CallbackContext):
    gs = gspread.service_account(os.path.join(os.getcwd(), 'service_account.json'))
    tg_users: list[BotUser] = BotUser.get_all()

    for tg_user in tg_users:
        chat: Chat = context.bot.get_chat(chat_id=tg_user.telegram)
        try:
            connect_account: Customer = tg_user.market_customer
        except RuntimeError:
            continue

        result_table = gs.create(f"Отчёт по остаткам от {datetime.datetime.now().strftime('%d.%m.%Y')}"
                                 f" для {connect_account.username}")
        result_table.share(value=None, perm_type="anyone", role="writer")

        for marketplace in Marketplace:
            sheet = result_table.add_worksheet(title=marketplace.value, rows=1000, cols=5)
            products = ProductProcessor.get_product_from_marketplace(connect_account, marketplace)
            sheet.append_row(["Название товара", "Остаток"])
            sheet.append_rows([[str(product.title), str(product.get_stock(marketplace))] for product in products])

        chat.send_message(text=f"Привет! Я сгенерировал отчёт по остаткам товаров - {result_table.url}")
