from app import db
from datetime import datetime

class BridgeDesign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    parameters = db.Column(db.Text)  # JSON string of parameters
    dxf_filename = db.Column(db.String(255))
    status = db.Column(db.String(50), default='processing')
    error_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<BridgeDesign {self.filename}>'

class BridgeParameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    design_id = db.Column(db.Integer, db.ForeignKey('bridge_design.id'), nullable=False)
    variable_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    
    design = db.relationship('BridgeDesign', backref=db.backref('parameters', lazy=True))
