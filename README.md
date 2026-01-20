# DataSage

Comprehensive One-Stop Machine Learning Platform

---

## 🚀 Quick Start with Docker

Get the entire application running with **zero manual setup** in just 2 commands:

```bash
# 1. Clone the repository
git clone <repo-url>
cd DataSage

# 2. Start everything with Docker
docker compose up --build
```

That's it! The application will be available at:
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: Run separately (see Frontend Setup below)

---

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)
- **No Python or PostgreSQL installation required!**

---

## 🛠️ Setup Instructions

### 1. Environment Configuration

Copy the example environment file and customize if needed:

```bash
# Windows PowerShell
copy .env.example .env


```

**Default values work out of the box for development.** Edit `.env` only if you need to:
- Change database credentials
- Use a different port
- Customize JWT secret key

### 2. Start the Application

```bash
# Start all services (backend + PostgreSQL)
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build
```

**What happens automatically:**
1. ✅ PostgreSQL 17 database is created
2. ✅ Database tables are initialized
3. ✅ Backend dependencies are installed
4. ✅ FastAPI server starts with hot reload enabled

### 3. Verify Everything Works

```bash
# Check service status
docker compose ps

# View logs
docker compose logs -f backend

# Test API
curl http://localhost:8000/docs
```

---

## 🖥️ Frontend Setup

The frontend runs outside Docker for now:

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

---

## 🔧 Development Workflow

### Hot Reload

Code changes are automatically detected:
- **Backend**: Edit any `.py` file → Uvicorn reloads automatically
- **Frontend**: Edit any `.vue` file → Nuxt reloads automatically

### Viewing Logs

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# PostgreSQL only
docker compose logs -f postgres
```

### Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes database data)
docker compose down -v
```

### Rebuilding After Dependency Changes

```bash
# Rebuild backend after updating requirements.txt
docker compose up --build backend
```

### Accessing the Database

```bash
# Connect to PostgreSQL container
docker compose exec postgres psql -U datasage -d datasage_db

# Run SQL queries
\dt  # List tables
SELECT * FROM users;
```

### Running Backend Commands

```bash
# Execute Python scripts inside the container
docker compose exec backend python init_db.py

# Access Python shell
docker compose exec backend python

# Access container shell
docker compose exec backend bash
```

---

## 📁 Project Structure

```
DataSage/
├── backend/
│   ├── Dockerfile              # Backend container definition
│   ├── entrypoint.sh           # Startup script (auto-migrations)
│   ├── requirements.txt        # Python dependencies
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database connection
│   ├── models.py               # SQLAlchemy models
│   ├── init_db.py              # Database initialization
│   └── ...
├── frontend/
│   ├── package.json            # Node.js dependencies
│   └── ...
├── docker-compose.yml          # Multi-service orchestration
├── .env.example                # Environment template
└── README.md                   # This file
```

---

## 🐛 Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:
```bash
# Find and stop the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Or change the port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Database Connection Failed

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Check if PostgreSQL is healthy
docker compose ps

# Restart services
docker compose restart

# Check PostgreSQL logs
docker compose logs postgres
```

### Permission Denied on entrypoint.sh

**Error**: `permission denied: /entrypoint.sh`

**Solution**:
```bash
# Make script executable (Linux/Mac)
chmod +x backend/entrypoint.sh

# Rebuild the container
docker compose up --build
```

### Database Tables Not Created

**Error**: `relation "users" does not exist`

**Solution**:
```bash
# Manually run database initialization
docker compose exec backend python init_db.py

# Or restart services to trigger entrypoint
docker compose restart backend
```

### Hot Reload Not Working

**Solution**:
```bash
# Ensure source code is mounted correctly
docker compose down
docker compose up --build

# Check docker-compose.yml has:
# volumes:
#   - ./backend:/app
```

### Clean Slate Reset

To completely reset the environment:

```bash
# Stop all services and remove volumes
docker compose down -v

# Remove all containers and images
docker compose down --rmi all

# Start fresh
docker compose up --build
```

---

## 🚢 Production Deployment

**Note**: This Docker setup is optimized for **development**. For production:

1. Use multi-stage builds to reduce image size
2. Don't mount source code as volumes
3. Use production-grade WSGI server (e.g., Gunicorn)
4. Set strong `SECRET_KEY` in `.env`
5. Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
6. Enable HTTPS with reverse proxy (Nginx, Traefik)
7. Set `DEBUG=False` and remove `--reload` flag

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nuxt.js Documentation](https://nuxt.com/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker: `docker compose up --build`
5. Submit a pull request

---

## 📄 License


