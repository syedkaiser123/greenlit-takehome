# SimpleCRUD

SimpleCRUD is a Python project that implements CRUD (Create, Read, Update, Delete) functionality for managing users, companies, and films using FastAPI and SQLAlchemy.

## Project Structure

- **models/companies.py**: Defines the SQLAlchemy model for the Company entity and its Pydantic schema `CompanySchema`.
- **models/users.py**: Contains the SQLAlchemy model for the User entity, Pydantic schemas `UserSchema` and `UserRoleSchema`.
- **models/films.py**: Defines the SQLAlchemy model for the Film entity, and Pydantic schema `FilmSchema`.
- **database/database_config.py**: Contains the database configuration, including creating the database engine, sessionmaker, and declarative base.
- **main.py**: Implements the CRUD endpoints for users and films, along with a custom exception handler and a function to retrieve user roles with associated films and companies.

## Code Overview

- **models/companies.py**: Defines the Company model with columns like `name`, `contact_email_address`, and `phone_number`. It establishes relationships with films and users. Also, includes a Pydantic schema `CompanySchema` for data validation.
- **models/users.py**: Contains the User model with columns for user details and relationships with films and companies. It also defines Pydantic schemas `UserSchema` and `UserRoleSchema` for data validation.
- **models/films.py**: Defines the Film model with columns like `title`, `description`, and `genres`. It establishes relationships with companies and users. Includes Pydantic schema `FilmSchema` for data validation. Also, includes a custom SQLAlchemy type `ListType` for storing lists as strings in the database.
- **database/database_config.py**: Sets up the database configuration, including creating the database engine, sessionmaker, and declarative base.
- **main.py**: Implements CRUD endpoints for users and films, along with a custom exception handler and a function to retrieve user roles with associated films and companies.

## How to Run
1. Set up poetry on your system.
2. Install the required dependencies by running `poetry install` from the root directory.
3. clone the repo ```git clone https://github.com/syedkaiser123/greenlit-takehome.git```
4. Navigate to ```cd greenlit-takehome```
5. Set up your PostgreSQL database and update the `SQLALCHEMY_DATABASE_URL` in `database/database_config.py` with your database connection string. ```OR``` you can just use the given postgres connection string in the database/database_config.py and access it via the UI ```https://supabase.com/dashboard/project/rbuwsyjyaobjdyqizakw```

## Note: Here are the credentials to access the hosted database:
    - URL: https://supabase.com/dashboard/project/rbuwsyjyaobjdyqizakw
    - Username: syedkaiser123
    - Password: 525DloVS4uuldi0X
6. Run the FastAPI application by executing `uvicorn main:app --reload`.
7. Access the API endpoints through a web browser or API client like Postman.

## API Endpoints
- **POST** ```http://127.0.0.1:8000/users/```

- **DELETE** ```http://127.0.0.1:8000/users/1```
- **PUT** ```http://127.0.0.1:8000/users/18```
- **POST** ```http://127.0.0.1:8000/films/```
- **PUT** ```http://127.0.0.1:8000/films/5```
- **POST** ```http://127.0.0.1:8000/companies/```
- **PUT** ```http://127.0.0.1:8000/companies/2```
- **POST** ```http://127.0.0.1:8000/users/1/films/2```
- **GET** ```http://127.0.0.1:8000/user-roles/```

### Note: You can also find the postman collection in the above repo.

## Dependencies

- FastAPI: Web framework for building APIs with Python.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- uvicorn: ASGI server for running FastAPI applications.
- Pydantic: Data validation and settings management using Python type annotations.

### **Note**: All dependencies including the ones that are not mentioned here but are available in the ```pyproject.toml``` file, can be installed via the ```poetry install``` command as explained above.
