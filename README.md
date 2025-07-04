# Codemonk Backend Intern Assignment

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)  
[![Django](https://img.shields.io/badge/django-4.x-green)](https://www.djangoproject.com/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  

## Project Description

This project is a RESTful API built using Django Rest Framework and PostgreSQL. It enables users to submit multiple paragraphs of text, indexes the words within those paragraphs, and provides a search API to retrieve paragraphs containing a specified word. The API supports user authentication and is containerized using Docker for easy deployment.

## Project Structure

```
codemonk_backend/               # Root directory
├── api/                        # Django app (named "api")
│   ├── migrations/             # Django migrations
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # User, Paragraph, WordIndex models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # All API views (Register, Login, paragraphs, Search)
│   ├── urls.py                 # App-specific URL patterns
│   └── tests.py                # Unit tests
│
├── codemonk_backend/           # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Database, Installed apps, JWT config
│   ├── urls.py                 # Project-level URL config
│   └── wsgi.py
│
├── .env                       # Environment variables (e.g. DB, SECRET_KEY)
├── Dockerfile                 # Docker config for app container
├── docker-compose.yml         # Compose PostgreSQL + app services
├── manage.py                  # Django CLI
├── requirements.txt           # Python dependencies
└── README.md
```

## Features

- Custom user model with authentication  
- Submit multiple paragraphs of text  
- Tokenize and index words to paragraphs  
- Search API to find top 10 paragraphs containing a word  
- PostgreSQL database backend  
- Docker and Docker Compose setup for containerized deployment  
- Swagger API documentation for easy API exploration  

## Tech Stack

- Python 3  
- Django 4.x  
- Django Rest Framework  
- PostgreSQL  
- Docker & Docker Compose  

## Prerequisites

- Docker and Docker Compose installed and available in your system PATH  
- Alternatively, Python 3 and PostgreSQL installed locally if not using Docker  

## Setup and Run

1. Clone the repository:

```bash
git clone <repository-url>
cd codemonk
```

2. Build and run the Docker containers:

```bash
docker-compose up --build
```

3. The API will be available at: `http://localhost:8000/`

4. Access Swagger API documentation at: `http://localhost:8000/swagger/`

## API Endpoints

| Endpoint              | Method | Description                                         |
|-----------------------|--------|-----------------------------------------------------|
| `/api/register/`      | POST   | Register a new user                                 |
| `/api/login/`         | POST   | Authenticate and receive JWT tokens                 |
| `/api/paragraphs/`    | POST   | Upload text containing multiple paragraphs          |
| `/api/search/?word=`  | GET    | Retrieve top 10 paragraphs containing the word      |



## 📸 API Testing with Postman


1. Register a new user

<img width="1440" alt="Screenshot 2025-07-05 at 00 37 55" src="https://github.com/user-attachments/assets/bf7cc768-f98c-4593-a71c-8640ad3fffba" />

2. login to obtain an authentication token
  
<img width="1440" alt="Screenshot 2025-07-05 at 00 40 52" src="https://github.com/user-attachments/assets/860a860a-19bd-46db-a0c0-a71344f6da9f" />


3. Submit text paragraphs via the endpoint:

```
[POST /api/paragraphs/](http://localhost:8000/api/paragraphs/)
```
<img width="1440" alt="Screenshot 2025-07-05 at 00 42 07" src="https://github.com/user-attachments/assets/ffcbd9f4-fee8-455c-9685-b2633785e0b8" />



4. Search for paragraphs containing a specific word via the endpoint:

```
[GET /api/search/?word=Maecenas] (http://localhost:8000/api/search/?word= Maecenas)
```
<img width="1440" alt="Screenshot 2025-07-05 at 00 43 47" src="https://github.com/user-attachments/assets/141ee6cd-dd90-43f6-bfa2-e11c49fe6506" />

```
[[GET /api/search/?word=lorem] (http://localhost:8000/api/search/?word= lorem)]
```
<img width="1440" alt="Screenshot 2025-07-05 at 00 46 33" src="https://github.com/user-attachments/assets/8235287f-1806-482b-86ac-a8c6eef2d711" />


## Testing

This project includes comprehensive automated tests covering key API endpoints and functionality.

### Tests Included

- User registration and login
- Paragraph submission with multiple paragraphs
- Paragraph submission with special text content (e.g., containing "txt")
- Search API for single word queries (case insensitive)
- Authentication enforcement on protected endpoints
- Error handling for missing or invalid input parameters

### Running Tests

To run the automated tests, ensure your environment is set up and dependencies installed. Then run:

```bash
python manage.py test
```

or if using Docker:

```bash
docker-compose run web python manage.py test
```

### Additional Testing Recommendations

- **Performance Testing:** Use the provided `performance_test.sh` script to simulate load on the search endpoint. This helps verify the API's responsiveness under concurrent requests.

- **Security Testing:** Follow the instructions in `security_test_instructions.md` to perform vulnerability scans using tools like OWASP ZAP. Focus on authentication, input validation, and common web vulnerabilities.

- **Docker Deployment Testing:** If Docker is installed, build and run the containers using:

```bash
docker-compose build
docker-compose up -d
```

Verify the services are running and accessible.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Push your branch and open a pull request describing your changes.

Please ensure your code follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

## Code Style

This project follows the Google Python Style Guide.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
