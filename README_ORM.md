# MegaTrip ORM Implementation

This document explains the new ORM (Object-Relational Mapping) implementation using FastAPI as middleware between Streamlit and MySQL database.

## Architecture Overview

```
[External Users] → [Streamlit Frontend] → [FastAPI Middleware (Internal)] → [SQLAlchemy ORM] → [MySQL Database]
```

### Benefits of This Architecture

1. **Separation of Concerns**: Clear separation between UI, business logic, and data access
2. **Type Safety**: Pydantic models provide runtime type checking
3. **Better Error Handling**: Centralized error handling in the API layer
4. **Performance**: Connection pooling and optimized database queries
5. **Scalability**: API can be scaled independently of the frontend
6. **Documentation**: Automatic API documentation with FastAPI
7. **Testing**: Easier to test business logic separately from UI
8. **Security**: FastAPI is internal-only, not exposed to external traffic

## Project Structure

```
├── api/                    # FastAPI middleware (internal only)
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── models.py          # SQLAlchemy ORM models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   └── database.py        # Database connection
├── api_client.py          # API client for Streamlit
├── run_app.py             # Script to run both services
├── viewer/                # Streamlit pages (updated to use API)
├── model/                 # Legacy models (can be removed)
└── requirements.txt       # Updated dependencies
```

## Key Components

### 1. SQLAlchemy Models (`api/models.py`)

ORM models that map to database tables:

```python
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    # ... relationships
    created_trips = relationship("Trip", back_populates="creator")
```

### 2. Pydantic Schemas (`api/schemas.py`)

Data validation and serialization:

```python
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    user_id: int
    username: str
    created_at: datetime
```

### 3. CRUD Operations (`api/crud.py`)

Database operations using SQLAlchemy:

```python
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.user_id == user_id).first()
```

### 4. FastAPI Endpoints (`api/main.py`)

RESTful API endpoints (internal only):

```python
@app.get("/api/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # ... implementation
```

### 5. API Client (`api_client.py`)

Streamlit interface to the internal API:

```python
def login(self, username: str, password: str) -> Optional[Dict]:
    response = self.session.post(f"{self.base_url}/api/users/login", ...)
    return self._handle_response(response)
```

## Running the Application

### Option 1: Development Mode

Run both services locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run both FastAPI and Streamlit
python run_app.py
```

This will start:
- FastAPI server at `http://localhost:8000` (internal only)
- FastAPI docs at `http://localhost:8000/docs` (internal only)
- Streamlit app at `http://localhost:8501` (public)

### Option 2: Docker Compose

```bash
# Build and run with Docker
docker-compose up --build
```

This will start:
- MySQL database on port 3306
- FastAPI service (internal only, not exposed externally)
- Streamlit service on port 8501 (public)

## Security Architecture

### Network Isolation

- **FastAPI**: Runs internally, only accessible by Streamlit
- **Streamlit**: Public-facing interface for users
- **MySQL**: Internal database, only accessible by FastAPI

### Local Development:
```
FastAPI: 127.0.0.1:8000 (localhost only)
Streamlit: 0.0.0.0:8501 (public)
```

### Docker Production:
```
FastAPI: Internal Docker network only
Streamlit: Exposed on port 8501
MySQL: Internal Docker network only
```

## API Endpoints (Internal Only)

### User Endpoints
- `POST /api/users/` - Create user
- `POST /api/users/login` - Login user
- `GET /api/users/{user_id}` - Get user
- `DELETE /api/users/{user_id}` - Delete user

### Trip Endpoints
- `POST /api/trips/` - Create trip
- `GET /api/trips/{trip_id}` - Get trip with details
- `PUT /api/trips/{trip_id}` - Update trip
- `DELETE /api/trips/{trip_id}` - Delete trip
- `GET /api/trips/` - Get recent trips
- `GET /api/users/{user_id}/created-trips` - Get user's created trips
- `GET /api/users/{user_id}/participated-trips` - Get user's participated trips
- `POST /api/trips/{trip_id}/participants/{user_id}` - Add participant
- `DELETE /api/trips/{trip_id}/participants/{user_id}` - Remove participant

### Item Endpoints
- `POST /api/items/` - Create item
- `GET /api/items/{item_id}` - Get item
- `PUT /api/items/{item_id}` - Update item
- `DELETE /api/items/{item_id}` - Delete item
- `GET /api/trips/{trip_id}/items` - Get trip items

## Database Schema

The ORM models map to the existing database schema:

- `users` table → `User` model
- `trips` table → `Trip` model
- `items` table → `Item` model
- `trip_participants` table → Many-to-many relationship

## Migration from Legacy Code

To migrate existing Streamlit pages:

1. Replace direct database calls with API client calls
2. Update imports to use `api_client`
3. Handle API responses (JSON format)
4. Remove legacy model imports

Example migration:

```python
# Before (Direct DB)
from model.user_manager import UserManager
user = UserManager.get_user(username, password)

# After (API)
from api_client import api_client
login_result = api_client.login(username, password)
user = login_result["user"] if login_result else None
```

## Testing

### API Testing (Development Only)

FastAPI provides automatic interactive documentation:
- Visit `http://localhost:8000/docs` (only accessible during local development)
- Test endpoints directly in the browser

### Manual Testing

```bash
# Test user creation (local development only)
curl -X POST "http://localhost:8000/api/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'

# Test login (local development only)
curl -X POST "http://localhost:8000/api/users/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
```

## Performance Benefits

1. **Connection Pooling**: SQLAlchemy manages database connections efficiently
2. **Lazy Loading**: Relationships are loaded only when needed
3. **Query Optimization**: ORM generates optimized SQL queries
4. **Caching**: API responses can be cached
5. **Async Support**: FastAPI supports async operations
6. **Network Efficiency**: Internal API communication is faster than external calls

## Security Improvements

1. **Input Validation**: Pydantic validates all input data
2. **SQL Injection Prevention**: ORM prevents SQL injection attacks
3. **Error Handling**: Centralized error handling prevents information leakage
4. **Network Isolation**: FastAPI is not exposed to external traffic
5. **Authentication**: Can easily add JWT tokens or OAuth
6. **Rate Limiting**: Can add rate limiting to API endpoints
7. **Internal Communication**: API only accessible by authorized Streamlit app

## Next Steps

1. **Complete Migration**: Update all Streamlit pages to use the API
2. **Add Authentication**: Implement JWT tokens for secure authentication
3. **Add Tests**: Write unit tests for API endpoints
4. **Add Logging**: Implement comprehensive logging
5. **Add Monitoring**: Add health checks and monitoring
6. **Optimize Performance**: Add caching and query optimization
7. **Add Documentation**: Generate API documentation

## Troubleshooting

### Common Issues

1. **Connection Refused**: Make sure FastAPI is running before starting Streamlit
2. **Database Connection**: Check MySQL connection parameters in `config.py`
3. **Import Errors**: Make sure all dependencies are installed
4. **Port Conflicts**: Check if ports 8000 and 8501 are available
5. **API Communication**: Ensure API_URL environment variable is set correctly in Docker

### Debugging

1. Check FastAPI logs for API errors
2. Check Streamlit logs for frontend errors
3. Use FastAPI docs (`/docs`) to test API endpoints (local development only)
4. Check database logs for SQL errors
5. Verify internal network connectivity in Docker

## Conclusion

The ORM implementation provides a robust, scalable, and secure architecture for the MegaTrip application. It separates concerns, improves performance, and makes the codebase easier to test and maintain. The internal-only FastAPI design ensures that the API layer is not exposed to external threats while providing all the benefits of a modern REST API architecture. 