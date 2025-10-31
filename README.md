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


