# 🔌 API Documentation - AI-Powered Voice-Based Solution for Auto Retailers

This document provides comprehensive API documentation for the AI-powered voice-based auto retail solution, with special focus on the innovative voice assistant and AI-driven features.

## 📋 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URLs](#base-urls)
- [Car Management API](#car-management-api)
- [User Authentication API](#user-authentication-api)
- [Contact Management API](#contact-management-api)
- [Voice Assistant API](#voice-assistant-api)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## 🌐 Overview

The AI-Powered Voice-Based Auto Retail API provides RESTful endpoints with cutting-edge AI integration for managing cars, users, contacts, and advanced voice assistant interactions. This innovative solution revolutionizes how auto retailers interact with customers through artificial intelligence and voice technology.

### API Version
- **Current Version**: v1
- **Base URL**: `http://localhost:8000/api/v1/` (development)
- **Content Type**: `application/json`
- **Character Encoding**: UTF-8

## 🔐 Authentication

### Authentication Methods

1. **Session Authentication** (Web Interface)
2. **Token Authentication** (API Access)
3. **Django Admin Authentication** (Admin Panel)

### Session Authentication
Used for web interface interactions. Login through the web form creates a session.

```http
POST /accounts/login/
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

### Token Authentication
For API access, you can implement token-based authentication:

```http
Authorization: Token your_api_token_here
```

## 🌍 Base URLs

### Development
```
http://localhost:8000/
```

### Production
```
https://yourdomain.com/
```

## 🚗 Car Management API

### List All Cars
Retrieve a list of all available cars with optional filtering.

```http
GET /cars/
GET /cars/?search=toyota
GET /cars/?min_price=10000&max_price=50000
GET /cars/?year=2020
GET /cars/?transmission=automatic
```

**Query Parameters:**
- `search` (string): Search by car title, make, or model
- `min_price` (integer): Minimum price filter
- `max_price` (integer): Maximum price filter  
- `year` (integer): Filter by year
- `transmission` (string): Filter by transmission type
- `fuel_type` (string): Filter by fuel type
- `body_style` (string): Filter by body style

**Response:**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "car_title": "Toyota Camry 2020",
      "make": "Toyota",
      "model": "Camry",
      "year": 2020,
      "price": 25000,
      "description": "Well maintained Toyota Camry...",
      "transmission": "Automatic",
      "fuel_type": "Petrol",
      "mileage": 15000,
      "engine": "2.5L",
      "body_style": "Sedan",
      "exterior_color": "White",
      "interior_color": "Black",
      "car_photo": "/media/photos/2022/06/04/camry.jpg",
      "car_photo_1": "/media/photos/2022/06/04/camry1.jpg",
      "features": ["Air Conditioning", "Power Steering", "ABS"],
      "is_featured": true,
      "created_date": "2022-06-04T10:30:00Z"
    }
  ]
}
```

### Get Car Details
Retrieve detailed information about a specific car.

```http
GET /cars/{id}/
```

**Response:**
```json
{
  "id": 1,
  "car_title": "Toyota Camry 2020",
  "make": "Toyota",
  "model": "Camry",
  "year": 2020,
  "price": 25000,
  "description": "Well maintained Toyota Camry with full service history...",
  "transmission": "Automatic",
  "fuel_type": "Petrol",
  "mileage": 15000,
  "engine": "2.5L",
  "body_style": "Sedan",
  "exterior_color": "White",
  "interior_color": "Black",
  "car_photo": "/media/photos/2022/06/04/camry.jpg",
  "car_photo_1": "/media/photos/2022/06/04/camry1.jpg",
  "car_photo_2": "/media/photos/2022/06/04/camry2.jpg",
  "car_photo_3": "/media/photos/2022/06/04/camry3.jpg",
  "car_photo_4": "/media/photos/2022/06/04/camry4.jpg",
  "features": ["Air Conditioning", "Power Steering", "ABS", "Airbags"],
  "is_featured": true,
  "created_date": "2022-06-04T10:30:00Z"
}
```

### Search Cars
Advanced search functionality with multiple filters.

```http
POST /cars/search/
Content-Type: application/json

{
  "search": "toyota",
  "min_price": 10000,
  "max_price": 50000,
  "year_min": 2018,
  "year_max": 2022,
  "transmission": "automatic",
  "fuel_type": "petrol",
  "features": ["air_conditioning", "power_steering"]
}
```

## 👤 User Authentication API

### User Registration
Register a new user account.

```http
POST /accounts/register/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secure_password123",
  "password2": "secure_password123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "user_id": 123
}
```

### User Login
Authenticate user and create session.

```http
POST /accounts/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "user": {
    "id": 123,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### User Dashboard
Get user dashboard information (requires authentication).

```http
GET /accounts/dashboard/
Authorization: Session
```

**Response:**
```json
{
  "user": {
    "id": 123,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2022-06-01T00:00:00Z"
  },
  "inquiries": 5,
  "favorite_cars": 3
}
```

## 📞 Contact Management API

### Submit Contact Inquiry
Submit a contact inquiry about a car.

```http
POST /contact/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "car_id": 1,
  "customer_need": "I'm interested in this car",
  "car_title": "Toyota Camry 2020",
  "city": "New York",
  "state": "NY",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "I would like to schedule a test drive."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Your inquiry has been submitted successfully",
  "inquiry_id": 456
}
```

## 🎤 Voice Assistant API

### Start Voice Session
Initialize a new voice assistant session.

```http
POST /voice-assistant/start-session/
Content-Type: application/json

{
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

**Response:**
```json
{
  "session_id": "sess_123456789",
  "status": "active",
  "created_at": "2022-06-04T15:00:00Z"
}
```

### Process Voice Query
Send voice query to the assistant.

```http
POST /voice-assistant/query/
Content-Type: application/json

{
  "session_id": "sess_123456789",
  "query": "Show me Toyota cars under $30000",
  "query_type": "car_search"
}
```

**Response:**
```json
{
  "response": "I found 5 Toyota cars under $30,000. Here are the results:",
  "cars": [
    {
      "id": 1,
      "car_title": "Toyota Corolla 2021",
      "price": 22000,
      "make": "Toyota",
      "model": "Corolla"
    }
  ],
  "response_type": "car_results"
}
```

## ⚠️ Error Handling

### Standard Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided data is invalid",
    "details": {
      "email": ["This field is required"],
      "password": ["Password must be at least 8 characters"]
    }
  },
  "status": "error"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Common Error Codes

- `VALIDATION_ERROR` - Input validation failed
- `AUTHENTICATION_REQUIRED` - User must be logged in
- `PERMISSION_DENIED` - Insufficient permissions
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `DUPLICATE_ENTRY` - Resource already exists
- `RATE_LIMIT_EXCEEDED` - Too many requests

## 🚦 Rate Limiting

### Default Limits
- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Admin users**: 5000 requests per hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 📊 Response Formats

### Pagination
Large result sets are paginated:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/cars/?page=2",
  "previous": null,
  "results": [...]
}
```

### Date Formats
All dates are in ISO 8601 format:
```
2022-06-04T15:30:00Z
```

## 🛠️ SDK and Integration

### JavaScript Example
```javascript
// Fetch cars
fetch('/cars/')
  .then(response => response.json())
  .then(data => console.log(data));

// Submit contact form
fetch('/contact/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    email: 'john@example.com',
    message: 'Interested in this car'
  })
});
```

### Python Example
```python
import requests

# Get cars
response = requests.get('http://localhost:8000/cars/')
cars = response.json()

# Submit inquiry
data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john@example.com',
    'message': 'Interested in this car'
}
response = requests.post('http://localhost:8000/contact/', json=data)
```

## 🔧 Testing the API

### Using cURL
```bash
# Get all cars
curl -X GET http://localhost:8000/cars/

# Search cars
curl -X GET "http://localhost:8000/cars/?search=toyota&min_price=20000"

# Submit contact form
curl -X POST http://localhost:8000/contact/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'
```

### Using Postman
1. Import the API collection (if available)
2. Set base URL to `http://localhost:8000`
3. Configure authentication if needed
4. Test endpoints with sample data

---

**API Support**: For API questions and issues, please refer to the main documentation or create an issue in the repository. 