from fastapi import APIRouter, HTTPException
from pathlib import Path
from fastapi import UploadFile, File, Form
import shutil
from fastapi.responses import JSONResponse
import json
import tempfile
import os
import logging
from typing import Any, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("content")

router = APIRouter(prefix="/content", tags=["content"])


def _base_dir() -> Path:
    return Path(__file__).resolve().parents[3]


def _content_path(file_name: str) -> Path:
    return _base_dir() / "content" / file_name


def load_json(file_name: str) -> Dict[str, Any]:
    file_path = _content_path(file_name)
    logger.info(f"LOAD file={file_name} path={file_path}")

    if not file_path.exists():
        return {"error": f"Missing file: {file_path}"}

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def _parse_date_iso(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return datetime(1970, 1, 1)

def _testimonial_upload_dir() -> Path:
    return _base_dir() / "public" / "uploads" / "testimonials"

def save_json(file_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    file_path = _content_path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"SAVE target={file_path} cwd={os.getcwd()} base={_base_dir()}")

    try:
        payload = json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        encoding="utf-8",
        dir=str(file_path.parent),
        suffix=".tmp",
    ) as tf:
        tf.write(payload)
        tmp_path = Path(tf.name)

    logger.info(f"SAVE tmp={tmp_path}")

    tmp_path.replace(file_path)

    try:
        verify = json.loads(file_path.read_text(encoding="utf-8"))
        logger.info(f"SAVE verify_ok keys={list(verify.keys())[:10]}")
    except Exception as e:
        logger.exception(f"SAVE verify_failed {e}")

    return {"ok": True, "file": file_name, "path": str(file_path)}


@router.get("/home")
def get_home_content():
    return load_json("home.json")


@router.put("/home")
def update_home_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    result = save_json("home.json", body)
    return JSONResponse(status_code=200, content=result)


@router.get("/about")
def get_about_content():
    return load_json("about.json")


@router.put("/about")
def update_about_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    result = save_json("about.json", body)
    return JSONResponse(status_code=200, content=result)


@router.get("/contact")
def get_contact_content():
    return load_json("contact.json")


@router.put("/contact")
def update_contact_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    result = save_json("contact.json", body)
    return JSONResponse(status_code=200, content=result)


@router.get("/faqs")
def get_faqs_content():
    return load_json("faqs.json")


@router.put("/faqs")
def update_faqs_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("faqs.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "FAQs content updated", "file": "faqs.json"},
    )


@router.get("/feedback")
def get_feedback_content():
    return load_json("feedback.json")


@router.put("/feedback")
def update_feedback_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("feedback.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Feedback content updated", "file": "feedback.json"},
    )


@router.get("/blog")
def get_blog_content():
    return load_json("blog.json")


@router.put("/blog")
def update_blog_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("blog.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Blog content updated", "file": "blog.json"},
    )


@router.get("/blog-details")
def get_blog_details_content():
    return load_json("blogdetail.json")


@router.put("/blog-details")
def update_blog_details_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("blogdetail.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Blog details content updated", "file": "blogdetail.json"},
    )

@router.get("/dashboard-preview")
def get_dashboard_preview_content():
    return load_json("dashboardpreview.json")


@router.put("/dashboard-preview")
def update_dashboard_preview_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    result = save_json("dashboardpreview.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Dashboard preview content updated", "file": "dashboardpreview.json", "meta": result},
    )

@router.get("/arohio/main-feature")
def get_arohio_main_feature_content():
    return load_json("arohio-main-feature.json")


@router.put("/arohio/main-feature")
def update_arohio_main_feature_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("arohio-main-feature.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Arohio main feature content updated", "file": "arohio-main-feature.json"},
    )


@router.get("/header")
def get_header_content():
    return load_json("header.json")


@router.put("/header")
def update_header_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("header.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Header content updated", "file": "header.json"},
    )


@router.get("/footer")
def get_footer_content():
    return load_json("footer.json")


@router.put("/footer")
def update_footer_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("footer.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Footer content updated", "file": "footer.json"},
    )


@router.get("/terms")
def get_terms_content():
    return load_json("terms.json")


@router.put("/terms")
def update_terms_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("terms.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Terms content updated", "file": "terms.json"},
    )


@router.get("/refund-policy")
def get_refund_policy_content():
    return load_json("refunds.json")


@router.put("/refund-policy")
def update_refund_policy_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("refunds.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Refund policy content updated", "file": "refunds.json"},
    )


@router.get("/privacy-policy")
def get_privacy_policy_content():
    return load_json("privacy-policy.json")


@router.put("/privacy-policy")
def update_privacy_policy_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("privacy-policy.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Privacy policy content updated", "file": "privacy-policy.json"},
    )


@router.get("/book-publishing")
def get_book_publishing_content():
    return load_json("book-publishing.json")


@router.put("/book-publishing")
def update_book_publishing_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("book-publishing.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Book publishing content updated", "file": "book-publishing.json"},
    )

@router.post("/testimonials")
def add_testimonial(body: Dict[str, Any]):
    required_fields = ["first_name", "last_name", "service", "rating", "message"]

    for field in required_fields:
        if not body.get(field):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}",
            )

    data = load_json("testimonials.json")

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Invalid testimonials file")

    testimonials = data.get("testimonials", [])

    if not isinstance(testimonials, list):
        raise HTTPException(status_code=500, detail="Invalid testimonials format")

    new_testimonial = {
        "id": f"t{len(testimonials) + 1}",
        "first_name": body["first_name"].strip(),
        "last_name": body["last_name"].strip(),
        "role": body.get("role", "").strip(),
        "service": body["service"],
        "rating": int(body["rating"]),
        "message": body["message"].strip(),
        "avatar_url": body.get("avatar_url") or "https://i.pravatar.cc/120",
        "published": bool(body.get("publish_permission", False)),
        "created_at": datetime.utcnow().isoformat(),
    }

    testimonials.append(new_testimonial)
    data["testimonials"] = testimonials

    save_json("testimonials.json", data)

    return JSONResponse(
        status_code=201,
        content={
            "ok": True,
            "message": "Testimonial submitted successfully",
            "testimonial_id": new_testimonial["id"],
        },
    )

@router.get("/publishing-digital")
def get_publishing_digital_content():
    return load_json("publishing_digital.json")


@router.put("/publishing-digital")
def update_publishing_digital_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("publishing_digital.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Publishing digital content updated", "file": "publishing_digital.json"},
    )


@router.get("/accessibilty-feature")
def get_accessibilty_feature_content():
    return load_json("accessibilty-feature.json")


@router.put("/accessibilty-feature")
def update_accessibilty_feature_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("accessibilty-feature.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Accessibilty feature content updated", "file": "accessibilty-feature.json"},
    )


@router.get("/it-developement")
def get_it_developement_content():
    return load_json("it-developement.json")


@router.put("/it-developement")
def update_it_developement_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("it-developement.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "IT developement content updated", "file": "it-developement.json"},
    )


@router.get("/data-labelling")
def get_data_labelling_content():
    return load_json("data-labelling.json")


@router.put("/data-labelling")
def update_data_labelling_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("data-labelling.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Data labelling content updated", "file": "data-labelling.json"},
    )


@router.get("/localization")
def get_localization_content():
    return load_json("localization.json")


@router.put("/localization")
def update_localization_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("localization.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Localization content updated", "file": "localization.json"},
    )


@router.get("/elearning")
def get_elearning_content():
    return load_json("elearning.json")


@router.put("/elearning")
def update_elearning_content(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(status_code=400, detail="Body must be a non-empty JSON object")

    save_json("elearning.json", body)

    return JSONResponse(
        status_code=200,
        content={"ok": True, "message": "Elearning content updated", "file": "elearning.json"},
    )

@router.get("/blog/latest")
def get_latest_blog_posts(limit: int = 3):
    data = load_json("blog.json")

    if isinstance(data, dict) and data.get("error"):
        raise HTTPException(status_code=404, detail=data["error"])

    posts = data.get("posts", [])
    if not isinstance(posts, list):
        raise HTTPException(status_code=500, detail="Invalid blog.json format")

    posts_sorted = sorted(
        posts,
        key=lambda p: _parse_date_iso(str(p.get("dateISO", ""))),
        reverse=True,
    )

    latest = posts_sorted[: max(1, min(limit, 50))]

    return {
        "items": [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "dateISO": p.get("dateISO"),
                "readTime": p.get("readTime"),
                "cover": p.get("cover") or data.get("assets", {}).get("fallback_cover"),
                "excerpt": p.get("excerpt"),
                "slug": p.get("slug"),
                "href": f"/blog/{p.get('slug')}",
            }
            for p in latest
        ]
    }
@router.post("/testimonial-avatar")
async def upload_testimonial_avatar(
    file: UploadFile = File(...),
    testimonial_id: str = Form(...)
):
    logger.info(f"UPLOAD_START testimonial_id={testimonial_id} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        logger.error(f"UPLOAD_INVALID_TYPE testimonial_id={testimonial_id} content_type={file.content_type}")
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    logger.info(f"UPLOAD_DIR path={upload_dir}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    logger.info(f"UPLOAD_EXT original_ext={ext}")
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"
        logger.info(f"UPLOAD_EXT_FALLBACK new_ext={ext}")

    original_stem = Path(file.filename).stem
    safe_name = f"{original_stem}{ext}"

    file_path = upload_dir / safe_name
    logger.info(f"UPLOAD_FILEPATH path={file_path}")

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"UPLOAD_WRITE_SUCCESS path={file_path}")
    except Exception as e:
        logger.exception(f"UPLOAD_WRITE_FAILED testimonial_id={testimonial_id} error={e}")
        raise HTTPException(status_code=500, detail="Failed to save image")
    finally:
        await file.close()
        logger.info(f"UPLOAD_FILE_CLOSED testimonial_id={testimonial_id}")

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    logger.info(f"UPLOAD_BASE_URL base_url={base_url}")

    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"
    logger.info(f"UPLOAD_PUBLIC_URL url={public_url}")

    data = load_json("feedback.json")
    logger.info("UPLOAD_JSON_LOADED file=feedback.json")

    if isinstance(data, dict) and data.get("error"):
        logger.error(f"UPLOAD_JSON_ERROR error={data.get('error')}")
        raise HTTPException(status_code=404, detail=data["error"])

    testimonials = data.get("testimonials", [])
    logger.info(f"UPLOAD_TESTIMONIALS_COUNT count={len(testimonials) if isinstance(testimonials, list) else 'invalid'}")

    if not isinstance(testimonials, list):
        logger.error("UPLOAD_INVALID_JSON_FORMAT testimonials_not_list")
        raise HTTPException(status_code=500, detail="Invalid feedback.json testimonials format")

    updated = False
    for t in testimonials:
        if isinstance(t, dict) and str(t.get("id")) == str(testimonial_id):
            t["avatar_url"] = public_url
            updated = True
            logger.info(f"UPLOAD_TESTIMONIAL_UPDATED testimonial_id={testimonial_id}")
            break

    if not updated:
        logger.error(f"UPLOAD_TESTIMONIAL_NOT_FOUND testimonial_id={testimonial_id}")
        raise HTTPException(status_code=404, detail=f"Testimonial id not found: {testimonial_id}")

    data["testimonials"] = testimonials
    save_json("feedback.json", data)
    logger.info(f"UPLOAD_JSON_SAVED file=feedback.json testimonial_id={testimonial_id}")

    logger.info(f"UPLOAD_COMPLETE testimonial_id={testimonial_id}")

    return {
        "ok": True,
        "url": public_url,
        "testimonial_id": testimonial_id,
        "updated_json": True
    }
@router.post("/publishing-digital/upload-image")
async def upload_publishing_digital_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"PUBLISHING_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        logger.error(f"PUBLISHING_UPLOAD_INVALID_TYPE content_type={file.content_type}")
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    logger.info(f"PUBLISHING_UPLOAD_DIR path={upload_dir}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    logger.info(f"PUBLISHING_UPLOAD_EXT original_ext={ext}")
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"
        logger.info(f"PUBLISHING_UPLOAD_EXT_FALLBACK new_ext={ext}")

    original_stem = Path(file.filename).stem
    safe_name = f"{original_stem}{ext}"

    file_path = upload_dir / safe_name
    logger.info(f"PUBLISHING_UPLOAD_FILEPATH path={file_path}")

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"PUBLISHING_UPLOAD_WRITE_SUCCESS path={file_path}")
    except Exception as e:
        logger.exception(f"PUBLISHING_UPLOAD_WRITE_FAILED error={e}")
        raise HTTPException(status_code=500, detail="Failed to save image")
    finally:
        await file.close()
        logger.info("PUBLISHING_UPLOAD_FILE_CLOSED")

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    logger.info(f"PUBLISHING_UPLOAD_BASE_URL base_url={base_url}")

    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"
    logger.info(f"PUBLISHING_UPLOAD_PUBLIC_URL url={public_url}")

    data = load_json("publishing_digital.json")
    logger.info("PUBLISHING_JSON_LOADED file=publishing_digital.json")

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Invalid publishing_digital.json")

    keys = json_path.split(".")
    ref = data

    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]

    ref[keys[-1]] = public_url

    save_json("publishing_digital.json", data)
    logger.info(f"PUBLISHING_JSON_UPDATED json_path={json_path}")

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path,
        "updated_json": True
    }
@router.post("/accessibilty-feature/upload-image")
async def upload_accessibility_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"ACCESSIBILITY_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("accessibilty-feature.json")
    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("accessibilty-feature.json", data)

    return {"ok": True, "url": public_url, "json_path": json_path}

@router.post("/it-developement/upload-image")
async def upload_it_development_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"IT_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("it-developement.json")
    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("it-developement.json", data)

    return {"ok": True, "url": public_url, "json_path": json_path}

@router.post("/localization/upload-image")
async def upload_localization_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"LOCALIZATION_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("localization.json")
    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("localization.json", data)

    return {"ok": True, "url": public_url, "json_path": json_path}

@router.post("/data-labelling/upload-image")
async def upload_data_labelling_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"DATALABEL_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("data-labelling.json")
    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("data-labelling.json", data)

    return {"ok": True, "url": public_url, "json_path": json_path}

@router.post("/elearning/upload-image")
async def upload_elearning_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(
        f"ELEARNING_UPLOAD_START json_path={json_path} filename={file.filename}"
    )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("elearning.json")
    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("elearning.json", data)

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path
    }

@router.post("/arohio/main-feature/upload-image")
async def upload_arohio_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"AROHIO_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("arohio-main-feature.json")

    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("arohio-main-feature.json", data)

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path
    }
@router.post("/blog/upload-image")
async def upload_blog_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(f"BLOG_UPLOAD_START json_path={json_path} filename={file.filename}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("blog.json")

    keys = json_path.split(".")
    ref = data
    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]
    ref[keys[-1]] = public_url

    save_json("blog.json", data)

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path
    }
@router.post("/blog-details/upload-image")
async def upload_blog_details_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(
        f"BLOG_DETAILS_UPLOAD_START json_path={json_path} filename={file.filename}"
    )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("blogdetail.json")

    keys = json_path.split(".")
    ref = data

    for k in keys[:-1]:
        ref = ref[int(k)] if k.isdigit() else ref[k]

    last_key = keys[-1]
    if isinstance(ref, list):
        ref[int(last_key)] = public_url
    else:
        ref[last_key] = public_url

    save_json("blogdetail.json", data)

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path
    }

@router.post("/home/upload-image")
async def upload_home_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(
        f"HOME_UPLOAD_START json_path={json_path} filename={file.filename}"
    )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("home.json")

    keys = json_path.split(".")
    ref = data

    for k in keys[:-1]:
        if isinstance(ref, list):
            ref = ref[int(k)]
        else:
            ref = ref[k]

    last_key = keys[-1]
    if isinstance(ref, list):
        ref[int(last_key)] = public_url
    else:
        ref[last_key] = public_url

    save_json("home.json", data)

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path
    }
@router.post("/about/upload-image")
async def upload_about_image(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(
        f"ABOUT_UPLOAD_START json_path={json_path} filename={file.filename}"
    )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    data = load_json("about.json")

    keys = json_path.split(".")
    ref = data

    for k in keys[:-1]:
        if isinstance(ref, list):
            ref = ref[int(k)]
        else:
            ref = ref[k]

    last_key = keys[-1]
    if isinstance(ref, list):
        ref[int(last_key)] = public_url
    else:
        ref[last_key] = public_url

    save_json("about.json", data)

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path
    }
@router.get("/blog-post-map")
def get_blog_post_map():
    return load_json("blog_post_map.json")

@router.put("/blog-post-map")
def update_blog_post_map(body: Dict[str, Any]):
    if not isinstance(body, dict) or not body:
        raise HTTPException(
            status_code=400,
            detail="Body must be a non-empty JSON object"
        )

    save_json("blog_post_map.json", body)

    return JSONResponse(
        status_code=200,
        content={
            "ok": True,
            "message": "Blog post mapping updated",
            "file": "blog_post_map.json"
        }
    )
@router.post("/footer/upload-certificate")
async def upload_footer_certificate(
    file: UploadFile = File(...),
    json_path: str = Form(...)
):
    logger.info(
        f"FOOTER_CERT_UPLOAD_START json_path={json_path} filename={file.filename}"
    )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    upload_dir = _testimonial_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    safe_name = f"{Path(file.filename).stem}{ext}"
    file_path = upload_dir / safe_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    base_url = os.getenv("APP_URL", "http://localhost:8000")
    public_url = f"{base_url}/api/uploads/testimonials/{safe_name}"

    logger.info(f"FOOTER_CERT_PUBLIC_URL url={public_url}")

    data = load_json("footer.json")

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Invalid footer.json")

    keys = json_path.split(".")
    ref = data

    for k in keys[:-1]:
        if isinstance(ref, list):
            ref = ref[int(k)]
        else:
            ref = ref[k]

    last_key = keys[-1]
    if isinstance(ref, list):
        ref[int(last_key)] = public_url
    else:
        ref[last_key] = public_url

    save_json("footer.json", data)

    logger.info(
        f"FOOTER_CERT_UPLOAD_DONE json_path={json_path}"
    )

    return {
        "ok": True,
        "url": public_url,
        "json_path": json_path,
        "updated_json": True
    }
