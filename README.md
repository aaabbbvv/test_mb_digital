### Project Setup

To set up and run the project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure that Docker Compose is installed.
3. Start the application by running the following command:

```bash
docker compose up -d
```
after  this actions you could open admin part by 
```bash
http://0.0.0.0:8000/admin 
```
use default credentioanals from default.env file
```bash
DEFAULT_ADMIN_EMAIL=admin@admin.com
DEFAULT_ADMIN_PASSWORD=qwerty123456!
```
####Access the API documentation via Swagger or Redoc:

- Swagger: [http://0.0.0.0:8000/api/v0/swagger/](http://0.0.0.0:8000/api/v0/swagger/)
- Redoc: [http://0.0.0.0:8000/api/v0/redoc/](http://0.0.0.0:8000/api/v0/redoc/)

The documentation includes:
- JWT authentication setup
- CRUD operations for the `User` and `Group` models
- Endpoints for adding and removing users from groups

To modify user group memberships, use the following endpoint:

```bash
POST http://0.0.0.0:8000/api/v0/membership-change/
```