from app.db.session import engine
from app.db.base import Base

from app.models.page_section import PageSection
from app.models.page_section_media import PageSectionMedia
from app.models.nav_menu import NavMenu
from app.models.nav_menu_item import NavMenuItem
# from app.models.blog import Blog
from app.models.newsletter_subscribers import NewsletterSubscriber
from app.models.contact_requests import ContactRequest
from app.models.media_asset import MediaAsset
# from app.models.blog_category import BlogCategory
# from app.models.blog_post import BlogPost
# from app.models.blog_post_category import BlogPostCategory
from app.models.role import Role
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.feedback import Feedback
from app.models.sample_category import SampleCategory
from app.models.sample_industry import SampleIndustry
from app.models.sample import Sample
from app.models.sample_lead import SampleLead

Base.metadata.create_all(bind=engine)

print(
    "Tables created: roles, users, audit_logs, "
    "pages, page_sections, page_section_media, "
    "nav_menus, nav_menu_items, "
    "newsletter_subscribers, contact_requests, media_assets, "
    "feedbacks, sample_categories, sample_industries, "
    "samples, sample_leads"
)

