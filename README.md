# Event Management System API

This Django application provides a RESTful API for managing events. Users can create events, RSVP to events, and leave reviews. The system supports authentication with JWT tokens, custom permissions restricting event modifications to organizers, and controls access to private events through invitations. It also includes pagination and search features on event and review listings.

## Features

- User registration and authentication (JWT).
- CRUD operations on events (only organizers can update or delete).
- RSVP to events with status: Going, Maybe, Not Going.
- Leave reviews with rating and comments on events.
- Event visibility control with public and private events.
- Pagination and search/filter support.
- Unit tests to verify API correctness.

## Setup and Run

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository** (or download files to your local machine):

   ```
   git clone https://github.com/rishee10/Event-Management.git
   ```

   ```
   cd Event-Management
   ```


2. **Create and activate a virtual environment**:

   ```
   python -m venv venv
   ```

   ***Activate on Windows***
   ```
   venv\Scripts\activate
   ```

    ***Activate on macOS/Linux***

    ```
    source venv/bin/activate
    ```

3. **Download Dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Run Makemigrations and migrate command**

   ```
   python manage.py makemigrations
   ```

   ```
   python manage.py migrate
   ```
5. **Run Server**

   ```
   python manage.py runserver
   ```

6. **Run the test cases**

   ```
   python manage.py test Event
   ```

## API Endpoints:

**Event API:**

```POST /events/``` : Create a new event (authenticated users only).

```GET /events/``` : List all public events (with pagination).

```GET /events/{id}/``` : Get details of a specific event.

```PUT /events/{id}/``` : Update an event (only the organizer can edit).

```DELETE /events/{id}/``` : Delete an event (only the organizer).

**RSVP API:**

```POST /events/{event_id}/rsvp/``` : RSVP to an event.

```PATCH /events/{event_id}/rsvp/{user_id}/``` : Update RSVP status.

**Review API:**

```POST /events/{event_id}/reviews/``` : Add a review for an event.

```GET /events/{event_id}/reviews/``` : List all reviews for an event.
   


