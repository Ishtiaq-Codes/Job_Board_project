import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    

from flask import Flask
from config import Config
from db import db
from routes.job_routes import job_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # ###############CORS setup  Allow React frontend to connect##########
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    app.register_blueprint(job_bp, url_prefix='/api')
    
    # ######### tables
    with app.app_context():
        db.create_all()
    @app.route('/')
    def home():
        return {"message": "Job Board API is running Now"}

    
    return app

if __name__ == '__main__':
    app = create_app()
    print(" Flask backend running on http://localhost:5000")
    print(" API available at http://localhost:5000/api/jobs")
    app.run(debug=True, port=5000)