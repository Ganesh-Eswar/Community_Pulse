import psycopg2

def select_all_users(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def select_all_events(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM events;")
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def select_all_rsvps(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM rsvps;")
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def select_all_admin_actions(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM admin_actions;")
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

def select_all_event_history(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM event_history;")
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

# Example usage:
# Example usage:
conn = psycopg2.connect(dbname="community_pulse",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432")

users = select_all_users(conn)
events = select_all_events(conn)
rsvps = select_all_rsvps(conn)
admin_actions = select_all_admin_actions(conn)
event_history = select_all_event_history(conn)
print(users)
print(events)
print(rsvps)
print(admin_actions)
print(event_history)
conn.close()
