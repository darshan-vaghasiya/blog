# Django Blog Project

A Django-based blog platform with features like post creation, comments, likes, user registration, and statistics generation. This project uses Docker, Celery for asynchronous tasks, and Redis as a message broker.

## Features

- **User Authentication**: Registration, login, and role-based access.
- **Post Management**: CRUD operations for posts.
- **Comments**: Users can add comments to posts.
- **Likes**: Users can like/unlike posts.
- **Post Statistics**: Daily statistics for posts (like views, likes, and comments).
- **Rate Limiting**: Apply API rate limits to endpoints.
- **Asynchronous Tasks**: Using Celery to send welcome emails and generate post statistics.

## Technologies

- Django 4.2
- Django REST Framework
- Celery (for async tasks)
- Redis (message broker for Celery)
- PostgreSQL (database)
- Docker (containerization)

## Setup

### Prerequisites

- Docker and Docker Compose installed
- Python 3.9 or above (for local development)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/your-project-name.git
   cd your-project-name
   
2. **Create .env file**:
    ```
   touch .env
   
and set database configurations.
   
3. **Build the Docker containers**:
    ```
   docker-compose build
   
4. **Run the containers:**:
    ```
   docker-compose up

5. **Run migrations**:
    ```
    docker-compose exec web bash
    python manage.py migrate


