from telegram import (
    BotCommand
)

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

import handlers
from src.core.config import TELEGRAM_TOKEN

async def post_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("/start", "Начало | Начать заново"),
        BotCommand("/info", "Информация о профиле")
    ])


def run_bot() -> None:
    application = (
        ApplicationBuilder().token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", handlers.start_handle))
    application.add_handler(CallbackQueryHandler(handlers.general_menu_callback_handle,
                                                 pattern='^show_general_menu_handle'))

    application.add_handler(CallbackQueryHandler(handlers.general_menu_callback_handle, pattern='^show_profile'))
    application.add_handler(CallbackQueryHandler(handlers.general_menu_callback_handle, pattern='^get_vpn_settings'))
    application.add_handler(CallbackQueryHandler(handlers.general_menu_callback_handle, pattern='^check_payment'))
    application.add_handler(CallbackQueryHandler(handlers.general_menu_callback_handle, pattern='^create_payment_link'))

    # start the bot
    application.run_polling()


if __name__ == "__main__":
    run_bot()
