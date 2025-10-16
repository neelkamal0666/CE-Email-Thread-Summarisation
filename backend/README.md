# CE Email Summarization Backend

Production-ready Flask backend with modular architecture and separation of concerns.

## Architecture

```
backend/
├── app.py                      # Application factory and entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── models/                    # Data models
│   ├── __init__.py
│   ├── database.py           # Database connection manager
│   ├── thread.py             # Thread model
│   ├── summary.py            # Summary model
│   └── audit_log.py          # Audit log model
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── thread_service.py     # Thread operations
│   ├── summary_service.py    # Summary operations
│   ├── nlp_service.py        # NLP summarization
│   └── analytics_service.py  # Analytics operations
└── routes/                    # API endpoints (controllers)
    ├── __init__.py
    ├── health_routes.py      # Health check
    ├── thread_routes.py      # Thread endpoints
    ├── summary_routes.py     # Summary endpoints
    └── analytics_routes.py   # Analytics endpoints
```

## Design Patterns

### 1. Application Factory Pattern
```python
app = create_app('production')  # or 'development', 'testing'
```

### 2. Service Layer Pattern
Business logic separated from routes:
- **Routes**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Models**: Data structures and database operations

### 3. Dependency Injection
Services are injected where needed, making testing easier.

### 4. Configuration Management
Environment-specific configurations with validation.

## Layers

### Models Layer (`models/`)
**Responsibility**: Data structures and database operations

- `database.py`: Connection management, schema initialization
- `thread.py`: Thread data model
- `summary.py`: Summary data model with business methods
- `audit_log.py`: Audit log model

**Example:**
```python
from models.thread import Thread

thread = Thread(
    thread_id="CE-123",
    topic="Delivery Issue",
    subject="Late Delivery",
    # ...
)
```

### Services Layer (`services/`)
**Responsibility**: Business logic and orchestration

- `thread_service.py`: Thread CRUD, import logic
- `summary_service.py`: Summary CRUD, approval workflow
- `nlp_service.py`: NLP summarization (OpenAI + rule-based)
- `analytics_service.py`: Analytics calculations

**Example:**
```python
from services.thread_service import ThreadService

service = ThreadService(db)
threads = service.get_all_threads()
service.create_thread(thread)
```

### Routes Layer (`routes/`)
**Responsibility**: HTTP request/response handling

- `thread_routes.py`: `/api/threads/*` endpoints
- `summary_routes.py`: `/api/summaries/*` endpoints
- `analytics_routes.py`: `/api/analytics` endpoints
- `health_routes.py`: `/api/health` endpoint

**Example:**
```python
@thread_bp.route('/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    thread = thread_service.get_thread_by_id(thread_id)
    return jsonify(thread.to_dict())
```

## Configuration

### Environment Variables

Create `.env` file:
```bash
# Flask
FLASK_ENV=development  # or production
SECRET_KEY=your-secret-key-here

# Database
DATABASE_PATH=ce_threads.db

# OpenAI (optional)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=500

# Server
HOST=0.0.0.0
PORT=5000

# CORS
CORS_ORIGINS=*
```

### Configuration Classes

- **DevelopmentConfig**: Debug enabled, relaxed settings
- **ProductionConfig**: Debug disabled, security enforced
- **TestingConfig**: In-memory database, testing mode

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings
```

## Running

### Development
```bash
python app.py
# or
FLASK_ENV=development python app.py
```

### Production
```bash
FLASK_ENV=production gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## API Endpoints

### Health
- `GET /api/health` - Health check

### Threads
- `POST /api/threads/import` - Import threads
- `GET /api/threads` - List all threads
- `GET /api/threads/<id>` - Get specific thread
- `POST /api/threads/<id>/summarize` - Generate summary
- `DELETE /api/threads/<id>` - Delete thread

### Summaries
- `GET /api/summaries` - List summaries (optional: `?status=pending`)
- `GET /api/summaries/<id>` - Get specific summary
- `PUT /api/summaries/<id>/edit` - Edit summary
- `POST /api/summaries/<id>/approve` - Approve summary
- `POST /api/summaries/<id>/reject` - Reject summary

### Analytics
- `GET /api/analytics` - Dashboard statistics
- `GET /api/export/<id>` - Export approved summary


```


HTTP status codes:
- `200`: Success
- `400`: Bad request
- `404`: Not found
- `500`: Server error

## Logging

Production logs are written to `logs/app.log`:
- Rotating file handler (10MB max, 10 backups)
- INFO level logging
- Includes timestamp, level, message, and location

## Security Features

### 1. Configuration Validation
Production config requires secure SECRET_KEY.

### 2. CORS Configuration
Configurable allowed origins.

### 3. Input Validation
Request data validated before processing.

### 4. SQL Injection Prevention
Parameterized queries throughout.

### 5. Error Message Sanitization
Production errors don't expose internal details.
```

## Future Enhancements
- [ ] Using postgres instead of sqlite
- [ ] Add Redis caching layer
- [ ] Implement background job queue (Celery)
- [ ] Add user authentication and RBAC
- [ ] Implement rate limiting
- [ ] Add request/response validation schemas
- [ ] Add comprehensive test suite
- [ ] Add API documentation (Swagger)
- [ ] Add database migrations (Alembic)
- [ ] Add monitoring and metrics (Prometheus)
- [ ] Add distributed tracing


