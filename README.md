# User Profile Management System

## Overview
This Django-based project provides a system for managing user profiles, authentication, and a user dashboard. It includes secure user authentication, session management, and customizable dashboards for each user.

## Features
- **User Authentication**: Secure login and registration system using Django's authentication framework.
- **User Profiles**: Ability for users to view, update, and manage their profiles.
- **Dashboard**: Personalized user dashboards with customizable features.
- **API Integration**: Provides RESTful APIs to integrate user management with front-end or external systems.
- **Session Management**: Secure session handling to ensure user data privacy and safety.
  
## Tech Stack
- **Backend**: Django
- **Database**: MySQL
- **APIs**: Django REST Framework

## Prerequisites
- Python 3.7 or higher
- Django 3.2 or higher
- MySQL

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/himanshu-sharmav/user_profile_management.git
   cd user_dashboard
   ```

2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database in `settings.py` by configuring the database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_db_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Token and Credential Files
This project uses OAuth2 for Google APIs.

### Generating Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and navigate to the **Credentials** section.
3. Create OAuth 2.0 credentials and download the `credentials.json` file.
4. Move the `credentials.json` file into the project directory.

### Generating `token.json`
After placing `credentials.json` in your project directory, run the application, which will guide you through OAuth authorization and automatically generate a `token.json` file. Keep these files **private** and **out of version control** by adding them to `.gitignore`.

## REST API Documentation
This project also provides RESTful APIs for user management. Below is a sample of available endpoints:

### API Endpoints
- **POST /api/register**: Register a new user.
- **POST /api/login**: Authenticate a user.
- **GET /api/user/{id}**: Retrieve a user's profile.
- **PUT /api/user/{id}**: Update user information.

## Authors
- Himanshu Sharma

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```

---
