from db import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'job'
    __table_args__ = {'extend_existing': True}  # 👈 ADD THIS LINE
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    posting_date = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')
    tags = db.Column(db.String(500), default='')  # Comma-separated tags

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'posting_date': self.posting_date,
            'job_type': self.job_type,
            'tags': self.tags.split(',') if self.tags else []
        }

    @classmethod
    def create_from_scraped_data(cls, data):
        return cls(
            title=data['title'],
            company=data['company'],
            location=data['location'],
            posting_date=data['posting_date'],
            job_type=data.get('job_type', 'Full-time'),
            tags=','.join(data.get('tags', []))
        )