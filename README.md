**URL Shortener Application**

A Django-based URL shortener application that allows users to create shortened URLs with optional password protection and expiration settings. The application also provides analytics for access logs.

**Features**

* Generate shortened URLs for long URLs.
* Set expiration times for shortened URLs (default is 24 hours).
* Optional password protection for accessing shortened URLs.
* Track access logs, including timestamps and IP addresses.
* Analytics endpoint to view usage statistics and access logs.

**Requirements**

Python 3.9+

Django 4.0+

Django REST Framework (DRF)

**Setup Instructions**
1. Clone the Repository
  $ git clone <repository-url>
  $ cd <repository-folder>

2. Set Up a Virtual Environment
   
   $ python -m venv venv
   $ source venv/bin/activate

4. Install Dependencies
   
   $ pip install -r requirements.txt

5. Apply Migrations
   
   $ python manage.py migrate

7. Run the Development Server
   
   $ python manage.py runserver

**API Endpoints**

Endpoint: POST /post-shorten/

payload:
  {
  "original_url": "https://google.com",
  "expiry_hours": 24,        // Optional, defaults to 24 hours
  "password": "123"   // Optional
  }

  
Response:
  {
  "id": 1,
  "original_url": "https://google.com",
  "short_url": "a2f7d",
  "created_at": "2024-01-01T12:00:00Z",
  "expires_at": "2024-01-02T12:00:00Z",
  "access_count": 0
}

**Redirect to Original URL**

Endpoint: GET /<short_url>/

Optional Query Parameter:

password: If the shortened URL is password-protected.
Response: Redirects to the original URL.

**Analytics for a Shortened URL**

Endpoint: GET /analytics/<short_url>/

Response:
  [
  {
    "id": 1,
    "short_url": "a2f7d",
    "access_count": 2,
    "access_log": [
    {
        "id": 1,
        "timestamp": "2024-01-01T13:00:00Z",
        "ip_address": "127.0.0.1"
      },
      {
        "id": 2,
        "timestamp": "2024-01-01T14:00:00Z",
        "ip_address": "127.0.0.1"
      }
    ]
  }
]
