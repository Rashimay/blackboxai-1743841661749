# Attendance Monitoring System

A mobile-based attendance tracking system with QR code scanning and photo proof capabilities.

## Features

- Role-based authentication (Admin, Instructor, Student)
- QR code generation for lectures
- QR code scanning for attendance
- Photo proof capture
- Dashboard for each user role
- Attendance tracking and reporting

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```bash
   flask run
   ```

## Usage

1. Access the application at `http://localhost:5000`
2. Register accounts for different roles
3. As an instructor:
   - Create lectures
   - Generate QR codes for attendance
4. As a student:
   - Scan QR codes to mark attendance
   - Upload photo proof

## Configuration

Edit `.env` file for:
- Database configuration
- Secret key
- Upload folders