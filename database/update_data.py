import psycopg2

def update_user(conn, user_id, name, email, phone, password_hash, role, status, verified_organizer, updated_at):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE users
            SET name = %s,
                email = %s,
                phone = %s,
                password_hash = %s,
                role = %s,
                status = %s,
                verified_organizer = %s,
                updated_at = %s
            WHERE id = %s;
        """, (name, email, phone, password_hash, role, status, verified_organizer, updated_at, user_id))
    conn.commit()

def update_event(conn, event_id, title, description, category, location, lat, lng, start_time, end_time, created_by, approved, photos, status, updated_at):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE events
            SET title = %s,
                description = %s,
                category = %s,
                location = %s,
                lat = %s,
                lng = %s,
                start_time = %s,
                end_time = %s,
                created_by = %s,
                approved = %s,
                photos = %s,
                status = %s,
                updated_at = %s
            WHERE id = %s;
        """, (title, description, category, location, lat, lng, start_time, end_time, created_by, approved, photos, status, updated_at, event_id))
    conn.commit()

def update_rsvp(conn, rsvp_id, event_id, user_id, name, email, phone, num_guests, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE rsvps
            SET event_id = %s,
                user_id = %s,
                name = %s,
                email = %s,
                phone = %s,
                num_guests = %s,
                timestamp = %s
            WHERE id = %s;
        """, (event_id, user_id, name, email, phone, num_guests, timestamp, rsvp_id))
    conn.commit()

def update_admin_action(conn, action_id, admin_id, action_type, target_id, details, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE admin_actions
            SET admin_id = %s,
                action_type = %s,
                target_id = %s,
                details = %s,
                timestamp = %s
            WHERE id = %s;
        """, (admin_id, action_type, target_id, details, timestamp, action_id))
    conn.commit()

def update_event_history(conn, history_id, event_id, user_id, action, details, timestamp):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE event_history
            SET event_id = %s,
                user_id = %s,
                action = %s,
                details = %s,
                timestamp = %s
            WHERE id = %s;
        """, (event_id, user_id, action, details, timestamp, history_id))
    conn.commit()

# Example usage:
# Example usage:
conn = psycopg2.connect(dbname="community_pulse",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432")


update_user(
    conn,
    "1a2b3c4d-1111-2222-3333-444455556666",   # user_id
    "Alice J. Johnson",                       # name (changed)
    "alice.jj@example.com",                   # email (changed)
    "+1234567899",                            # phone (changed)
    "new_hashed_password",                    # password_hash (changed)
    "user",                                   # role
    "active",                                 # status
    True,                                     # verified_organizer (changed)
    "2025-05-20T15:00:00Z"                    # updated_at (changed)
)

update_event(
    conn,
    "3c4d5e6f-3333-4444-5555-666677778888",   # event_id
    "Community Yoga & Meditation",            # title (changed)
    "Now includes a meditation session.",     # description (changed)
    "Community Classes",                      # category
    "Main Community Center",                  # location (changed)
    40.712800,                               # lat (changed)
    -74.005900,                              # lng (changed)
    "2025-06-01T08:30:00Z",                   # start_time (changed)
    "2025-06-01T10:00:00Z",                   # end_time (changed)
    "1a2b3c4d-1111-2222-3333-444455556666",   # created_by
    True,                                     # approved
    ["https://example.com/photos/yoga1.jpg", "https://example.com/photos/yoga3.jpg"],  # photos (changed)
    "active",                                 # status
    "2025-05-20T15:00:00Z"                    # updated_at (changed)
)


update_rsvp(
    conn,
    "6f7e8a9b-6666-7777-8888-999900001111",   # rsvp_id
    "3c4d5e6f-3333-4444-5555-666677778888",   # event_id
    "1a2b3c4d-1111-2222-3333-444455556666",   # user_id
    "Alice J. Johnson",                       # name (changed)
    "alice.jj@example.com",                   # email (changed)
    "+1234567899",                            # phone (changed)
    2,                                        # num_guests (changed)
    "2025-05-20T16:00:00Z"                    # timestamp (changed)
)


update_admin_action(
    conn,
    "8a9b0c1d-8888-9999-0000-111122223333",   # action_id
    "2b3c4d5e-2222-3333-4444-555566667777",   # admin_id
    "approve",                                # action_type
    "3c4d5e6f-3333-4444-5555-666677778888",   # target_id
    "Approved event after reviewing updates.", # details (changed)
    "2025-05-20T17:00:00Z"                    # timestamp (changed)
)


update_event_history(
    conn,
    "0a1b2c3d-0000-1111-2222-333344445555",   # history_id
    "3c4d5e6f-3333-4444-5555-666677778888",   # event_id
    "1a2b3c4d-1111-2222-3333-444455556666",   # user_id
    "Updated",                                # action (changed)
    "Event updated to include meditation.",   # details (changed)
    "2025-05-20T18:00:00Z"                    # timestamp (changed)
)
