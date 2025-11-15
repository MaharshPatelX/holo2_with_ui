# Environment Configuration Guide

## Overview

Both frontend and backend now use `.env` files for configuration. This makes it easy to change ports, URLs, and settings without modifying code.

## Files Created

### Backend
- `backend/.env` - Your configuration (gitignored)
- `backend/.env.example` - Template for others

### Frontend
- `frontend/.env` - Your configuration (gitignored)
- `frontend/.env.example` - Template for others

## Backend Configuration (`backend/.env`)

```env
# Backend Configuration
PORT=5001
HOST=0.0.0.0
DEBUG=true

# Model Configuration
MODEL_NAME=Hcompany/Holo2-4B
```

### Variables:
- `PORT` - Backend API port (default: 5001)
- `HOST` - Host to bind to (default: 0.0.0.0 for all interfaces)
- `DEBUG` - Enable debug mode (true/false)
- `MODEL_NAME` - HuggingFace model name

## Frontend Configuration (`frontend/.env`)

```env
# Frontend Configuration
PORT=8081
HOST=0.0.0.0
DEBUG=true

# Backend API URL (internal connection)
BACKEND_API_URL=http://localhost:5001
```

### Variables:
- `PORT` - Frontend web server port (default: 8081)
- `HOST` - Host to bind to (default: 0.0.0.0)
- `DEBUG` - Enable debug mode (true/false)
- `BACKEND_API_URL` - Internal URL to backend API

## For Different Environments

### Local Development
```env
# Frontend
PORT=8081
BACKEND_API_URL=http://localhost:5001

# Backend  
PORT=5001
```

### Runpod Deployment
```env
# Frontend
PORT=8081
BACKEND_API_URL=http://localhost:5001

# Backend
PORT=5001
```

### Custom Setup
Just edit the `.env` files and restart the services!

## Usage

### Install Dependencies
Both services now require `python-dotenv`:

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
pip install -r requirements.txt
```

### Run Services
The apps will automatically load `.env` on startup:

```bash
# Backend
cd backend
python app.py
# Reads PORT, HOST, DEBUG from .env

# Frontend
cd frontend
python app.py
# Reads PORT, HOST, DEBUG, BACKEND_API_URL from .env
```

## Important Notes

1. **`.env` files are gitignored** - Your configuration stays private
2. **`.env.example` files are tracked** - Share templates with others
3. **Restart required** - Changes to `.env` need service restart
4. **Defaults provided** - If `.env` is missing, defaults are used

## Troubleshooting

### Port already in use
Change `PORT` in the `.env` file:
```env
PORT=8082  # Use different port
```

### Can't connect to backend
Check `BACKEND_API_URL` in frontend `.env`:
```env
BACKEND_API_URL=http://localhost:5001
```

### Changes not taking effect
Restart both services after editing `.env`

---

**Easy configuration, no code changes needed!** 🎉

