from flask import Blueprint, request, jsonify
from models.jobs import Job
from db import db
from sqlalchemy import or_
from datetime import datetime

job_bp = Blueprint('jobs', __name__)

@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        # Filtering parameters
        job_type = request.args.get('job_type')
        location = request.args.get('location')
        tag = request.args.get('tag')
        search = request.args.get('search')
        
        # Sorting parameters
        sort = request.args.get('sort', 'posting_date_desc')
        
        # Base query
        query = Job.query
        
        # Apply filters
        if job_type and job_type != 'All':
            query = query.filter(Job.job_type == job_type)
        
        if location and location != 'All':
            query = query.filter(Job.location.contains(location))
        
        if tag and tag != 'All':
            query = query.filter(Job.tags.contains(tag))
        
        if search:
            query = query.filter(
                or_(
                    Job.title.contains(search),
                    Job.company.contains(search)
                )
            )
        
        # Apply sorting
        if sort == 'posting_date_desc':
            query = query.order_by(Job.posting_date.desc())
        elif sort == 'posting_date_asc':
            query = query.order_by(Job.posting_date.asc())
        
        jobs = query.all()
        return jsonify([job.to_dict() for job in jobs])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/jobs', methods=['POST'])
def create_job():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['title', 'company', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new job
        new_job = Job(
            title=data['title'],
            company=data['company'],
            location=data['location'],
            posting_date=data.get('posting_date', datetime.now().strftime("%Y-%m-%d")),
            job_type=data.get('job_type', 'Full-time'),
            tags=','.join(data.get('tags', []))
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        return jsonify(new_job.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@job_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            job.title = data['title']
        if 'company' in data:
            job.company = data['company']
        if 'location' in data:
            job.location = data['location']
        if 'posting_date' in data:
            job.posting_date = data['posting_date']
        if 'job_type' in data:
            job.job_type = data['job_type']
        if 'tags' in data:
            job.tags = ','.join(data['tags'])
        
        db.session.commit()
        
        return jsonify(job.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@job_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        db.session.delete(job)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500