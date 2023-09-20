from fastapi import APIRouter

from src.api.routes.database_route import router as database_router
from src.api.routes.raw_data_route import router as raw_data_router
from src.api.routes.config_files_route import router as config_files_router
from src.api.routes.seed_db_route import router as seed_db_router
router = APIRouter()

router.include_router(database_router, prefix="/database")
router.include_router(config_files_router, prefix="/config_files")
router.include_router(raw_data_router, prefix="/raw_data")
router.include_router(seed_db_router, prefix="/seed_db")