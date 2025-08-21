from aiogram import Router

from handlers.event_handlers import router as event_handlers_router
from handlers.commands import router as commands_router

router = Router()

router.include_routers(
    event_handlers_router, 
    commands_router
)
