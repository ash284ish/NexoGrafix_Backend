from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.sample_category import SampleCategory
from app.models.sample_industry import SampleIndustry
from app.models.sample import Sample

def seed_samples():
    session: Session = SessionLocal()

    # 1. Seed Categories
    categories_data = [
        {"name": "Accessibility", "slug": "accessibility"},
        {"name": "PDF Accessibility", "slug": "pdf-accessibility"},
        {"name": "EPUB Accessibility", "slug": "epub-accessibility"},
        {"name": "XML Conversion", "slug": "xml-conversion"},
        {"name": "Translation & Localization", "slug": "translation-localization"},
        {"name": "AI Annotation", "slug": "ai-annotation"},
        {"name": "Data Annotation", "slug": "data-annotation"},
        {"name": "Assessment Development", "slug": "assessment-development"},
        {"name": "Educational Content", "slug": "educational-content"},
    ]

    categories_map = {}
    for cat in categories_data:
        existing = session.query(SampleCategory).filter(SampleCategory.slug == cat["slug"]).first()
        if not existing:
            new_cat = SampleCategory(name=cat["name"], slug=cat["slug"])
            session.add(new_cat)
            session.flush()
            categories_map[cat["slug"]] = new_cat
        else:
            categories_map[cat["slug"]] = existing

    # 2. Seed Industries
    industries_data = [
        {"name": "Publishing", "slug": "publishing"},
        {"name": "Education", "slug": "education"},
        {"name": "Healthcare", "slug": "healthcare"},
        {"name": "Banking", "slug": "banking"},
        {"name": "Technology", "slug": "technology"},
        {"name": "Legal", "slug": "legal"},
    ]

    industries_map = {}
    for ind in industries_data:
        existing = session.query(SampleIndustry).filter(SampleIndustry.slug == ind["slug"]).first()
        if not existing:
            new_ind = SampleIndustry(name=ind["name"], slug=ind["slug"])
            session.add(new_ind)
            session.flush()
            industries_map[ind["slug"]] = new_ind
        else:
            industries_map[ind["slug"]] = existing

    # 3. Seed Samples
    samples_data = [
        {
            "title": "PDF Accessibility Remediation for Higher Education Publishing",
            "slug": "pdf-accessibility-publishing",
            "short_description": "Comprehensive WCAG 2.1 AA and PDF/UA remediation of complex STEM textbooks containing multi-column layouts, mathematical formulas, and nested tables.",
            "detailed_description": "<h3>Project Overview</h3><p>A leading higher education publisher needed to make their legacy catalog of over 100 textbooks fully accessible for visually impaired students using screen readers. The textbooks were filled with complex structural components including sidebars, multi-column reading flows, mathematical equations, and intricate tables.</p><h3>Our Process</h3><p>We analyzed each textbook to establish document tag structure tree, defined logical reading order, added high-quality descriptions (alt text) for STEM diagrams, and verified using screen readers (NVDA, JAWS) and PAC 2021 checker.</p>",
            "featured_image": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=800&q=80",
            "video_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "status": "published",
            "visibility": "public",
            "technologies": ["Adobe Acrobat Pro", "CommonLook PDF", "PAC 2021", "NVDA", "JAWS"],
            "project_highlights": [
                "Achieved 100% WCAG 2.1 AA and PDF/UA compliance",
                "Remediated over 12,000 pages within a tight 3-month timeline",
                "Delivered accurate alt text descriptions for complex STEM illustrations"
            ],
            "client_outcome": "The publisher successfully distributed accessible digital textbooks to university libraries, preventing compliance violations and broadening their user base to include visually impaired students.",
            "tags": ["PDF Accessibility", "WCAG 2.1", "PDF/UA", "Remediation", "Higher Education"],
            "gallery_images": [
                "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=500&q=80",
                "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=500&q=80"
            ],
            "before_after_images": {
                "before": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=500&q=80",
                "after": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=500&q=80"
            },
            "screenshots": [
                "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=500&q=80"
            ],
            "download_files": [
                {"name": "PDF_Accessibility_Case_Study.pdf", "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}
            ],
            "seo_title": "PDF Accessibility Remediation Case Study | Nexografix",
            "seo_meta_description": "Read how Nexografix remediated over 12,000 pages of higher education textbooks to meet WCAG 2.1 AA and PDF/UA accessibility standards.",
            "seo_meta_keywords": "pdf accessibility, wcag, pdf remediation, higher education publishing, accessible pdf",
            "views": 154,
            "downloads": 42,
            "category_slugs": ["accessibility", "pdf-accessibility"],
            "industry_slugs": ["publishing", "education"]
        },
        {
            "title": "EPUB 3 Accessibility Conversion for K-12 Textbooks",
            "slug": "epub-accessibility-k12",
            "short_description": "Converting legacy print assets into highly interactive and accessible EPUB 3 formats matching accessibility standards.",
            "detailed_description": "<h3>Project Overview</h3><p>An educational publisher requested the conversion of their primary K-12 science catalog into reflowable and fixed-layout EPUB 3 packages. The files needed to comply with the EPUB Accessibility 1.1 specification and be optimized for screen reader navigation.</p>",
            "featured_image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
            "status": "published",
            "visibility": "public",
            "technologies": ["Ace by DAISY", "Sigil", "HTML5", "CSS3", "Calibre"],
            "project_highlights": [
                "Generated accessible EPUB 3 output scoring 100% on Ace checker",
                "Structured complex sidebars and tables using semantic HTML5 elements",
                "Embedded media overlays for sync-text-to-speech support"
            ],
            "client_outcome": "The publisher entered state adoption programs that require strict accessibility, opening new revenue streams in public school systems.",
            "tags": ["EPUB 3", "Accessibility", "Daisy Consortium", "K-12", "E-learning"],
            "download_files": [
                {"name": "EPUB_Accessibility_Best_Practices.epub", "url": "https://github.com/IDPF/epub3-samples/releases/download/20230704/accessible_epub_3.epub"}
            ],
            "seo_title": "EPUB 3 Accessibility Conversion | Nexografix",
            "views": 98,
            "downloads": 18,
            "category_slugs": ["accessibility", "epub-accessibility"],
            "industry_slugs": ["publishing", "education"]
        },
        {
            "title": "Large-Scale XML Conversion for Tech Documentation",
            "slug": "xml-conversion-documentation",
            "short_description": "Migrating millions of lines of unstructured technical documents into DITA XML schemas for a Fortune 500 technology firm.",
            "detailed_description": "<h3>Project Overview</h3><p>Our client had millions of product manuals stored in legacy HTML and PDF formats. These files were difficult to maintain, update, and publish in multiple languages. We developed an automated XSLT workflow to migrate their documentation to structured DITA XML.</p>",
            "featured_image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
            "status": "published",
            "visibility": "public",
            "technologies": ["XSLT 3.0", "Oxygen XML Editor", "Python", "XPath"],
            "project_highlights": [
                "Automated migration with over 99.8% semantic accuracy",
                "Converted 300,000 pages of documentation to DITA XML format",
                "Reduced duplicate content across manuals by 35% through reuse design"
            ],
            "client_outcome": "The tech firm reduced localization costs by 45% and improved manual publishing speed from weeks to minutes.",
            "tags": ["XML", "DITA", "XSLT", "Data Migration", "Documentation"],
            "views": 72,
            "downloads": 11,
            "category_slugs": ["xml-conversion"],
            "industry_slugs": ["technology"]
        }
    ]

    for s_data in samples_data:
        existing = session.query(Sample).filter(Sample.slug == s_data["slug"]).first()
        if existing:
            continue

        sample_cats = [categories_map[slug] for slug in s_data["category_slugs"] if slug in categories_map]
        sample_inds = [industries_map[slug] for slug in s_data["industry_slugs"] if slug in industries_map]

        new_sample = Sample(
            title=s_data["title"],
            slug=s_data["slug"],
            short_description=s_data["short_description"],
            detailed_description=s_data["detailed_description"],
            featured_image=s_data["featured_image"],
            video_url=s_data.get("video_url"),
            status=s_data["status"],
            visibility=s_data["visibility"],
            technologies=s_data.get("technologies"),
            project_highlights=s_data.get("project_highlights"),
            client_outcome=s_data.get("client_outcome"),
            tags=s_data.get("tags"),
            gallery_images=s_data.get("gallery_images"),
            before_after_images=s_data.get("before_after_images"),
            screenshots=s_data.get("screenshots"),
            download_files=s_data.get("download_files"),
            seo_title=s_data.get("seo_title"),
            seo_meta_description=s_data.get("seo_meta_description"),
            seo_meta_keywords=s_data.get("seo_meta_keywords"),
            views=s_data["views"],
            downloads=s_data["downloads"],
            categories=sample_cats,
            industries=sample_inds
        )
        session.add(new_sample)

    session.commit()
    session.close()
    print("Samples seeded successfully")
