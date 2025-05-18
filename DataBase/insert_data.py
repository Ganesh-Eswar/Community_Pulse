import psycopg2

def insert_user(conn, id, name, email, phone, password_hash, role, status, verified_organizer, created_at, updated_at):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (id, name, email, phone, password_hash, role, status, verified_organizer, created_at, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING;
        """, (id, name, email, phone, password_hash, role, status, verified_organizer, created_at, updated_at))
    conn.commit()

def insert_event(conn, id, title, description, category, location, lat, lng, start_time, end_time, created_by, approved, photos, status, created_at, updated_at):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO events (id, title, description, category, location, lat, lng, start_time, end_time, created_by, approved, photos, status, created_at, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING;
        """, (id, title, description, category, location, lat, lng, start_time, end_time, created_by, approved, photos, status, created_at, updated_at))
    conn.commit()

def insert_rsvp(conn, id, event_id, user_id, name, email, phone, num_guests, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO rsvps (id, event_id, user_id, name, email, phone, num_guests, timestamp)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING;
        """, (id, event_id, user_id, name, email, phone, num_guests, timestamp))
    conn.commit()

def insert_admin_action(conn, id, admin_id, action_type, target_id, details, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO admin_actions (id, admin_id, action_type, target_id, details, timestamp)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING;
        """, (id, admin_id, action_type, target_id, details, timestamp))
    conn.commit()

def insert_event_history(conn, id, event_id, user_id, action, details, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO event_history (id, event_id, user_id, action, details, timestamp)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING;
        """, (id, event_id, user_id, action, details, timestamp))
    conn.commit()

# Example usage:
conn = psycopg2.connect(dbname="community_pulse",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432")
# insert_user(conn, "1a2b3c4d-1111-2222-3333-44445555666", "Alice Johnson", "alice.johnson@example.com", "+1234567890", "hashed_password_1", "user", "active", False, "2025-01-01T10:00:00Z", "2025-04-01T12:00:00Z")
# insert_event(conn, "3c4d5e6f-3333-4444-5555-666677778888", "Community Yoga Session", "A relaxing yoga session for all levels.", "Community Classes", "Community Center Hall", 40.712776, -74.005974, "2025-06-01T08:00:00Z", "2025-06-01T09:30:00Z", "1a2b3c4d-1111-2222-3333-444455556666", True, ["https://example.com/photos/yoga1.jpg", "https://example.com/photos/yoga2.jpg"], "active", "2025-05-01T10:00:00Z", "2025-05-10T12:00:00Z")
# insert_rsvp(conn, "5e6f7g8h-5555-6666-7777-888899990000", "3c4d5e6f-3333-4444-5555-666677778888", "1a2b3c4d-1111-2222-3333-444455556666", "Alice Johnson", "alice.johnson@example.com", "+1234567890", 1, "2025-05-15T14:00:00Z")
# insert_admin_action(conn, "7g8h9i0j-7777-8888-9999-000011112222", "2b3c4d5e-2222-3333-4444-555566667777", "approve", "3c4d5e6f-3333-4444-5555-666677778888", "Approved yoga session event.", "2025-05-10T13:00:00Z")
# insert_event_history(conn, "9i0j1k2l-9999-0000-1111-222233334444", "3c4d5e6f-3333-4444-5555-666677778888", "1a2b3c4d-1111-2222-3333-444455556666", "Created", "Event created by Alice Johnson.", "2025-04-30T10:00:00Z")

insert_user(
    conn,
    "2b3c4d5e-2222-3333-4444-555566667777",
    "Bob Smith",
    "bob.smith@example.com",
    "+1987654321",
    "hashed_password_2",
    "admin",
    "active",
    True,
    "2024-12-15T09:30:00Z",
    "2025-04-15T11:00:00Z"
)

insert_event(
    conn,
    "4d5e6f7a-4444-5555-6666-777788889999",
    "Local Football Match",
    "Friendly football match at the local park.",
    "Sports Matches",
    "Local Park",
    40.730610,
    -73.935242,
    "2025-06-05T15:00:00Z",
    "2025-06-05T17:00:00Z",
    "2b3c4d5e-2222-3333-4444-555566667777",
    False,
    [],
    "pending",
    "2025-05-02T11:00:00Z",
    "2025-05-11T13:00:00Z"
)


insert_rsvp(
    conn,
    "6f7e8a9b-6666-7777-8888-999900001111",  # fixed
    "4d5e6f7a-4444-5555-6666-777788889999",  # fixed
    "2b3c4d5e-2222-3333-4444-555566667777",
    "Bob Smith",
    "bob.smith@example.com",
    "+1987654321",
    3,
    "2025-05-16T15:30:00Z"
)

insert_admin_action(
    conn,
    "8a9b0c1d-8888-9999-0000-111122223333",  # fixed
    "2b3c4d5e-2222-3333-4444-555566667777",
    "ban",
    "1a2b3c4d-1111-2222-3333-444455556666",
    "Banned user for spamming.",
    "2025-05-12T09:00:00Z"
)

insert_event_history(
    conn,
    "0a1b2c3d-0000-1111-2222-333344445555",  # fixed
    "4d5e6f7a-4444-5555-6666-777788889999",  # fixed
    "2b3c4d5e-2222-3333-4444-555566667777",
    "Updated",
    "Event details updated by Bob Smith.",
    "2025-05-05T14:00:00Z"
)


conn.close()
