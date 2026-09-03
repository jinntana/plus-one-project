# NC Plus One

NC Plus One is a backend API for a small event RSVP platform.

Users can register, log in, browse events, RSVP to events, cancel their RSVP, create events, update events they organise, view attendee lists, and see basic event statistics.

I built this project as part of my move into backend and data engineering. The aim was to build a realistic API with authentication, protected routes, database relationships, repeatable seed data, integration tests, and SQL queries that do more than basic CRUD.

## Why I built this

I wanted a project that showed more than just simple endpoints.

This project gave me a chance to practise building an API around real relationships:

- users can organise events
- users can RSVP to events
- organisers can manage their own events
- organisers can view attendee lists
- reporting endpoints can use SQL joins, aggregates and window functions

It also helped me practise handling the parts that usually matter in real backend work: authentication, password hashing, permissions, error handling, testing, and database reset scripts.

## What problem it solves

NC Plus One gives a basic backend structure for managing events and RSVPs.

It could be used as the API behind a simple meetup, community event, networking, or internal company event platform. The frontend could use this API to let users sign up, log in, browse events, RSVP, cancel attendance, and let organisers manage their own events.

## Features

- Register a new user
- Log in and receive a JWT
- Store passwords using bcrypt hashing
- View all events
- View a single event with venue details
- Create a new event as the logged-in user
- Update an event only if you are the organiser
- RSVP to an event
- Cancel your own RSVP
- View attendees for an event you organise
- View events you have RSVP’d to
- View organiser statistics
- Return clear HTTP status codes for common errors

## Tech stack

- Python
- FastAPI
- PostgreSQL
- Pytest
- bcrypt
- JWT
- python-dotenv
- Uvicorn
- Terraform
- AWS EC2 deployment preparation

## Project structure

```text
.
├── db
│   ├── connection.py
│   ├── credentials.py
│   ├── data
│   ├── schema.sql
│   ├── seed.py
│   └── setup.sql
├── main.py
├── requirements.txt
├── tests
│   └── test_main.py
└── terraform