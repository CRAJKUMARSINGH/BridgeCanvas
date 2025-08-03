from datetime import datetime
from . import db

class BridgeDesign(db.Model):
    """Database model for storing bridge designs"""
    __tablename__ = 'bridge_designs'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False, default='Untitled Project')
    original_filename = db.Column(db.String(255), nullable=False)
    generated_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional metadata
    span_length = db.Column(db.Float, nullable=True)
    bridge_type = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'project_name': self.project_name,
            'original_filename': self.original_filename,
            'generated_filename': self.generated_filename,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'span_length': self.span_length,
            'bridge_type': self.bridge_type,
            'status': self.status
        }
