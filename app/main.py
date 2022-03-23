import os
from typing import Generator

from fastapi import FastAPI, Depends, File
from fastapi.responses import RedirectResponse
from google.cloud import vision
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import app.core.config as app_config
from app.db.session import SessionLocal
from app.models import Brands, SubBrands

app = FastAPI()

if app_config.DEVELOPER_MODE:
    app = FastAPI(title=app_config.PROJECT_NAME,
                  description=app_config.PROJECT_DESCRIPTION,
                  version=app_config.PROJECT_VERSION)
else:
    app = FastAPI(title=app_config.PROJECT_NAME,
                  description=app_config.PROJECT_DESCRIPTION,
                  version=app_config.PROJECT_VERSION,
                  openapi_url=None,
                  redoc_url=None, docs_url=None)

if app_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in app_config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=app_config.ALLOW_METHODS,
        allow_headers=app_config.ALLOW_HEADERS,
    )

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(APP_ROOT, 'core/configs', 'ServiceAccountToken.json')


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"API": "v1"}


@app.get("/check/{company_name}")
async def check_company(*,
                        db: Session = Depends(get_db),
                        company_name: str):
    result = check_company_name(db, company_name)
    return result


@app.post("/check/image")
def check_image(*,
                db: Session = Depends(get_db),
                img: bytes = File(...)):
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=img)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    result = {}
    for logo in logos:
        status = check_company_name(db, logo.description)
        result[logo.description] = status.get('status')
    return result


@app.exception_handler(404)
def not_found(request, exc):
    return RedirectResponse("/")


def check_company_name(db, company_name: str):
    filters = [Brands.name == company_name]
    brands = db.query(Brands.name, Brands.status_id).filter(*filters).one_or_none()

    if not brands:
        brands = db.query(SubBrands.name, SubBrands.status_id).filter(SubBrands.name == company_name).one_or_none()
        if not brands:
            return {"status": "not found"}

    result = brands._asdict()
    if result['status_id'] == 3:
        return {"status": "bloody"}
    elif result['status_id'] == 2:
        return {"status": "pressure"}
    elif result['status_id'] == 1:
        return {"status": "clear"}
