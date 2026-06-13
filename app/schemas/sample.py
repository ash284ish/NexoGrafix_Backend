from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

# Category Schemas
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)

class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Industry Schemas
class IndustryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)

class IndustryOut(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Lead Schemas
class SampleLeadCreate(BaseModel):
    sample_id: Optional[int] = None
    name: str = Field(min_length=1, max_length=255)
    company: Optional[str] = Field(default=None, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=30)
    service_required: Optional[str] = Field(default=None, max_length=255)
    message: str = Field(min_length=1)

class SampleLeadOut(BaseModel):
    id: int
    sample_id: Optional[int]
    name: str
    company: Optional[str]
    email: EmailStr
    phone: Optional[str]
    service_required: Optional[str]
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

# Sample Schemas
class SampleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    short_description: str = Field(min_length=1, max_length=500)
    detailed_description: str = Field(min_length=1)
    featured_image: Optional[str] = Field(default=None, max_length=500)
    video_url: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default="published", max_length=30)  # draft, published
    visibility: Optional[str] = Field(default="public", max_length=30)  # public, private, password_protected
    password: Optional[str] = Field(default=None, max_length=255)
    
    technologies: Optional[List[str]] = None
    project_highlights: Optional[List[str]] = None
    client_outcome: Optional[str] = None
    tags: Optional[List[str]] = None
    gallery_images: Optional[List[str]] = None
    before_after_images: Optional[Dict[str, str]] = None
    screenshots: Optional[List[str]] = None
    download_files: Optional[List[Dict[str, str]]] = None

    category_ids: Optional[List[int]] = None
    industry_ids: Optional[List[int]] = None

    # SEO fields
    seo_title: Optional[str] = Field(default=None, max_length=255)
    seo_meta_description: Optional[str] = Field(default=None, max_length=500)
    seo_meta_keywords: Optional[str] = Field(default=None, max_length=500)
    seo_og_image: Optional[str] = Field(default=None, max_length=500)
    seo_canonical_url: Optional[str] = Field(default=None, max_length=500)

class SampleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    slug: Optional[str] = Field(default=None, max_length=255)
    short_description: Optional[str] = Field(default=None, max_length=500)
    detailed_description: Optional[str] = None
    featured_image: Optional[str] = Field(default=None, max_length=500)
    video_url: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=30)
    visibility: Optional[str] = Field(default=None, max_length=30)
    password: Optional[str] = Field(default=None, max_length=255)
    
    technologies: Optional[List[str]] = None
    project_highlights: Optional[List[str]] = None
    client_outcome: Optional[str] = None
    tags: Optional[List[str]] = None
    gallery_images: Optional[List[str]] = None
    before_after_images: Optional[Dict[str, str]] = None
    screenshots: Optional[List[str]] = None
    download_files: Optional[List[Dict[str, str]]] = None

    category_ids: Optional[List[int]] = None
    industry_ids: Optional[List[int]] = None

    # SEO fields
    seo_title: Optional[str] = Field(default=None, max_length=255)
    seo_meta_description: Optional[str] = Field(default=None, max_length=500)
    seo_meta_keywords: Optional[str] = Field(default=None, max_length=500)
    seo_og_image: Optional[str] = Field(default=None, max_length=500)
    seo_canonical_url: Optional[str] = Field(default=None, max_length=500)

class SampleOut(BaseModel):
    id: int
    title: str
    slug: str
    short_description: str
    detailed_description: str
    featured_image: Optional[str]
    video_url: Optional[str]
    status: str
    visibility: str
    password: Optional[str] = None  # Return password only if needed for edit, but maybe hide it for public
    
    technologies: Optional[List[str]]
    project_highlights: Optional[List[str]]
    client_outcome: Optional[str]
    tags: Optional[List[str]]
    gallery_images: Optional[List[str]]
    before_after_images: Optional[Dict[str, str]]
    screenshots: Optional[List[str]]
    download_files: Optional[List[Dict[str, str]]]
    
    categories: List[CategoryOut] = []
    industries: List[IndustryOut] = []

    # SEO fields
    seo_title: Optional[str]
    seo_meta_description: Optional[str]
    seo_meta_keywords: Optional[str]
    seo_og_image: Optional[str]
    seo_canonical_url: Optional[str]

    # Analytics
    views: int
    downloads: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
