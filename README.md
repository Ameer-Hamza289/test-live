# 🚗 AI-Powered Voice-Based Solution for Auto Retailers

An innovative Django-based application that revolutionizes the auto retail industry through artificial intelligence and voice interaction technology. This comprehensive solution enables auto retailers to provide customers with voice-controlled car search, intelligent recommendations, and seamless browsing experiences.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Features
- **Car Inventory Management**: Complete CRUD operations for car listings
- **Advanced Search & Filtering**: Search cars by make, model, year, price range, and features
- **User Authentication**: Registration, login, password reset, and user dashboard
- **Admin Panel**: Django admin interface for managing cars, users, and contacts
- **Responsive Design**: Mobile-friendly interface using Bootstrap

### AI-Powered Voice Features (Core Innovation)
- **Intelligent Voice Assistant**: Advanced AI-driven voice interaction for auto retail
- **Natural Language Processing**: Understands customer intent and preferences
- **Smart Car Recommendations**: AI-powered suggestions based on voice queries
- **Voice-Guided Navigation**: Hands-free browsing experience
- **Conversational Commerce**: Voice-based car inquiry and information retrieval
- **Speech Analytics**: Call session tracking and customer behavior analysis

### Supporting Features
- **Image Gallery**: Multiple car images with lightbox gallery
- **Contact Management**: Inquiry system with email notifications
- **Dynamic Filtering**: Real-time car filtering with AJAX
- **SEO Optimized**: Clean URLs and meta tags

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django built-in authentication system
- **Media Storage**: Local file system with Pillow for image processing

### Frontend
- **CSS Framework**: Bootstrap 4
- **JavaScript Libraries**: 
  - jQuery
  - Slick Carousel
  - Lightbox
  - Bootstrap Select
- **Icons**: Font Awesome, Flaticon
- **Animations**: Animate.css

### AI/Voice Technology Stack (Core Innovation)
- **Speech Recognition**: Web Speech API for voice input processing
- **Natural Language Processing**: Custom RAG (Retrieval-Augmented Generation) engine
- **Voice Synthesis**: Web Speech Synthesis API for audio responses
- **Machine Learning**: AI algorithms for intelligent car recommendations
- **Conversational AI**: Advanced dialogue management for auto retail scenarios

## 📁 Project Structure

```
CarDealerWeb-Django/
├── accounts/                 # User authentication and management
├── cars/                    # Car inventory management
├── contacts/               # Contact and inquiry system
├── pages/                  # Static pages (home, about, services)
├── voice_assistant/        # AI voice assistant functionality
├── cardealer/             # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── static/           # Static assets (CSS, JS, images)
├── templates/            # HTML templates
├── media/               # User uploaded files
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CarDealerWeb-Django
   ```

2. **Create virtual environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

## 📱 Usage

### For Customers
1. **Browse Cars**: View available cars with detailed information
2. **Search & Filter**: Use advanced search to find specific cars
3. **Voice Assistant**: Use voice commands to search for cars
4. **Contact Dealer**: Submit inquiries through contact forms
5. **User Account**: Register to save favorites and track inquiries

### For Administrators
1. **Admin Panel**: Access at `/admin` with superuser credentials
2. **Manage Cars**: Add, edit, or remove car listings
3. **User Management**: View and manage user accounts
4. **Contact Management**: Review and respond to customer inquiries
5. **Voice Assistant Analytics**: Monitor voice assistant usage and feedback

## 🎯 Key Functionalities

### Car Search & Filtering
- Search by keywords (make, model, etc.)
- Filter by price range, year, transmission type
- Advanced filtering by car features
- Sort by price, year, or date added

### AI-Powered Voice Solution
- **Voice-Activated Intelligence**: Hands-free car search and browsing
- **Natural Language Understanding**: Advanced query processing for auto retail
- **Intelligent Recommendations**: AI-driven car suggestions based on voice input
- **Conversational Interface**: Natural dialogue for customer inquiries
- **Voice Analytics**: Comprehensive tracking and analysis of voice interactions
- **Auto Retailer Dashboard**: Voice interaction insights and customer behavior data

### User Management
- User registration with email verification
- Password reset functionality
- User dashboard with inquiry history
- Profile management

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Static Files Configuration
Static files are served from `cardealer/static/` directory during development.
For production, configure your web server to serve static files.

## 📚 Additional Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- [API Documentation](docs/API.md) - REST API endpoints and usage
- [User Manual](docs/USER_GUIDE.md) - Complete user guide
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Email: [your-email@example.com]
- Documentation: Check the `docs/` folder

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Final Year Project (FYP) Status

**Topic**: "AI-powered voice-based solution for auto retailers"

This project demonstrates cutting-edge technology integration:
- **Artificial Intelligence**: Advanced NLP and machine learning for auto retail
- **Voice Technology**: Speech recognition and synthesis for hands-free interaction
- **Full-stack Development**: Comprehensive Django web application
- **Industry Innovation**: Revolutionary approach to auto retail customer experience
- **Software Engineering**: Professional development practices and architecture

### Academic Contribution
- **Novel Solution**: First-of-its-kind voice-powered auto retail platform
- **AI Integration**: Practical application of conversational AI in automotive industry
- **User Experience Innovation**: Redefining how customers interact with auto retailers
- **Technical Excellence**: Demonstrates mastery of modern web technologies

---

**Final Year Project (FYP)**  
*AI-Powered Voice-Based Solution for Auto Retailers*  
**Innovation in Automotive Technology and Customer Experience** 