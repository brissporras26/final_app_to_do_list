<!-- setup.md -->
# Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- MongoDB
- virtualenv (recommended)

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd todo-app
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure MongoDB
```bash
# Make sure MongoDB is running locally
# Default connection string: mongodb://localhost:27017/test_db
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
FLASK_APP=app
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/todo_app
SECRET_KEY=your-secret-key
```

### MongoDB Setup

1. Start MongoDB service
2. Create database and collections
3. Set up indexes (if required)

---