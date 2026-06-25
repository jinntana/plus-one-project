DROP TABLE IF EXISTS rsvps;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  email      VARCHAR(255) UNIQUE NOT NULL,
  password   VARCHAR(255) NOT NULL,
  name       VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE venues (
  id       SERIAL PRIMARY KEY,
  name     VARCHAR(255) NOT NULL,
  address  VARCHAR(255),
  capacity INT NOT NULL
);

CREATE TABLE events (
  id           SERIAL PRIMARY KEY,
  title        VARCHAR(255) NOT NULL,
  description  TEXT,
  starts_at    TIMESTAMPTZ NOT NULL,
  ends_at      TIMESTAMPTZ NOT NULL,
  organiser_id INT NOT NULL REFERENCES users(id),
  venue_id     INT NOT NULL REFERENCES venues(id),
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE rsvps (
  id          SERIAL PRIMARY KEY,
  attendee_id INT NOT NULL REFERENCES users(id),
  event_id    INT NOT NULL REFERENCES events(id),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);