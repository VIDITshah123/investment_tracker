import logging
from sqlalchemy.orm import Session
from database.models import ManagementNote, Alert

logger = logging.getLogger(__name__)

class GuidanceTracker:
    def __init__(self, session: Session):
        self.session = session

    def check_guidance_drift(self, company_id: int):
        notes = self.session.query(ManagementNote).filter_by(company_id=company_id).order_by(ManagementNote.created_at.desc()).limit(4).all()
        down_streak = 0
        for n in notes:
            if n.direction == 'down':
                down_streak += 1
            else:
                break
        
        if down_streak >= 3:
            alert = Alert(
                company_id=company_id,
                alert_type="guidance_drift",
                message=f"Warning: Management guidance revised downward for {down_streak} consecutive quarters."
            )
            self.session.add(alert)
            self.session.commit()
            logger.warning(f"Guidance drift alert created for company_id={company_id}")
