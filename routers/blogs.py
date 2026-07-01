from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from fastapi import UploadFile, File, Form
from typing import List
import shutil
import os
import shutil
import uuid
from sqlalchemy.exc import IntegrityError
router = APIRouter()
from auth_dependency import get_current_user

'''
@router.get(
    "/blogs",
    response_model=list[schemas.BlogResponse]
)
def get_blogs(
    db:Session=Depends(get_db)
):
    blogs = db.query(
        models.Blog
    ).all()
    return blogs
'''

@router.post("/blogs", openapi_extra={
    "requestBody": {
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "required": ["title", "content", "category_id", "images"],
                    "properties": {
                        "title": {
                            "type": "string",
                            "title": "Title"
                        },
                        "content": {
                            "type": "string",
                            "title": "Content"
                        },
                        "category_id": {
                            "type": "integer",
                            "title": "Category ID"
                        },
                        "images": {
                            "type": "array",
                            "title": "Images",
                            "items": {
                                "type": "string",
                                "format": "binary"   # <-- this makes Swagger show file picker
                            }
                        }
                    }
                }
            }
        },
        "required": True
    }
})
def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    images: List[UploadFile] = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # your existing code stays exactly the same
    user_id = current_user["user_id"]
    os.makedirs("uploads", exist_ok=True)

    if not images:
        raise HTTPException(
            status_code=400,
            detail="Please upload at least one image."
        )

    allowed_extensions = ["jpg", "jpeg", "png"]
    for img in images:
        if not img.filename or "." not in img.filename:
            raise HTTPException(
                status_code=400,
                detail="One of the uploaded files is invalid."
            )
        ext = img.filename.split(".")[-1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"'{img.filename}' is not a supported image type. Only jpg, jpeg, png allowed."
            )

    try:
        new_blog = models.Blog(
            title=title,
            content=content,
            category_id=category_id,
            user_id=user_id
        )
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid category selected. Please choose a valid category."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create blog right now. Please try again later."
        )

    image_list = []
    try:
        for img in images:
            ext = img.filename.split(".")[-1]
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            file_path = f"uploads/{unique_name}"

            with open(file_path, "wb") as f:
                shutil.copyfileobj(img.file, f)

            db_image = models.BlogImage(
                blog_id=new_blog.id,
                file_name=img.filename,
                file_path=file_path
            )
            db.add(db_image)
            image_list.append(file_path)

        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Blog was created but image upload failed. Please try uploading images again."
        )

    return {
        "message": "Blog created successfully",
        "blog_id": new_blog.id,
        "images": image_list
    }
'''
    user_id=request.state.user["user_id"]

    # image check
    allowed=[
        "jpg",
        "jpeg",
        "png"
    ]
    
    file_location=f"uploads/{image.filename}"

    with open(file_location,"wb") as buffer:

        shutil.copyfileobj(
            image.file,
            buffer
        )
    new_blog=models.Blog(
        title=title,
        content=content,
        category_id=category_id,
        user_id=user_id,
        image=image.filename
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
'''
@router.get("/blogs")
def get_blogs(
    request: Request,
    db:Session=Depends(get_db)
):

    try:
        blogs=db.query(models.Blog).all()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to load blogs right now. Please try again later."
        )

    return [

        {
            "id":blog.id,

            "title":blog.title,

            "content":blog.content,

            "category_id":blog.category_id,

            "user_id":blog.user_id,

            "image":
            f"{request.base_url}uploads/{blog.image}"

        }

        for blog in blogs
    ]

@router.get("/blogs/{blog_id}")
def get_blog(blog_id: int, request: Request, db: Session = Depends(get_db)):

    try:
        blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        images = db.query(models.BlogImage).filter(
            models.BlogImage.blog_id == blog_id
        ).all()

        image_urls = [
            f"{request.base_url}{img.file_path}"
            for img in images
        ]
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to load this blog right now. Please try again later."
        )

    return {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "images": image_urls
    }

@router.get("/categories")
def get_categories(
    db:Session=Depends(get_db)
):
    try:
        return db.query(
            models.Category
        ).all()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to load categories right now. Please try again later."
        )
