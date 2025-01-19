
# BlackRose Assignment Backend

This is the backend project for the BlackRose Assignment. It is built using **FastAPI** and includes APIs for authentication, CRUD operations, and real-time WebSocket communication. The project is structured for scalability and maintainability, using clear module separation and service-oriented architecture.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Running the Application](#running-the-application)
- [Development Notes](#development-notes)

---

## Features

1. **Authentication**
   - Secure user authentication using `JWT` tokens.

2. **CRUD Operations**
   - Create, Read, Update, and Delete records stored in a CSV file.

3. **Real-Time WebSocket Communication**
   - Stream real-time OHLC (Open-High-Low-Close) data.

4. **Database Backup**
   - Automated CSV backup functionality.

5. **CORS Enabled**
   - Supports frontend communication from specific domains.

---

## Project Structure

```plaintext
blackrose-assignment/
├── app/
│   ├── api/
│   │   ├── auth.py               # Authentication-related routes
│   │   ├── record.py             # CRUD operations for records
│   │   ├── websocket.py          # WebSocket setup and routes
│   ├── db/
│   │   ├── base.py               # Database initialization logic
│   │   ├── random_repo.py        # Random number repository
│   ├── models/
│   │   ├── auth.py               # Authentication-related models
│   │   ├── random_number.py      # Models for random data generation
│   ├── services/
│   │   ├── auth_service.py       # Authentication logic
│   │   ├── file_service.py       # File handling and data operations
│   │   ├── random_gen_service.py # Background random data generation service
│   ├── utils/
│   │   ├── backup.py             # CSV backup utilities
│   │   ├── lock.py               # File locking utilities
├── backend_table.csv             # Main CSV file for record storage
├── backend_table_backup.csv      # Backup CSV file
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
└── data.db                       # SQLite database (if applicable)
```

---

## Setup Instructions

### Prerequisites

- Python 3.9 or above
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/blackrose-assignment.git
   cd blackrose-assignment
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. Access the API documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints

### Authentication

- `POST /auth/login` - Authenticate and generate a JWT token.

### CRUD Operations

- `GET /record/` - Fetch all records.
- `POST /record/` - Add a new record.
- `PUT /record/{id}` - Update a record by ID.
- `DELETE /record/{id}` - Delete a record by ID.

### WebSocket

- `/ohlc-stream/` - Stream OHLC data in real-time.

---

## Dependencies

The application uses the following Python libraries:

- **FastAPI**: Framework for building APIs.
- **Uvicorn**: ASGI server for FastAPI.
- **Socket.IO**: WebSocket support for real-time communication.
- **Pandas**: Data manipulation and CSV handling.
- **JWT**: Token-based authentication.
- **Pydantic**: Data validation and settings management.

---

## Development Notes

1. **Environment Variables**:
   Ensure required environment variables (e.g., database URLs, secret keys) are set up.

2. **CORS Configuration**:
   The application is configured to allow requests from the following origins:
   - `https://blackrose-frontend.pages.dev`
   - `http://localhost:3000`

3. **Database**:
   Data is stored in `backend_table.csv` with automatic backups to `backend_table_backup.csv`.

4. **Socket.IO**:
   Real-time data is streamed using Socket.IO. Ensure the server and client are properly configured.

---

