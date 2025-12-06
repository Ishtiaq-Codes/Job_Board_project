# 🎯 Actuary Job Board - Full Stack Application

## 📋 Project Overview

This is a complete full-stack job listing web application built for Bitbash's technical assessment. The application displays actuarial job postings with advanced filtering, sorting, and management capabilities, integrating data scraped from the Actuary List website.

**Video Recording link (Explaning Architecture and code of Web App )**
https://drive.google.com/file/d/13PT0PzmexqlIqtSQc4cFznmV21Qpg-ow/view?usp=sharing)

---

## 🚀 Features

### 🔧 Backend (Flask API)
- **RESTful API** with complete CRUD operations
- **PostgreSQL database** with SQLAlchemy ORM
- **Advanced filtering** by job type, location, tags, and search
- **Multiple sorting options** (date, title, company)
- **Input validation** and comprehensive error handling
- **CORS configured** for frontend communication

### ⚛️ Frontend (React)
- **Professional job listings** with card-based design
- **Add, edit, and delete** job functionality
- **Real-time filtering** and sorting
- **Responsive design** for mobile and desktop
- **Form validation** and user feedback
- **Clean, modern UI** with Tailwind CSS

### 🤖 Web Scraping (Selenium)
- **Automated data collection** from ActuaryList.com
- **Duplicate prevention** with smart checks
- **Error handling** for robust operation
- **Production-ready** with fallback mechanisms

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask, SQLAlchemy, PostgreSQL, Python |
| **Frontend** | React, Vite, Tailwind CSS, Context API |
| **Scraping** | Selenium, ChromeDriver, BeautifulSoup |
| **Deployment** | Render, Vercel, PostgreSQL |
| **Development** | Git, GitHub, Postman |

---

## 📁 Project Structure

```
job-board-app/
├── 📂 backend/
│   ├── app.py                 # Main Flask application
│   ├── models/
│   │   └── job.py            # SQLAlchemy Job model
│   ├── routes/
│   │   └── job_routes.py     # API endpoints
│   ├── db.py                 # Database configuration
│   ├── config.py             # Environment configuration
│   ├── requirements.txt      # Python dependencies
│   └── wsgi.py              # Production WSGI entry point
├── 📂 frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── JobList.jsx
│   │   │   ├── JobCard.jsx
│   │   │   ├── JobForm.jsx
│   │   │   ├── FilterBar.jsx
│   │   │   ├── SearchBox.jsx
│   │   │   ├── DropdownFilter.jsx
│   │   │   └── SortDropdown.jsx
│   │   ├── context/
│   │   │   └── JobContext.jsx # State management
│   │   ├── utils/
│   │   │   └── api.js        # API communication
│   │   ├── App.jsx           # Main application
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── 📂 scraper/
│   ├── scrape.py             # Selenium scraper
│   └── requirements.txt      # Scraper dependencies
└── 📄 README.md
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (or SQLite for development)
- Chrome browser (for scraper)

### 🏃‍♂️ Local Development

#### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database configuration

# Run the application
python app.py
```
Backend runs on: `http://localhost:5000`

#### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend runs on: `http://localhost:5173`

#### 3. Scraper Setup
```bash
cd scraper

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scrape.py
```

---

## 📊 API Documentation

### Base URL
`http://localhost:5000/api` (development)  
`https://your-backend.onrender.com/api` (production)

### Endpoints

#### 🟢 GET /jobs
Retrieve all jobs with optional filtering and sorting.

**Query Parameters:**
- `job_type` - Filter by job type (Full-time, Part-time, etc.)
- `location` - Filter by location
- `tag` - Filter by tag
- `search` - Search in title and company
- `sort` - Sort order (posting_date_desc, posting_date_asc, title_asc, etc.)

**Example:**
```bash
GET /api/jobs?job_type=Full-time&location=Remote&sort=posting_date_desc
```

#### 🟡 POST /jobs
Create a new job listing.

**Request Body:**
```json
{
  "title": "Senior Actuarial Analyst",
  "company": "Insurance Corp",
  "location": "New York, NY",
  "posting_date": "2024-01-15",
  "job_type": "Full-time",
  "tags": ["Life", "Pricing", "Python"]
}
```

#### 🔵 GET /jobs/{id}
Retrieve a specific job by ID.

#### 🟠 PUT /jobs/{id}
Update an existing job.

#### 🔴 DELETE /jobs/{id}
Delete a job by ID.

---

## 🎨 Frontend Components

### JobCard
Displays individual job listings with:
- Job title, company, location
- Posting date and job type
- Interactive tags
- Edit and delete actions

### JobForm
Handles job creation and editing with:
- Form validation for required fields
- Error message display
- Loading states during submission
- Pre-filled data for edits

### FilterBar
Advanced filtering interface with:
- Keyword search across titles and companies
- Dropdown filters for job type and location
- Tag-based filtering
- Sort controls with multiple options
- Active filter indicators and reset functionality

### JobList
Main container component that:
- Fetches and displays job data
- Handles loading and error states
- Manages responsive grid layout

---

## 🤖 Scraper Implementation

The Selenium scraper automatically collects job data from ActuaryList.com:

### Features
- **Dynamic content handling** with explicit waits
- **Popup and cookie consent management**
- **Duplicate detection** before saving
- **Error resilience** with fallback data
- **Production optimization** with headless mode

### Usage
```python
from scraper import ActuaryListScraper

scraper = ActuaryListScraper()
jobs = scraper.scrape_jobs(max_pages=2)
```

### Manual Testing Checklist
- [ ] API endpoints respond correctly
- [ ] CRUD operations work as expected
- [ ] Filtering and sorting function properly
- [ ] Form validation shows appropriate errors
- [ ] Responsive design works on mobile/desktop
- [ ] Scraper successfully collects and saves jobs
- [ ] Error handling displays user-friendly messages

### API Testing with curl
```bash
# Get all jobs
curl http://localhost:5000/api/jobs

# Create a job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Job","company":"Test Co","location":"Test"}'

# Filter jobs
curl "http://localhost:5000/api/jobs?job_type=Full-time&location=Remote"
```

---

## 🐛 Troubleshooting

### Common Issues

**CORS Errors:**
- Ensure Flask-CORS is properly configured
- Check frontend API base URL matches backend

**Database Connection:**
- Verify PostgreSQL is running
- Check DATABASE_URL environment variable
- Ensure database tables are created

**Scraper Failures:**
- Update ChromeDriver to match Chrome version
- Check website structure hasn't changed
- Verify internet connection

**Frontend Build Issues:**
- Clear node_modules and reinstall dependencies
- Check Node.js version compatibility
- Verify environment variables are set

---

## 📝 Assumptions & Trade-offs

### Design Decisions
1. **Mono-repository structure** for better code organization and deployment
2. **SQLite for development**, PostgreSQL for production for ease of setup
3. **Context API** for state management instead of Redux for simplicity
4. **Server-side filtering** preferred over client-side for real-time data
5. **Comma-separated tags** in database with array conversion in API

### Scope Limitations
- No user authentication (out of project scope)
- Basic error handling without detailed logging
- Simple pagination instead of infinite scroll
- No job application tracking system

### Future Enhancements
- User authentication and authorization
- Advanced search with saved filters
- Job application tracking
- Email notifications for new jobs
- Admin dashboard for content management

---

## 👨‍💻 Development Notes

### Code Quality
- Follows PEP 8 for Python code style
- Uses ESLint and Prettier for JavaScript
- Modular component structure in React
- Proper error handling and validation
- Comprehensive code comments

### Performance Considerations
- Database indexing on frequently filtered columns
- Efficient React re-renders with proper state management
- Lazy loading for large job lists
- Optimized database queries with SQLAlchemy

### Security Measures
- Input validation on all API endpoints
- SQL injection prevention with ORM
- CORS configuration for production
- Environment variable protection

---

## 📞 Support

For questions or issues with this project:

1. Check the troubleshooting section above
2. Review API documentation for endpoint details
3. Examine error messages in browser console and server logs
4. Contact: [hfizitq@gmail.com] 

---

## 📄 License

This project was developed as part of a technical assessment for Bitbash. All code is available for review and evaluation purposes.

---

## 🎯 Project Compliance

✅ **All PDF Requirements Met**
- Complete Flask REST API with CRUD operations
- SQLAlchemy database integration  
- React frontend with professional UI
- Selenium web scraping implementation
- Filtering, sorting, and validation
- Responsive design and error handling
- Proper documentation and deployment

**Ready for production use and technical evaluation!** 🚀

---

*Last Updated: [7-12-2025]*  
*Built with ❤️ for Bitbash Technical Assessment*
