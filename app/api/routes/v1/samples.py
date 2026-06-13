from fastapi import APIRouter, Depends, HTTPException, status, Header, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, desc, asc
from typing import List, Optional
from datetime import datetime, timezone

from app.db.session import get_db
from app.models.user import User
from app.models.sample_category import SampleCategory
from app.models.sample_industry import SampleIndustry
from app.models.sample import Sample
from app.models.sample_lead import SampleLead
from app.schemas.sample import (
    CategoryCreate, CategoryOut,
    IndustryCreate, IndustryOut,
    SampleLeadCreate, SampleLeadOut,
    SampleCreate, SampleUpdate, SampleOut
)
from app.core.security import verify_token

import shutil
import uuid
from pathlib import Path

router = APIRouter(prefix="/samples", tags=["Samples"])

def get_current_admin(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token format")
    
    token = authorization.split(" ", 1)[1].strip()
    try:
        user_id = verify_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    
    return user

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    admin: User = Depends(get_current_admin)
):
    base_dir = Path(__file__).resolve().parents[3]
    upload_dir = base_dir / "app" / "public" / "uploads" / "samples"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    ext = Path(file.filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = upload_dir / unique_name
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")
    finally:
        await file.close()
        
    public_url = f"/api/uploads/samples/{unique_name}"
    return {"url": public_url, "filename": file.filename, "saved_name": unique_name}


# ──────────────────────────────────────────────────────────────────────────────
# CATEGORIES ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    stmt = select(SampleCategory).order_by(SampleCategory.name.asc())
    return db.execute(stmt).scalars().all()

@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    slug = payload.slug.strip().lower()
    exists = db.execute(select(SampleCategory).where(SampleCategory.slug == slug)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Category slug already exists")
        
    category = SampleCategory(
        name=payload.name.strip(),
        slug=slug
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    payload: CategoryCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    category = db.get(SampleCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    slug = payload.slug.strip().lower()
    exists = db.execute(
        select(SampleCategory).where(SampleCategory.slug == slug, SampleCategory.id != category_id)
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Category slug already exists")
        
    category.name = payload.name.strip()
    category.slug = slug
    db.commit()
    db.refresh(category)
    return category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    category = db.get(SampleCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return

# ──────────────────────────────────────────────────────────────────────────────
# INDUSTRIES ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/industries", response_model=List[IndustryOut])
def get_industries(db: Session = Depends(get_db)):
    stmt = select(SampleIndustry).order_by(SampleIndustry.name.asc())
    return db.execute(stmt).scalars().all()

@router.post("/industries", response_model=IndustryOut, status_code=status.HTTP_201_CREATED)
def create_industry(payload: IndustryCreate, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    slug = payload.slug.strip().lower()
    exists = db.execute(select(SampleIndustry).where(SampleIndustry.slug == slug)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Industry slug already exists")
        
    industry = SampleIndustry(
        name=payload.name.strip(),
        slug=slug
    )
    db.add(industry)
    db.commit()
    db.refresh(industry)
    return industry

@router.put("/industries/{industry_id}", response_model=IndustryOut)
def update_industry(
    industry_id: int,
    payload: IndustryCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    industry = db.get(SampleIndustry, industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
        
    slug = payload.slug.strip().lower()
    exists = db.execute(
        select(SampleIndustry).where(SampleIndustry.slug == slug, SampleIndustry.id != industry_id)
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Industry slug already exists")
        
    industry.name = payload.name.strip()
    industry.slug = slug
    db.commit()
    db.refresh(industry)
    return industry

@router.delete("/industries/{industry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_industry(
    industry_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    industry = db.get(SampleIndustry, industry_id)
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    db.delete(industry)
    db.commit()
    return

# ──────────────────────────────────────────────────────────────────────────────
# SAMPLE LEADS ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/leads", response_model=List[SampleLeadOut])
def get_leads(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    stmt = select(SampleLead).order_by(SampleLead.created_at.desc())
    return db.execute(stmt).scalars().all()

@router.post("/leads", response_model=SampleLeadOut, status_code=status.HTTP_201_CREATED)
def create_lead(payload: SampleLeadCreate, db: Session = Depends(get_db)):
    lead = SampleLead(
        sample_id=payload.sample_id,
        name=payload.name.strip(),
        company=payload.company.strip() if payload.company else None,
        email=str(payload.email).strip().lower(),
        phone=payload.phone.strip() if payload.phone else None,
        service_required=payload.service_required.strip() if payload.service_required else None,
        message=payload.message.strip()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

# ──────────────────────────────────────────────────────────────────────────────
# SAMPLE CRUD ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

@router.get("", response_model=List[SampleOut])
def list_samples(
    category_slug: Optional[str] = Query(None),
    industry_slug: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("newest"), # newest, oldest, alphabetical
    include_private: bool = Query(False),
    db: Session = Depends(get_db)
):
    stmt = select(Sample).where(Sample.deleted_at.is_(None))
    
    # Visibility and Status filters
    if not include_private:
        stmt = stmt.where(Sample.visibility != "private")
        stmt = stmt.where(Sample.status == "published")
    elif status_filter:
        stmt = stmt.where(Sample.status == status_filter)
        
    # Category filter
    if category_slug:
        stmt = stmt.join(Sample.categories).where(SampleCategory.slug == category_slug)
        
    # Industry filter
    if industry_slug:
        stmt = stmt.join(Sample.industries).where(SampleIndustry.slug == industry_slug)
        
    # Search filter (title, short_desc, detailed_desc)
    if search:
        search_term = f"%{search.strip()}%"
        stmt = stmt.where(
            or_(
                Sample.title.ilike(search_term),
                Sample.short_description.ilike(search_term),
                Sample.detailed_description.ilike(search_term)
            )
        )
        
    # Sorting
    if sort == "oldest":
        stmt = stmt.order_by(Sample.created_at.asc())
    elif sort == "alphabetical":
        stmt = stmt.order_by(Sample.title.asc())
    else: # newest
        stmt = stmt.order_by(Sample.created_at.desc())
        
    return db.execute(stmt).scalars().unique().all()

@router.get("/stats/summary")
def get_stats_summary(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_samples = db.execute(select(func.count(Sample.id)).where(Sample.deleted_at.is_(None))).scalar() or 0
    total_views = db.execute(select(func.sum(Sample.views)).where(Sample.deleted_at.is_(None))).scalar() or 0
    total_downloads = db.execute(select(func.sum(Sample.downloads)).where(Sample.deleted_at.is_(None))).scalar() or 0
    total_leads = db.execute(select(func.count(SampleLead.id))).scalar() or 0
    
    most_viewed = db.execute(
        select(Sample).where(Sample.deleted_at.is_(None)).order_by(Sample.views.desc()).limit(5)
    ).scalars().all()
    
    most_downloaded = db.execute(
        select(Sample).where(Sample.deleted_at.is_(None)).order_by(Sample.downloads.desc()).limit(5)
    ).scalars().all()
    
    return {
        "total_samples": total_samples,
        "total_views": total_views,
        "total_downloads": total_downloads,
        "total_leads": total_leads,
        "most_viewed": [{"id": s.id, "title": s.title, "views": s.views} for s in most_viewed],
        "most_downloaded": [{"id": s.id, "title": s.title, "downloads": s.downloads} for s in most_downloaded]
    }

@router.get("/{id_or_slug}", response_model=SampleOut)
def get_sample(
    id_or_slug: str,
    password: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    stmt = select(Sample).where(Sample.deleted_at.is_(None))
    if id_or_slug.isdigit():
        stmt = stmt.where(Sample.id == int(id_or_slug))
    else:
        stmt = stmt.where(Sample.slug == id_or_slug)
        
    sample = db.execute(stmt).scalar_one_or_none()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
        
    # Visibility checks
    if sample.visibility == "password_protected":
        if not password or password != sample.password:
            raise HTTPException(
                status_code=403,
                detail="password_required"
            )
            
    # Auto-increment views
    sample.views += 1
    db.commit()
    db.refresh(sample)
    return sample

@router.post("", response_model=SampleOut, status_code=status.HTTP_201_CREATED)
def create_sample(
    payload: SampleCreate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    slug = payload.slug.strip().lower()
    exists = db.execute(select(Sample).where(Sample.slug == slug, Sample.deleted_at.is_(None))).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Sample slug already exists")
        
    # Resolve Categories
    categories = []
    if payload.category_ids:
        categories = db.execute(select(SampleCategory).where(SampleCategory.id.in_(payload.category_ids))).scalars().all()
        
    # Resolve Industries
    industries = []
    if payload.industry_ids:
        industries = db.execute(select(SampleIndustry).where(SampleIndustry.id.in_(payload.industry_ids))).scalars().all()
        
    sample = Sample(
        title=payload.title.strip(),
        slug=slug,
        short_description=payload.short_description.strip(),
        detailed_description=payload.detailed_description.strip(),
        featured_image=payload.featured_image,
        video_url=payload.video_url,
        status=payload.status,
        visibility=payload.visibility,
        password=payload.password,
        technologies=payload.technologies,
        project_highlights=payload.project_highlights,
        client_outcome=payload.client_outcome,
        tags=payload.tags,
        gallery_images=payload.gallery_images,
        before_after_images=payload.before_after_images,
        screenshots=payload.screenshots,
        download_files=payload.download_files,
        seo_title=payload.seo_title,
        seo_meta_description=payload.seo_meta_description,
        seo_meta_keywords=payload.seo_meta_keywords,
        seo_og_image=payload.seo_og_image,
        seo_canonical_url=payload.seo_canonical_url,
        categories=categories,
        industries=industries
    )
    
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample

@router.patch("/{sample_id}", response_model=SampleOut)
def update_sample(
    sample_id: int,
    payload: SampleUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    sample = db.execute(select(Sample).where(Sample.id == sample_id, Sample.deleted_at.is_(None))).scalar_one_or_none()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
        
    if payload.slug is not None:
        slug = payload.slug.strip().lower()
        exists = db.execute(select(Sample).where(Sample.slug == slug, Sample.id != sample_id, Sample.deleted_at.is_(None))).scalar_one_or_none()
        if exists:
            raise HTTPException(status_code=409, detail="Sample slug already exists")
        sample.slug = slug
        
    if payload.title is not None:
        sample.title = payload.title.strip()
    if payload.short_description is not None:
        sample.short_description = payload.short_description.strip()
    if payload.detailed_description is not None:
        sample.detailed_description = payload.detailed_description.strip()
    if payload.featured_image is not None:
        sample.featured_image = payload.featured_image
    if payload.video_url is not None:
        sample.video_url = payload.video_url
    if payload.status is not None:
        sample.status = payload.status
    if payload.visibility is not None:
        sample.visibility = payload.visibility
    if payload.password is not None:
        sample.password = payload.password
        
    if payload.technologies is not None:
        sample.technologies = payload.technologies
    if payload.project_highlights is not None:
        sample.project_highlights = payload.project_highlights
    if payload.client_outcome is not None:
        sample.client_outcome = payload.client_outcome
    if payload.tags is not None:
        sample.tags = payload.tags
    if payload.gallery_images is not None:
        sample.gallery_images = payload.gallery_images
    if payload.before_after_images is not None:
        sample.before_after_images = payload.before_after_images
    if payload.screenshots is not None:
        sample.screenshots = payload.screenshots
    if payload.download_files is not None:
        sample.download_files = payload.download_files
        
    if payload.seo_title is not None:
        sample.seo_title = payload.seo_title
    if payload.seo_meta_description is not None:
        sample.seo_meta_description = payload.seo_meta_description
    if payload.seo_meta_keywords is not None:
        sample.seo_meta_keywords = payload.seo_meta_keywords
    if payload.seo_og_image is not None:
        sample.seo_og_image = payload.seo_og_image
    if payload.seo_canonical_url is not None:
        sample.seo_canonical_url = payload.seo_canonical_url

    # Resolve/Update Categories
    if payload.category_ids is not None:
        categories = db.execute(select(SampleCategory).where(SampleCategory.id.in_(payload.category_ids))).scalars().all()
        sample.categories = categories
        
    # Resolve/Update Industries
    if payload.industry_ids is not None:
        industries = db.execute(select(SampleIndustry).where(SampleIndustry.id.in_(payload.industry_ids))).scalars().all()
        sample.industries = industries

    db.commit()
    db.refresh(sample)
    return sample

@router.delete("/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(
    sample_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    sample = db.execute(select(Sample).where(Sample.id == sample_id, Sample.deleted_at.is_(None))).scalar_one_or_none()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
        
    # Soft delete preferred
    sample.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return

@router.post("/{sample_id}/view", status_code=status.HTTP_200_OK)
def increment_view(sample_id: int, db: Session = Depends(get_db)):
    sample = db.execute(select(Sample).where(Sample.id == sample_id, Sample.deleted_at.is_(None))).scalar_one_or_none()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    sample.views += 1
    db.commit()
    return {"ok": True, "views": sample.views}

@router.post("/{sample_id}/download", status_code=status.HTTP_200_OK)
def increment_download(sample_id: int, db: Session = Depends(get_db)):
    sample = db.execute(select(Sample).where(Sample.id == sample_id, Sample.deleted_at.is_(None))).scalar_one_or_none()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    sample.downloads += 1
    db.commit()
    return {"ok": True, "downloads": sample.downloads}
