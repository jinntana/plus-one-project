# Portfolio - NC Plus One

<br/>

# 01 - Project Setup

**Goal:** Create your own copy of the project repository, clone it locally, and add a README.

## Steps

**1. Create your repository**

Navigate to the provided template repository. 

[Template Repository](https://github.com/northcoders/py-nc-plus-one)

Click **Use this template** and select **Create a new repository**.

When configuring the new repository:
- Set yourself as the owner
- Set the visibility to **Public** - this project will form part of your portfolio

> Do not fork the repository. Use the template button only.

**2. Clone the repository**

Once your repository has been created, clone it to your local machine:

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

**3. Add a README**

Create or update `README.md` at the root of the project. It should briefly describe what the project is — what it does and what technologies it uses. This is the first thing a prospective employer will read.

Commit and push the README before moving on to the next ticket:

```bash
git add README.md
git commit -m "Add project README"
git push
```

## Acceptance criteria
- Your repository is public and listed under your own GitHub account
- The repository was created from the template, not forked
- A README exists at the root of the project and has been pushed


---
<br/><br/>


# 02 - Create the Database

**Goal:** Create a local PostgreSQL database and a SQL script that can reliably recreate it from scratch.

## Requirements

- Create a local database named `nc_plus_one`
- Create a SQL script at `db/setup.sql` that drops and recreates the database — this allows any developer to get a clean setup with a single command
- Update the README with a **Database Setup** section explaining how to run the script

## Acceptance criteria
- `nc_plus_one` database exists locally and can be connected to
- `db/setup.sql` exists and contains the drop and create statements
- The README documents how to run `db/setup.sql`


---
<br/><br/>


# 03 - Create the Seed Function

**Goal:** Create a `seed` function that will be responsible for resetting the database to a known initial state.

## Background

Production databases change constantly as users interact with them. For testing purposes, we need a database that is predictable - one we can reset to a fixed starting point before each test run so that expected outcomes are always consistent.

The `seed` function is responsible for three things, in order:

1. Removing any data from previous runs
2. Rebuilding the table schemas
3. Inserting the test data

Because these are distinct responsibilities, you are encouraged to break the implementation across several smaller functions rather than handling everything in one place.


![Database ERD](https://assets.northcoders.com/nc-plus-one-erd.png "520px 500px Database ERD")

## Requirements

- Review the ERD before writing any code — make sure you understand the tables, their columns, and how they relate to each other
- Create a `seed` function in an appropriate location within the project
- The function should be invocable directly, so the database can be reset at any point during development
- At this stage the function can be empty - functionality will be added in subsequent tickets

## Acceptance criteria
- The ERD has been reviewed and the database structure is understood before proceeding
- A `seed` function exists and can be invoked


---
<br/><br/>


# 04 - Database Connection

**Goal:** Create a reusable database connection object that reads credentials from environment variables rather than hardcoded values.

## Requirements

- Create a `connection.py` file that establishes a connection to `nc_plus_one`
- Credentials should be stored in a `.env` file and loaded using `python-dotenv` — they must not be hardcoded anywhere in the codebase
- Create a `.env.example` file containing the same keys but no values, so other developers know what credentials are required without exposing your own
- Add `.env` to `.gitignore` before making any commits — credentials must never be pushed to source control

## Acceptance criteria
- `connection.py` exists and successfully connects to `nc_plus_one`
- All credentials are loaded from `.env` via `python-dotenv`
- `.env` is present in `.gitignore`
- `.env.example` is committed to the repository with the required keys but no values
- Update `README.md` to explain that to other devs that a `.env` should be created with the individual's local database credentials


---
<br/><br/>


# 05 - Seed Users

**Goal:** Implement the users portion of the seed function — dropping, recreating, and populating the users table.

![Database ERD](https://assets.northcoders.com/nc-plus-one-erd.png "520px 500px Database ERD")

## Requirements

- Drop the users table if it exists
- Create the users table according to the schema defined in the ERD
- Read the user data from the JSON file in the `data` directory and bulk insert it into the newly created table
- Any utility functions written to normalise or manipulate data before insertion must be built using TDD

## A note on structure

This ticket adds real functionality to the seed function. As with the seed function itself, consider whether the logic is best handled in one place or broken down into smaller, focused functions. Each responsibility — dropping, creating, inserting — is a candidate for its own function.

## Acceptance criteria
- The users table is dropped and recreated each time the seed function runs
- All user records from the JSON file are inserted into the table
- Any data transformation logic lives in a utility function covered by TDD
- Running the seed function multiple times produces the same result with no errors


---
<br/><br/>


# 06 - Seed Venues

**Goal:** Implement the venues portion of the seed function — dropping, recreating, and populating the venues table.

![Database ERD](https://assets.northcoders.com/nc-plus-one-erd.png "520px 500px Database ERD")

## Requirements

- Drop the venues table if it exists
- Create the venues table according to the schema defined in the ERD
- Read the venue data from the JSON file in the `data` directory and bulk insert it into the newly created table
- Any utility functions written to normalise or manipulate data before insertion must be built using TDD

## A note on structure

This ticket adds real functionality to the seed function. As with the seed function itself, consider whether the logic is best handled in one place or broken down into smaller, focused functions. Each responsibility — dropping, creating, inserting — is a candidate for its own function.

## Acceptance criteria
- The venues table is dropped and recreated each time the seed function runs
- All venue records from the JSON file are inserted into the table
- Any data transformation logic lives in a utility function covered by TDD
- Running the seed function multiple times produces the same result with no errors


---
<br/><br/>


# 07 - Seed Events

**Goal:** Implement the events portion of the seed function — dropping, recreating, and populating the events table.

![Database ERD](https://assets.northcoders.com/nc-plus-one-erd.png "520px 500px Database ERD")

## Requirements

- Drop the events table if it exists
- Create the events table according to the schema defined in the ERD
- Read the event data from the JSON file in the `data` directory and bulk insert it into the newly created table
- Any utility functions written to normalise or manipulate data before insertion must be built using TDD

## A note on structure

This ticket adds real functionality to the seed function. As with the seed function itself, consider whether the logic is best handled in one place or broken down into smaller, focused functions. Each responsibility — dropping, creating, inserting — is a candidate for its own function.

## Acceptance criteria
- The events table is dropped and recreated each time the seed function runs
- All event records from the JSON file are inserted into the table
- Any data transformation logic lives in a utility function covered by TDD
- Running the seed function multiple times produces the same result with no errors


---
<br/><br/>


# 08 - Seed RSVPs

**Goal:** Implement the RSVPs portion of the seed function — dropping, recreating, and populating the RSVPs table.

![Database ERD](https://assets.northcoders.com/nc-plus-one-erd.png "520px 500px Database ERD")

## Requirements

- Drop the RSVPs table if it exists
- Create the RSVPs table according to the schema defined in the ERD
- Read the RSVP data from the JSON file in the `data` directory and bulk insert it into the newly created table
- Any utility functions written to normalise or manipulate data before insertion must be built using TDD

## A note on structure

This ticket adds real functionality to the seed function. As with the seed function itself, consider whether the logic is best handled in one place or broken down into smaller, focused functions. Each responsibility — dropping, creating, inserting — is a candidate for its own function.

## Acceptance criteria
- The RSVPs table is dropped and recreated each time the seed function runs
- All RSVP records from the JSON file are inserted into the table
- Any data transformation logic lives in a utility function covered by TDD
- Running the seed function multiple times produces the same result with no errors


---
<br/><br/>


# 09 - GET /api/events

**Goal:** Create an endpoint that returns a list of all events.

## Endpoint

```
GET /api/events
```

## Expected response — 200 OK

```json
{
  "events": [
    {
      "id": 1,
      "title": "Leeds Tech Meetup – June Edition",
      "starts_at": "2026-06-18T18:30:00+01:00",
      "ends_at": "2026-06-18T21:00:00+01:00",
      "location": "Nexus, Leeds, LS2 8PD"
    },
  // ...
  ]
}
```

## Requirements

- Returns all events from the database
- Results must be ordered — choose an attribute that produces a meaningful and predictable order, and be prepared to justify your decision
- The response body must be an object with an `events` key, not a bare array

## Acceptance criteria

- `GET /api/events` responds with a `200` status code
- The response contains all seeded events
- Events are returned in a consistent, justified order
- The endpoint is covered by integration tests


---
<br/><br/>


# 10 - GET /api/events/:id

**Goal:** Create an endpoint that returns a single event by its ID.

## Endpoint

```
GET /api/events/:id
```

## Expected response — 200 OK

```json
{
  "event": {
    "id": 2,
    "title": "Intro to Machine Learning Workshop",
    "description": "Hands-on workshop covering perceptrons, neural networks, and classifiers using NumPy and PyTorch.",
    "starts_at": "2026-06-25T10:00:00+01:00",
    "ends_at": "2026-06-25T13:00:00+01:00",
    "location": "Online – Zoom",
    "address": null,
    "capacity": 100,
    "created_at": "2026-06-09T10:38:20.737764+01:00"
  }
}
```

## Requirements

- Returns a single event matching the given `id`
- The response body must be an object with an `event` key
- Handles the case where the `id` does not match any event
- The response should include venue details joined from the Venues table.

## Error cases

| Scenario | Status code |
|---|---|
| Event not found | `404 Not Found` |
| `id` is not a valid integer | `400 Bad Request` |

## Acceptance criteria

- `GET /api/events/:id` responds with a `200` status code and the correct event
- A non-existent ID returns a `404`
- An invalid ID returns a `400`
- All cases are covered by integration tests


---
<br/><br/>


# 11 - POST /api/auth/login

**Goal:** Create an endpoint that authenticates an existing user and returns a JWT for use on protected routes.

## Before you start — update the seed function

The login endpoint verifies a submitted password against the hash stored in the database. This means the seed data must contain hashed passwords, not plaintext ones.

Before implementing this endpoint, update your seed function to hash each user's password before inserting it. The plaintext passwords in `users.json` should be treated as inputs to the hashing function, not values to be stored directly.

Once updated, run your seed function and verify that the `password` column in the `users` table contains hashed values before proceeding.

## Endpoint

```
POST /api/auth/login
```

## Request body

```json
{
  "email": "alice@example.com",
  "password": "securepassword123"
}
```

## Expected response — 200 OK

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Requirements

- Verifies the submitted password against the stored hash
- Returns a signed JWT on success — the token payload should contain enough information to identify the user on subsequent requests
- Handles invalid credentials without revealing which field was incorrect

## Error cases

| Scenario | Status code |
|---|---|
| Email not found or password incorrect | `401 Unauthorized` |
| Missing `email` or `password` field | `400 Bad Request` |

> Return the same `401` whether the email doesn't exist or the password is wrong. Distinguishing between the two is a security risk.

## Acceptance criteria

- The seed function hashes passwords before inserting them
- `POST /api/auth/login` responds with a `200` and a signed JWT on valid credentials
- Invalid credentials return a `401` regardless of which field is wrong
- Missing fields return a `400`
- All cases are covered by integration tests


---
<br/><br/>


# 12 - POST /api/auth/register

**Goal:** Create an endpoint that registers a new user account.

## Endpoint

```
POST /api/auth/register
```

## Request body

```json
{
  "name": "Alice Smith",
  "email": "alice@example.com",
  "password": "securepassword123"
}
```

## Expected response — 201 Created

```json
{
  "user": {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "created_at": "2025-06-01T10:00:00Z"
  }
}
```

## Requirements

- Stores the user in the database with a hashed password — the plaintext password must never be saved
- The response must not include the password field under any circumstances

## Error cases

| Scenario | Status code |
|---|---|
| Email already registered | `409 Conflict` |
| Missing any required field | `400 Bad Request` |

## Acceptance criteria

- `POST /api/auth/register` responds with a `201` and the created user on success
- The password is hashed before being stored
- The password field is never present in the response
- A duplicate email returns a `409`
- Missing fields return a `400`
- All cases are covered by integration tests


---
<br/><br/>


# 13 - POST /api/events/:id/rsvp

**Goal:** Create an endpoint that allows an authenticated user to RSVP to an event.

## Endpoint

```
POST /api/events/:id/rsvp
Authorization: Bearer <token>
```

## Request body

None — the user is identified from the token and the event from the URL.

## Expected response — 201 Created

```json
{
  "rsvp": {
    "id": 55,
    "attendee_id": 1,
    "event_id": 12,
    "created_at": "2025-06-01T11:00:00Z"
  }
}
```

## Requirements

- Requires a valid JWT — the `user_id` must be read from the token, not the request body
- Creates an RSVP record linking the authenticated user to the given event

## Error cases

| Scenario | Status code |
|---|---|
| Missing or invalid token | `401 Unauthorized` |
| Event not found | `404 Not Found` |
| User has already RSVPed to this event | `409 Conflict` |

## Acceptance criteria

- `POST /api/events/:id/rsvp` responds with a `201` and the created RSVP on success
- Requests without a valid token return a `401`
- A non-existent event ID returns a `404`
- A duplicate RSVP returns a `409`
- All cases are covered by integration tests


---
<br/><br/>


# 14 - DELETE /api/events/:id/rsvp/me

**Goal:** Create an endpoint that allows an authenticated user to cancel their own RSVP.

## Endpoint

```
DELETE /api/events/:id/rsvp/me
Authorization: Bearer <token>
```

## Request body

None — the user is identified from the token and the event from the URL.

## Expected response — 204 No Content

No response body.

## Requirements

- Requires a valid JWT — the user is identified from the token
- A user may only cancel their own RSVP

## Error cases

| Scenario | Status code |
|---|---|
| Missing or invalid token | `401 Unauthorized` |
| No RSVP exists for this user on this event | `404 Not Found` |

## Acceptance criteria

- `DELETE /api/events/:id/rsvp/me` responds with a `204` on success
- Requests without a valid token return a `401`
- Attempting to cancel an RSVP that does not exist returns a `404`
- All cases are covered by integration tests


---
<br/><br/>


# 15 - POST /api/events

**Goal:** Create an endpoint that allows an authenticated user to create a new event. The authenticated user automatically becomes the organiser.

## Endpoint

```
POST /api/events
Content-Type: application/json
Authorization: Bearer <token>
```

## Request body

```json
{
  "title": "Summer Rooftop Social",
  "description": "An evening of networking and good vibes.",
  "starts_at": "2025-08-15T18:00:00Z",
  "ends_at": "2025-08-15T21:00:00Z",
  "venue_id": 2
}
```

## Expected response — 201 Created

```json
{
  "event": {
      "id": 12,
      "title": "Summer Rooftop Social",
      "description": "An evening of networking and good vibes.",
      "starts_at": "2025-08-15T18:00:00Z",
      "ends_at": "2025-08-15T21:00:00Z",
      "venue_id": 2,
      "organiser_id": 1,
      "created_at": "2025-06-01T10:00:00Z"
  }
}

```

## Requirements

- Requires a valid JWT — the `organiser_id` must be read from the token, not accepted in the request body
- Dates must be valid ISO 8601 strings

## Error cases

| Scenario | Status code |
|---|---|
| Missing or invalid token | `401 Unauthorized` |
| Missing required fields | `400 Bad Request` |
| Invalid date format | `400 Bad Request` |

## Acceptance criteria

- `POST /api/events` responds with a `201` and the created event on success
- `organiser_id` is derived from the token and not accepted from the request body
- Requests without a valid token return a `401`
- Missing or malformed fields return a `400`
- All cases are covered by integration tests


---
<br/><br/>


# 16 - PATCH /api/events/:id

**Goal:** Create an endpoint that allows an organiser to update the details of their own event.

## Endpoint

```
PATCH /api/events/:id
Content-Type: application/json
Authorization: Bearer <token>
```

## Request body

All fields are optional. Only include the fields to be updated.

```json
{
  "description": "Updated description — now with live music!",
  "starts_at": "2025-08-16T19:00:00Z",
  "ends_at": "2025-08-16T23:00:00Z"
}
```

## Expected response — 200 OK

```json
{
  "event": {
      "id": 12,
      "title": "Summer Rooftop Social",
      "description": "Updated description — now with live music!",
      "starts_at": "2025-08-16T19:00:00Z",
      "ends_at": "2025-08-16T23:00:00Z",
      "venue_id": 3,
      "organiser_id": 1,
      "created_at": "2025-06-01T10:00:00Z"
  }
}
```

## Requirements

- Requires a valid JWT — only the organiser of the event may update it
- Only fields present in the request body should be updated — omitted fields must remain unchanged
- If `starts_at` or `ends_at` are provided, both must result in a valid range where `ends_at` is after `starts_at`

## Error cases

| Scenario | Status code |
|---|---|
| Missing or invalid token | `401 Unauthorized` |
| Authenticated user is not the organiser | `403 Forbidden` |
| Event not found | `404 Not Found` |
| Invalid date format | `400 Bad Request` |
| `ends_at` is before `starts_at` | `400 Bad Request` |

## Acceptance criteria

- `PATCH /api/events/:id` responds with a `200` and the full updated event on success
- Only the fields present in the request body are modified
- Requests from a user who is not the organiser return a `403`
- A non-existent event ID returns a `404`
- Requests without a valid token return a `401`
- All cases are covered by integration tests


---
<br/><br/>


# 17 - GET /api/events/:id/attendees

**Goal:** Create an endpoint that returns the list of users who have RSVPed to a given event. Only the organiser of the event may access this list.

## Endpoint

```
GET /api/events/:id/attendees
Authorization: Bearer <token>
```

## Expected response — 200 OK

```json
{
  "attendees": [
    {
      "id": 1,
      "name": "Alice Smith",
      "email": "alice@example.com"
    },
    {
      "id": 7,
      "name": "Bob Jones",
      "email": "bob@example.com"
    }
  ]
}
```

## Requirements

- Requires a valid JWT — only the organiser of the event may access the attendee list
- The response must never include the `password` field

## Error cases

| Scenario | Status code |
|---|---|
| Missing or invalid token | `401 Unauthorized` |
| Authenticated user is not the organiser | `403 Forbidden` |
| Event not found | `404 Not Found` |

## Acceptance criteria

- `GET /api/events/:id/attendees` responds with a `200` and the correct attendee list on success
- Requests without a valid token return a `401`
- Requests from a user who is not the organiser return a `403`
- The `password` field is never present in any user object in the response
- A non-existent event ID returns a `404`
- All cases are covered by integration tests


---
<br/><br/>


# 18 - GET /api/user/me/events

**Goal:** Create an endpoint that returns all events the authenticated user has RSVPed to, enriched with window function data.

## Endpoint

```
GET /api/user/me/events
Authorization: Bearer <token>
```

## Expected response — 200 OK

```json
{
  "events": [
    {
      "id": 8,
      "title": "Spring Networking Night",
      "starts_at": "2025-04-10T18:00:00Z",
      "rsvp_date": "2025-03-01T09:00:00Z",
      "event_rank": 1,
      "total_rsvps": 3
    },
    {
      "id": 12,
      "title": "Summer Rooftop Social",
      "starts_at": "2025-08-16T19:00:00Z",
      "rsvp_date": "2025-06-01T11:00:00Z",
      "event_rank": 2,
      "total_rsvps": 3
    }
  ]
}
```

## Field definitions

| Field | Description |
|---|---|
| `rsvp_date` | The date and time the user RSVPed to the event |
| `event_rank` | The position of this event among the user's RSVPs, ordered by `starts_at` ascending (1 = earliest) |
| `total_rsvps` | The total number of events this user has RSVPed to |

## Requirements

- Requires a valid JWT — the user is identified from the token
- `event_rank` and `total_rsvps` must be computed using SQL window functions, not in application code
- Results must be ordered by `starts_at` ascending

## Error cases

| Scenario | Status code |
|---|---|
| Missing or invalid token | `401 Unauthorized` |

## Acceptance criteria

- `GET /api/user/me/events` responds with a `200` and the correct events on success
- `event_rank` and `total_rsvps` are produced by SQL window functions
- Results are ordered by `starts_at` ascending
- Requests without a valid token return a `401`
- All cases are covered by integration tests


---
<br/><br/>


# 19 - GET /api/organisers/:id/stats

**Goal:** Create an endpoint that returns aggregate statistics for an organiser, including how they rank compared to all other organisers.

## Endpoint

```
GET /api/organisers/:id/stats
```

## Expected response — 200 OK

```json
{ 
  "stats": {
      "organiser_id": 1,
      "name": "Alice Smith",
      "total_events": 5,
      "avg_attendance": 28.4,
      "best_attended_count": 61,
      "organiser_rank": 2
  }
}
```

## Field definitions

| Field | Description |
|---|---|
| `total_events` | Total number of events this organiser has created |
| `avg_attendance` | Average RSVP count across all of their events |
| `best_attended_count` | RSVP count for their single most-attended event |
| `organiser_rank` | Their rank among all organisers by total events hosted (1 = most events) |

## Requirements

- `organiser_rank` must be computed using a SQL window function across all organisers — it cannot be derived from a single organiser query alone
- Per-event attendee counts must be computed before aggregating — consider a subquery or CTE
- `avg_attendance` should be rounded to one decimal place

## Error cases

| Scenario | Status code |
|---|---|
| Organiser not found | `404 Not Found` |

## Acceptance criteria

- `GET /api/organisers/:id/stats` responds with a `200` and the correct stats on success
- All four aggregate fields are present and accurate
- `organiser_rank` is produced using a SQL window function
- An organiser ID that does not exist or has no events returns a `404`
- The endpoint is covered by integration tests
