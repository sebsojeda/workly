from sqlalchemy.sql import text

from .database import SessionLocal


def create_triggers(db: SessionLocal) -> None:
    db.execute(
        text(
            """\
CREATE TRIGGER IF NOT EXISTS create_applicant_notification AFTER INSERT ON jobs
FOR EACH ROW
BEGIN
    INSERT INTO notifications (message, job_id, created_at, updated_at)
    VALUES (
        'A new job was posted: ' || NEW.title || ' at ' || (SELECT name FROM employers WHERE id = NEW.employer_id) || ' in ' || NEW.location || '!',
        NEW.id,
        datetime('now'),
        datetime('now')
    );
END;"""
        )
    )
