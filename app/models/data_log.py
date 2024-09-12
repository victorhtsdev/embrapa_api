from app.extensions import db

class DataLog(db.Model):
    __tablename__ = 'data_log'

    uuid = db.Column(db.String(36), primary_key=True)
    object = db.Column(db.String(255), nullable=True)
    record_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    object_modified_date = db.Column(db.DateTime, nullable=True)