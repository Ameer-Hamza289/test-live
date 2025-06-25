# 📦 Installation Guide - AI-Powered Voice-Based Solution for Auto Retailers

This guide provides detailed installation instructions for the AI-powered voice-based auto retail solution, including setup of the innovative voice assistant and AI features.

## 📋 Prerequisites

Before installing the application, ensure you have the following installed on your system:

### System Requirements
- **Python**: Version 3.8 or higher
- **pip**: Python package installer (usually comes with Python)
- **Git**: Version control system
- **Web Browser**: Modern browser supporting HTML5 and JavaScript

### Optional Requirements
- **PostgreSQL**: For production database (SQLite is used for development)
- **Redis**: For caching (optional)
- **Nginx/Apache**: For production deployment

## 🔧 Step-by-Step Installation

### 1. Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>
cd CarDealerWeb-Django

# Or download and extract the ZIP file
# Then navigate to the extracted folder
```

### 2. Set Up Python Virtual Environment

**Windows:**
```cmd
# Create virtual environment
python -m venv myenv

# Activate virtual environment
myenv\Scripts\activate

# Verify activation (should show path to myenv)
where python
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv myenv

# Activate virtual environment
source myenv/bin/activate

# Verify activation (should show path to myenv)
which python
```

### 3. Install Python Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Environment Configuration

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env  # On Windows: type nul > .env
```

Add the following content to `.env`:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-very-secret-key-here-change-this-in-production

# Database Configuration (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (for contact forms and user registration)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Media and Static Files
MEDIA_URL=/media/
STATIC_URL=/static/

# Voice Assistant Settings
VOICE_ASSISTANT_ENABLED=True
```

### 5. Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate

# Create a superuser account for admin access
python manage.py createsuperuser
# Follow the prompts to create username, email, and password
```

### 6. Load Initial Data (Optional)

If you have fixture data or want to load sample data:

```bash
# Load sample data (if available)
python manage.py loaddata project_dump.json

# Or create sample cars manually through admin panel
```

### 7. Collect Static Files

```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

### 8. Test the Installation

```bash
# Run the development server
python manage.py runserver

# The server will start at: http://127.0.0.1:8000
```

Open your web browser and navigate to:
- **Main Site**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## 🗂️ Directory Structure After Installation

```
CarDealerWeb-Django/
├── myenv/                   # Virtual environment (created)
├── db.sqlite3              # Database file (created)
├── .env                    # Environment variables (created)
├── static_collected/       # Collected static files (created)
├── media/                  # User uploaded files
├── accounts/               # User authentication app
├── cars/                   # Car management app
├── contacts/              # Contact management app
├── pages/                 # Static pages app
├── voice_assistant/       # Voice assistant app
├── cardealer/            # Main project settings
├── templates/            # HTML templates
└── manage.py            # Django management script
```

## 🔐 Security Configuration

### Development Environment
- Keep `DEBUG=True` in development
- Use SQLite for development database
- Email backend can be console-based for testing

### Production Environment
- Set `DEBUG=False`
- Use PostgreSQL or MySQL
- Configure proper email backend
- Set up HTTPS
- Configure allowed hosts

## 🌐 Database Configuration Options

### SQLite (Default - Development)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cardealer_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📧 Email Configuration

### Gmail SMTP Configuration
1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password
3. Use the app password in `EMAIL_HOST_PASSWORD`

### Other Email Providers
Update the email settings in `.env` according to your email provider's documentation.

## 🎤 Voice Assistant Setup

The voice assistant uses Web Speech API which requires:
- HTTPS connection (for production)
- Modern browser with microphone access
- Proper SSL certificates

## 🚀 Running in Different Modes

### Development Mode
```bash
python manage.py runserver
```

### Production Mode
```bash
# Set DEBUG=False in .env
# Configure proper database
# Set up web server (Nginx/Apache)
# Use WSGI server like Gunicorn
```

## 🔧 Troubleshooting Installation

### Common Issues

1. **Python/pip not found**
   - Ensure Python is installed and added to PATH
   - Use `python3` and `pip3` on some systems

2. **Permission errors**
   - Use virtual environment
   - On Linux/Mac, you might need `sudo` for system-wide installs

3. **Dependencies not installing**
   - Update pip: `pip install --upgrade pip`
   - Clear pip cache: `pip cache purge`

4. **Database migration errors**
   - Delete `db.sqlite3` and migration files (keep `__init__.py`)
   - Re-run `makemigrations` and `migrate`

5. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings

### Getting Help

If you encounter issues:
1. Check the error message carefully
2. Refer to the [Troubleshooting Guide](TROUBLESHOOTING.md)
3. Search for similar issues online
4. Check Django documentation
5. Create an issue in the project repository

## ✅ Verification Checklist

After installation, verify that:

- [ ] Virtual environment is activated
- [ ] All dependencies are installed
- [ ] Database migrations are applied
- [ ] Superuser account is created
- [ ] Development server starts without errors
- [ ] Admin panel is accessible
- [ ] Static files are loading properly
- [ ] Voice assistant permissions work (microphone access)

## 🔄 Next Steps

After successful installation:
1. Read the [User Guide](USER_GUIDE.md)
2. Check the [API Documentation](API.md)
3. Configure your first car listings
4. Test all features including voice assistant
5. Customize the application for your needs

---

**Installation Support**: If you need help with installation, please refer to the troubleshooting guide or create an issue in the repository. 