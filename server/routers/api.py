from fastapi import APIRouter

from .transactions import router as transactions_router
from .models import router as models_router

router = APIRouter()


router.include_router(transactions_router)
router.include_router(models_router)