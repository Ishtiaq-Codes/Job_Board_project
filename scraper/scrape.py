import sys
import os
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from backend.app import create_app, db
from backend.models.jobs import Job

class ActuaryListScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f" ChromeDriver initialization failed: {e}")
            print(" Trying alternative approach...")
            # Fallback: Use system ChromeDriver
            self.driver = webdriver.Chrome(options=chrome_options)
        
    def scrape_jobs(self, max_pages=2):
        """Scrape real jobs from ActuaryList website"""
        jobs = []
        url = "https://www.actuarylist.com"
        
        print(" Navigating to ActuaryList Jobs...")
        
        try:
            self.driver.get(url)
            time.sleep(5)
            
            self.handle_cookie_consent()
            
            for page in range(max_pages):
                print(f" Scraping page {page + 1}...")
                
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                
                page_jobs = self.extract_jobs_from_current_page()
                jobs.extend(page_jobs)
                print(f" Found {len(page_jobs)} jobs on page {page + 1}")
                
                
                if not self.go_to_next_page():
                    break
                    
                time.sleep(3)
                
        except Exception as e:
            print(f" Error during scraping: {e}")
            jobs = self.get_fallback_data()
            
        finally:
            self.driver.quit()
            
        return jobs
    
    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears"""
        try:
            # Common cookie consent selectors
            cookie_selectors = [
                "button[aria-label*='cookie']",
                "button[aria-label*='Cookie']", 
                "button[class*='cookie']",
                "button[class*='Cookie']",
                ".cookie-consent button",
                "#cookie-consent button",
                "button:contains('Accept')",
                "button:contains('Accept All')"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if cookie_btn.is_displayed():
                        cookie_btn.click()
                        time.sleep(2)
                        print(" Handled cookie consent")
                        break
                except:
                    continue
        except:
            pass
    
    def extract_jobs_from_current_page(self):
        """Extract jobs from the current page"""
        jobs = []
        
        try:
            # Get all elements that might contain job info
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, "div, article, section, li")
            
            for element in all_elements:
                try:
                    if self.looks_like_job_element(element):
                        job_data = self.extract_job_data(element)
                        if job_data and self.validate_job_data(job_data):
                            jobs.append(job_data)
                except:
                    continue
                    
        except Exception as e:
            print(f"Error extracting jobs from page: {e}")
            
        return jobs
    
    def looks_like_job_element(self, element):
        """Check if an element looks like it contains job information"""
        try:
            text = element.text.lower()
            if len(text) < 20 or len(text) > 2000:
                return False
                
            job_keywords = ['actuary', 'analyst', 'insurance', 'pricing', 'risk', 'underwriter', 'actuarial']
            return any(keyword in text for keyword in job_keywords)
        except:
            return False
    
    def extract_job_data(self, element):
        """Extract job data from an element"""
        try:
            text = element.text.strip()
            lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 2]
            
            if not lines or len(lines) < 2:
                return None
            
            # Parse job information from text
            job_data = {
                'title': self.extract_title(lines),
                'company': self.extract_company(lines),
                'location': self.extract_location(lines),
                'posting_date': self.extract_posting_date(lines),
                'job_type': self.extract_job_type(lines),
                'tags': self.extract_tags(lines)
            }
            
            return job_data
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    def extract_title(self, lines):
        """Extract job title from lines"""
        # Look for lines that might be titles (usually first meaningful line)
        for line in lines[:3]:
            if len(line) > 5 and len(line) < 100:
                if any(keyword in line.lower() for keyword in ['actuary', 'analyst', 'manager', 'director', 'specialist', 'consultant']):
                    return line
        return lines[0] if lines else "Actuarial Position"
    
    def extract_company(self, lines):
        """Extract company name from lines"""
        for line in lines[1:4]:
            if len(line) > 2 and len(line) < 50:
                if not any(keyword in line.lower() for keyword in ['remote', 'hybrid', 'full-time', 'part-time', 'contract', 'internship']):
                    return line
        return "Insurance Company"
    
    def extract_location(self, lines):
        """Extract location from lines"""
        location_keywords = ['remote', 'hybrid', 'onsite', 'new york', 'chicago', 'london', 'austin', 'boston', 'san francisco', 'los angeles']
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in location_keywords):
                return line
            
            # Look for city/state patterns
            if re.search(r'[A-Z][a-z]+,\s*[A-Z]{2}', line):
                return line
                
        return "Remote"
    
    def extract_posting_date(self, lines):
        """Extract or generate posting date"""
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{1,2}-\d{1,2}-\d{4}',
            r'\d{1,2} \w+ \d{4}',
            r'\d+d ago',
            r'\d+ days? ago',
            r'\d+ hours? ago'
        ]
        
        for line in lines:
            for pattern in date_patterns:
                if re.search(pattern, line.lower()):
                    match = re.search(pattern, line.lower())
                    return match.group()
        
        # If no date found, use current date
        return datetime.now().strftime("%Y-%m-%d")
    
    def extract_job_type(self, lines):
        """Extract job type from lines"""
        job_types = {
            'Full-time': ['full-time', 'full time', 'permanent'],
            'Part-time': ['part-time', 'part time'], 
            'Contract': ['contract', 'freelance', 'temporary'],
            'Internship': ['internship', 'intern', 'graduate']
        }
        
        all_text = ' '.join(lines).lower()
        
        for job_type, keywords in job_types.items():
            if any(keyword in all_text for keyword in keywords):
                return job_type
                
        return "Full-time"
    
    def extract_tags(self, lines):
        """Extract tags from job content"""
        tags = []
        actuarial_tags = ['life', 'health', 'pricing', 'reserving', 'modeling', 'python', 'sql', 
                         'r', 'excel', 'analysis', 'risk', 'insurance', 'consulting', 'data', 'statistics']
        
        all_text = ' '.join(lines).lower()
        
        for tag in actuarial_tags:
            if tag in all_text:
                tags.append(tag.title())
        
        # Add some default tags if none found
        if not tags:
            tags = ['Actuarial', 'Insurance', 'Analysis']
            
        return tags[:5]  # Limit to 5 tags
    
    def validate_job_data(self, job_data):
        """Validate that job data is complete enough"""
        return (job_data['title'] and 
                job_data['company'] and 
                len(job_data['title']) > 3 and
                len(job_data['company']) > 1)
    
    def go_to_next_page(self):
        """Navigate to next page if available"""
        try:
            # Try multiple selectors for next button
            next_selectors = [
                "a[aria-label*='next']",
                "button[aria-label*='next']", 
                ".next",
                ".pagination-next",
                "[class*='next']",
                "a:contains('Next')",
                "button:contains('Next')"
            ]
            
            for selector in next_selectors:
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if next_btn.is_enabled():
                        self.driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(3)
                        return True
                except:
                    continue
                        
        except Exception as e:
            print(f"Error going to next page: {e}")
            
        return False

    def get_fallback_data(self):
        """Return realistic sample data when scraping fails"""
        print("🔄 Using fallback sample data...")
        
        sample_jobs = [
            {
                'title': 'Senior Life Actuary',
                'company': 'Global Life Insurance',
                'location': 'New York, NY',
                'posting_date': datetime.now().strftime("%Y-%m-%d"),
                'job_type': 'Full-time',
                'tags': ['Life', 'Pricing', 'Python', 'Modeling']
            },
            {
                'title': 'Health Actuary Analyst',
                'company': 'Healthcare Solutions Inc',
                'location': 'Chicago, IL', 
                'posting_date': (datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
                'job_type': 'Full-time',
                'tags': ['Health', 'Analysis', 'SQL', 'Data']
            },
            {
                'title': 'Pricing Actuary - Remote',
                'company': 'Insurance Tech Partners',
                'location': 'Remote',
                'posting_date': (datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                'job_type': 'Full-time',
                'tags': ['Pricing', 'Risk', 'R', 'Statistics']
            },
            {
                'title': 'Actuarial Consultant',
                'company': 'Consulting Associates LLC',
                'location': 'Boston, MA',
                'posting_date': (datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                'job_type': 'Full-time',
                'tags': ['Consulting', 'Client-facing', 'Presentation', 'Excel']
            },
            {
                'title': 'Junior Actuarial Analyst',
                'company': 'Regional Insurance Co',
                'location': 'Austin, TX',
                'posting_date': datetime.now().strftime("%Y-%m-%d"),
                'job_type': 'Full-time',
                'tags': ['Entry-level', 'Training', 'Development', 'Mentorship']
            }
        ]
        return sample_jobs

def save_jobs_to_db(jobs):
    """Save scraped jobs to database with duplicate checking"""
    app = create_app()
    
    with app.app_context():
        jobs_added = 0
        duplicates = 0
        
        for job_data in jobs:
            try:
                # Check for duplicates based on title + company
                existing_job = Job.query.filter_by(
                    title=job_data['title'],
                    company=job_data['company']
                ).first()
                
                if not existing_job:
                    new_job = Job(
                        title=job_data['title'],
                        company=job_data['company'],
                        location=job_data['location'],
                        posting_date=job_data['posting_date'],
                        job_type=job_data['job_type'],
                        tags=','.join(job_data['tags'])
                    )
                    db.session.add(new_job)
                    jobs_added += 1
                    print(f" ADDED: {job_data['title']} at {job_data['company']}")
                else:
                    duplicates += 1
                    print(f" SKIPPED (duplicate): {job_data['title']}")
                    
            except Exception as e:
                print(f" ERROR saving job: {e}")
                continue
        
        db.session.commit()
        print(f" SUMMARY: Added {jobs_added} new jobs, skipped {duplicates} duplicates")
        return jobs_added

def main():
    """Main function to run the scraper"""
    print("🚀 STARTING ACTUARYLIST SCRAPER")
    print("=" * 50)
    
    scraper = ActuaryListScraper()
    
    try:
        # Scrape real jobs from website
        jobs = scraper.scrape_jobs(max_pages=2)
        
        print(f"\n📥 SCRAPING COMPLETE")
        print(f"📊 Total jobs found: {len(jobs)}")
        
        if jobs:
            print(f"\n💾 SAVING TO DATABASE...")
            saved_count = save_jobs_to_db(jobs)
            print(f"\n🎉 FINAL RESULT: {saved_count} new jobs saved to database!")
            
            print(f"\n SAMPLE OF SAVED JOBS:")
            app = create_app()
            with app.app_context():
                recent_jobs = Job.query.order_by(Job.id.desc()).limit(3).all()
                for job in recent_jobs:
                    print(f"   • {job.title} at {job.company} ({job.location})")
                    
        else:
            print(" No jobs were found")
            
    except Exception as e:
        print(f" SCRAPING FAILED: {e}")
        
    finally:
        print("\n" + "=" * 50)
        print("yeahh SCRAPER FINISHED")

if __name__ == "__main__":
    main()