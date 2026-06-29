# My Blogs Project

## About Project

This is a Blog Management Backend API project developed using FastAPI. 
It allows users to create accounts, login, and manage blog posts with categories.
The project uses MySQL database to store users, blogs, and category data.

## Technologies Used
- Python
- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication
- Pydantic
- Uvicorn

## Features
- User Signup
- User Login with JWT Token Authentication
- Secure Password Encryption
- Get all blogs
- Create Blog
- View Blogs
- Update Blogs
- Delete Blogs
- Blog Category Management
- API documentation using Swagger UI

## How to Run Project
1. Clone the project
git clone your-github-link
2. Install required packages
pip install -r requirements.txt
3. Start server
uvicorn main:app --reload
4. Open browser
http://127.0.0.1:8000/docs

## Project Structure
- main.py → starts the application
- models.py → database tables
- schemas.py → data validation
- routers → API routes
- database.py → database connection

## Deployment

The project is deployed using Railway.
API URL: https://your-railway-link.up.railway.app
Swagger Documentation: https://your-railway-link.up.railway.app/docs
