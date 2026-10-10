# Handlers package
from aiogram import Router

from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.schools import router as schools_router
from handlers.schedule import router as schedule_router
from handlers.attendance import router as attendance_router
from handlers.qr import router as qr_router
from handlers.profile import router as profile_router
from handlers.workload import router as workload_router
from handlers.security import router as security_router
from handlers.notifications import router as notifications_router

def get_main_router() -> Router:
    """Combine all routers into a main router."""
    main_router = Router()
    main_router.include_router(start_router)
    main_router.include_router(registration_router)
    main_router.include_router(schools_router)
    main_router.include_router(schedule_router)
    main_router.include_router(attendance_router)
    main_router.include_router(qr_router)
    main_router.include_router(profile_router)
    main_router.include_router(workload_router)
    main_router.include_router(security_router)
    main_router.include_router(notifications_router)
    
    return main_router
