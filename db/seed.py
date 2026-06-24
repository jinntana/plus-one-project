import json
from connection import get_connection


def seed():
    conn = get_connection()
    cursor = conn.cursor()

    with open("db/schema.sql") as file:
        schema = file.read()

    cursor.execute(schema)

    with open("db/data/users.json") as file:
        users = json.load(file)

    with open("db/data/users.json") as file:
        users = json.load(file)

    user_rows = []

    for user in users:
        user_rows.append(
            (
                user["name"],
                user["email"],
                user["password"]
            )
        )

    cursor.executemany(
    """
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    """,
    user_rows
    )   


    with open("db/data/venues.json") as file:
        venues = json.load(file)

    venue_rows = []

    for venue in venues:
        venue_rows.append(
            (
                venue["name"],
                venue["address"],
                venue["capacity"]
            )
        )

    cursor.executemany(
    """
    INSERT INTO venues (name, address, capacity)
    VALUES (%s, %s, %s)
    """,
    venue_rows
    )
        
    with open("db/data/events.json") as file:
        events = json.load(file)

    event_rows = []

    for event in events:
        event_rows.append(
            (
                event["title"],
                event["description"],
                event["starts_at"],
                event["ends_at"],
                event["organiser_id"],
                event["venue_id"]
            )
            )

    cursor.executemany(
    """
    INSERT INTO events (
        title,
        description,
        starts_at,
        ends_at,
        organiser_id,
        venue_id
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    event_rows
    )

    with open("db/data/rsvps.json") as file:
        rsvps = json.load(file)

    rsvp_rows = []

    for rsvp in rsvps:
         rsvp_rows.append(
        (
            rsvp["attendee_id"],
            rsvp["event_id"]
        )
        )

    cursor.executemany(
    """
    INSERT INTO rsvps (attendee_id, event_id)
    VALUES (%s, %s)
    """,
    rsvp_rows
    )


    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed()