# utils.py

from models import db, EventHistory, AdminAction
from flask_login import current_user
from datetime import datetime

def log_event_action(event_id, user_id, action, details):
    history = EventHistory(
        event_id=event_id,
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.session.add(history)
    db.session.commit()

def log_admin_action(admin_id, action_type, target_id, details):
    log = AdminAction(
        admin_id=admin_id,
        action_type=action_type,
        target_id=target_id,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
