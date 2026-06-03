from fastapi import APIRouter

from app.api.routes.v1.newsletter_subscribers import router as newsletter_subscribers_router
from app.api.routes.v1.contact_submissions import router as contact_submissions_router
from app.api.routes.v1.stats import router as stats_router
from app.api.routes.v1.content import router as content_router
from app.api.routes.v1.users import router as users_router
from app.api.routes.v1.feedback import router as feedback_router

api_router = APIRouter()

api_router.include_router(newsletter_subscribers_router)
api_router.include_router(contact_submissions_router)
api_router.include_router(stats_router)
api_router.include_router(content_router)
api_router.include_router(users_router)
api_router.include_router(feedback_router)
