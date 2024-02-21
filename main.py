# from typing import Union
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

import httpx
from fastapi import Response
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from database.database_config import SessionLocal, engine
from models.users import *
from models.companies import *
from models.films import *
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI()

class CustomExceptionHandler(BaseHTTPMiddleware):
    """
    Middleware class for custom exception handling in FastAPI.
    
    This middleware intercepts exceptions raised during request processing
    and returns appropriate HTTP responses with error details.
    """
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exception:
            return http_exception
        except Exception as e:
            error_message = f"Internal Server Error: {str(e)}"
            return JSONResponse(status_code=500, content={"detail": error_message})

# Add custom exception handling middleware
app.add_middleware(CustomExceptionHandler)

# Add CORS middleware
app.add_middleware(CORSMiddleware)

SUPABASE_URL = "https://rbuwsyjyaobjdyqizakw.supabase.co"
# ANON KEY
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJidXdzeWp5YW9iamR5cWl6YWt3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg0NDkxOTUsImV4cCI6MjAyNDAyNTE5NX0.IE8iUt4HzyiCrudilxIff-7I7A7hAqCsMMLNvsEtKX4"
# SERVICE ROLE KEY
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJidXdzeWp5YW9iamR5cWl6YWt3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwODQ0OTE5NSwiZXhwIjoyMDI0MDI1MTk1fQ.geByTnNG5T1gnxtByUb54QgR3XSbEU_-c7uJhE5MN8Y"

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def add_user(user: UserSchema, db: Session, response_model=Response):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists or violates database constraints")
    except Exception as e:
        db.rollback()
        return {"message": "Failed to create user due to an unexpected error"}

# CRUD endpoints for users
@app.post("/users/")
async def create_new_user(user: UserSchema, db: Session = Depends(get_db)):
    """
    Creates a new user with the provided details.

    Args:
        user (UserSchema): The details of the new user to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: Details of the created user.
    """
    created_user = await add_user(user, db=db)
    return {
        "first_name": created_user.first_name,
        "last_name": created_user.last_name,
        "email": created_user.email,
        "minimum_fee": created_user.minimum_fee
    }

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes the user with the provided ID.

    Args:
        user_id (int): The ID of the user to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A message indicating the user deletion success.
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    """
    Updates the details of an existing user with the provided ID.

    Args:
        user_id (int): The ID of the user to be updated.
        user (UserSchema): The updated details of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserSchema: The updated details of the user.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        for key, value in user.dict().items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
            else:
                raise AttributeError(f"Invalid field: {key}")
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update violates database constraints")
    except AttributeError:
        raise HTTPException(status_code=422, detail="Invalid field in update data")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

# CRUD endpoints for films
@app.post("/films/", response_model=FilmSchema)
def create_film(film: FilmSchema, db: Session = Depends(get_db)):
    """
    Creates a new film with the provided details.

    Args:
        film (FilmSchema): The details of the new film to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FilmSchema: The details of the newly created film.
    """
    try:
        db_film = Film(**film.dict())
        db.add(db_film)
        db.commit()
        db.refresh(db_film)
        return db_film
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Bad Request: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create film: {str(e)}")

@app.put("/films/{film_id}", response_model=FilmSchema)
def update_film(film_id: int, film: FilmSchema, db: Session = Depends(get_db)):
    """
    Updates an existing film with the provided details.

    Args:
        film_id (int): The ID of the film to be updated.
        film (FilmSchema): The details of the film to be updated.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FilmSchema: The updated details of the film.
    """
    try:
        db_film = db.query(Film).filter(Film.id == film_id).first()
        if db_film is None:
            raise HTTPException(status_code=404, detail="Film not found")
        for key, value in film.dict().items():
            setattr(db_film, key, value)
        db.commit()
        db.refresh(db_film)
        return db_film
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update film with ID {film_id}: {str(e)}")


# CRUD endpoints for companies
@app.post("/companies/", response_model=CompanySchema)
def create_company(company: CompanySchema, db: Session = Depends(get_db)):
    """
    Creates a new company with the provided details.

    Args:
        company (CompanySchema): The details of the new company.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        CompanySchema: The details of the newly created company.
    """
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.put("/companies/{company_id}", response_model=CompanySchema)
def update_company(company_id: int, company: CompanySchema, db: Session = Depends(get_db)):
    """
    Update a company.

    Updates the details of the specified company.

    Args:
        company_id (int): The ID of the company.
        company (CompanySchema): The updated company details.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the company is not found.

    Returns:
        CompanySchema: The updated company details.
    """
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

# CRUD endpoints for user-film association
@app.post("/users/{user_id}/films/{film_id}")
def associate_user_film(user_id: int, film_id: int, db: Session = Depends(get_db)):
    """
    Associate a film with a user.

    Adds an association between the specified user and film.

    Args:
        user_id (int): The ID of the user.
        film_id (int): The ID of the film.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user or film is not found.

    Returns:
        dict: A message indicating the successful association of the film with the user.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    db_film = db.query(Film).filter(Film.id == film_id).first()
    if db_user is None or db_film is None:
        raise HTTPException(status_code=404, detail="User or Film not found")
    db_user.films.append(db_film)
    db.commit()
    return {"message": "Film associated with user successfully"}

@app.delete("/users/{user_id}/films/{film_id}")
def disassociate_user_film(user_id: int, film_id: int, db: Session = Depends(get_db)):
    """
    Disassociate a film from a user.

    Removes the association between the specified user and film.

    Args:
        user_id (int): The ID of the user.
        film_id (int): The ID of the film.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user or film is not found.

    Returns:
        dict: A message indicating the successful disassociation of the film from the user.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    db_film = db.query(Film).filter(Film.id == film_id).first()
    if db_user is None or db_film is None:
        raise HTTPException(status_code=404, detail="User or Film not found")
    db_user.films.remove(db_film)
    db.commit()
    return {"message": "Film disassociated from user successfully"}

# CRUD endpoints for user-company association
@app.post("/users/{user_id}/companies/{company_id}")
def associate_user_company(user_id: int, company_id: int, db: Session = Depends(get_db)):
    """
    Associate a company with a user.

    Creates an association between the specified user and company.

    Args:
        user_id (int): The ID of the user.
        company_id (int): The ID of the company.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user or company is not found.

    Returns:
        dict: A message indicating the successful association of the company with the user.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_user is None or db_company is None:
        raise HTTPException(status_code=404, detail="User or Company not found")
    db_user.companies.append(db_company)
    db.commit()
    return {"message": "Company associated with user successfully"}

@app.delete("/users/{user_id}/companies/{company_id}")
def disassociate_user_company(user_id: int, company_id: int, db: Session = Depends(get_db)):
    """
    Disassociate a company from a user.

    Deletes the association between the specified user and company.

    Args:
        user_id (int): The ID of the user.
        company_id (int): The ID of the company.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user or company is not found.

    Returns:
        dict: A message indicating the successful disassociation of the company from the user.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_user is None or db_company is None:
        raise HTTPException(status_code=404, detail="User or Company not found")
    db_user.companies.remove(db_company)
    db.commit()
    return {"message": "Company disassociated from user successfully"}


@app.get("/user-roles/", response_model=List[UserRoleSchema])
def get_user_roles(db: Session = Depends(get_db)):
    """
    Retrieve existing user roles along with their associated films and companies.
    """
    user_roles = get_user_roles_with_associations(db)
    return user_roles

def get_user_roles_with_associations(db: Session) -> List[UserRoleSchema]:
    """
    Retrieve existing user roles along with their associated films and companies.
    """
    user_roles = []
    users = db.query(User).options(joinedload(User.films), joinedload(User.companies)).all()

    for user in users:
        films = [
            {
                "title": film.title,
                "description": film.description,
                "budget": film.budget,
                "release_year": film.release_year,
                "genres": film.genres
                } for film in user.films]
        companies = [
            {
                "name": company.name,
                "contact_email_address": company.contact_email_address,
                "phone_number": company.phone_number
                } for company in user.companies]

        user_roles.append({
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "minimum_fee": user.minimum_fee,
            "films": films,
            "companies": companies
        })

    return user_roles