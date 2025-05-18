import psycopg2

def delete_user(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM users WHERE id = %s;
        """, (user_id,))
    conn.commit()

def delete_event(conn, event_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM events WHERE id = %s;
        """, (event_id,))
    conn.commit()

def delete_rsvp(conn, rsvp_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM rsvps WHERE id = %s;
        """, (rsvp_id,))
    conn.commit()

def delete_admin_action(conn, action_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM admin_actions WHERE id = %s;
        """, (action_id,))
    conn.commit()

def delete_event_history(conn, history_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM event_history WHERE id = %s;
        """, (history_id,))
    conn.commit()

# Example usage:
conn = psycopg2.connect(dbname="community_pulse",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432")
delete_user(conn, "2b3c4d5e-2222-3333-4444-555566667777")
delete_event(conn, "4d5e6f7a-4444-5555-6666-777788889999")
delete_rsvp(conn, "6f7e8a9b-6666-7777-8888-999900001111")
delete_admin_action(conn, "8a9b0c1d-8888-9999-0000-111122223333")
delete_event_history(conn, "0a1b2c3d-0000-1111-2222-333344445555")
conn.close()
