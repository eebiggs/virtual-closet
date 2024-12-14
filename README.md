# Virtual Closet

## Overview
The **Virtual Closet** app is a microservices-based application designed to help users manage their wardrobe. It allows users to log in, register, and keep track of their clothing items with details such as name, category, color, and season. The app also provides analytics on item usage and inventory.

---

## Features
- **User Authentication**: Register and log in securely to manage your personalized closet.
- **Manage Items**: Add, update, delete, and view clothing items.
- **Analytics**: Get insights into your closet, such as the number of items and activity history.
- **Microservices Architecture**: Includes separate services for authentication, item management, and analytics.

---

## Tech Stack
The Virtual Closet app is built with:

- **Frontend**:
  - [Svelte](https://svelte.dev)
  - Hosted on port `8080`.

- **Backend**:
  - Python Flask-based microservices:
    - **Auth Service**: Handles user authentication (port `5001`).
    - **Closet Service**: Manages closet item data (port `5000`).
    - **Analytics Service**: Tracks user actions and generates analytics (port `5003`).
  - **Gateway Service**: Acts as a single entry point for all backend services (port `5005`).

- **Database**:
  - PostgreSQL for persistent storage.

- **Containerization**:
  - Docker Compose and DigitalOcean

---

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eebiggs/virtual-closet.git
   cd virtual-closet
   ```

2. **Start the Services**:
   Use Docker Compose to build and run the app:
   ```bash
   docker-compose up --build
   ```

3. **Access the App**:
   - Frontend: [http://localhost:8080](http://localhost:8080)
   - Backend Gateway: [http://localhost:5005](http://localhost:5005)

---

## Environment Variables
The app uses environment variables for configuration. You can set them in a `.env` file or directly in `docker-compose.yml`.

### Example `.env`:
```env
DATABASE_URL=postgresql://postgres:password@db:5432/virtual_closet_db
AUTH_SERVICE_URL=http://auth_service:5001
CLOSET_SERVICE_URL=http://closet_service:5000
ANALYTICS_SERVICE_URL=http://analytics_service:5003
```

---

## API Endpoints
The app uses RESTful APIs exposed via the Gateway Service.

### Auth Endpoints:
- `POST /register`: Register a new user.
- `POST /login`: Log in an existing user.

### Closet Endpoints:
- `GET /items`: Get all items for a user.
- `POST /items`: Add a new item.
- `PUT /items/<item_id>`: Update an existing item.
- `DELETE /items/<item_id>`: Delete an item.

### Analytics Endpoints:
- `GET /analytics`: Get analytics for a user.

---

## Known Issues
- Currently deployed locally. Frontend cannot communicate with backend via Docker. Bugs still exist

---

## Future Work
- Add support for image uploads for clothing items.
- Enhance analytics with detailed category and usage breakdowns.
- Implement container orchestration (e.g., Kubernetes).
