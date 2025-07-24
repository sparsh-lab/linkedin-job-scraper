from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pickle, json, os, time, csv
from bs4 import BeautifulSoup
from datetime import datetime

# Load LinkedIn credentials
with open("scr/config.json", "r") as f:
    config = json.load(f)
    username = config.get("username")
    password = config.get("password")

# Setup WebDriver
driver = webdriver.Chrome()
driver.implicitly_wait(5)

# Cookie-based login
def load_cookies():
    if os.path.exists("cookies.pkl") and os.path.getsize("cookies.pkl") > 0:
        driver.get("https://www.linkedin.com/")
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                cookie.pop("sameSite", None)
                cookie.pop("expiry", None)
                driver.add_cookie(cookie)
        driver.get("https://www.linkedin.com/feed")
        time.sleep(3)
        return "feed" in driver.current_url
    return False

def manual_login(username, password):
    driver.get("https://www.linkedin.com/login")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()
        time.sleep(5)
    except Exception as e:
        print(f"❌ Login error: {e}")

def save_cookies():
    with open("cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("✅ Cookies saved.")

if load_cookies():
    print("✅ Logged in using cookies!")
else:
    print("🔐 Logging in manually...")
    manual_login(username, password)

driver.refresh()
time.sleep(2)

if "feed" in driver.current_url:
    print("✅ Login successful.")
    save_cookies()
else:
    print("❌ Login failed.")
    driver.quit()
    exit()

# Job Search Function
def search_jobs(job_title, location):
    driver.get("https://www.linkedin.com/jobs/search/")

        # Wait until keyword input is visible and interactable
    keyword_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']"))
        )
    keyword_input.click()
    keyword_input.clear()
    keyword_input.send_keys(job_title)

        # Wait until location input is ready
    location_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']"))
        )
    location_input.click()
    location_input.clear()
    location_input.send_keys(location)

    button = driver.find_element(By.CSS_SELECTOR, "button.jobs-search-box__submit-button")
    button.click()
    time.sleep(5)
    print(f"✅ Searching for '{job_title}' jobs in '{location}'")


search_jobs("Software Engineer", "India")
results = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")

# Scroll through job listings
def safe_linkedin_scroll():
    """Safe LinkedIn job scrolling - ONLY use this function"""
    print("🔄 Starting safe LinkedIn scroll...")
    
    # Method 1: Gentle page scrolling (this worked for you!)
    try:
        for i in range(5):  # Scroll more to load more jobs
            driver.execute_script("window.scrollBy(0, 400);")
            print(f"📜 Scrolled {400 * (i+1)}px")
            time.sleep(2)  # Wait for jobs to load
        print("✅ Page scroll complete!")
    except Exception as e:
        print(f"⚠️ Page scroll failed: {e}")
        return False
    
    # Method 2: Try to scroll job container if it exists
    try:
        job_container = driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list")
        print("📋 Found job container, scrolling...")
        
        for i in range(3):
            driver.execute_script("arguments[0].scrollTop += 300;", job_container)
            print(f"📜 Container scroll {i+1}/3")
            time.sleep(1)
            
    except Exception as e:
        print(f"ℹ️ Container scroll not available: {e}")
    
    print("🎉 LinkedIn scroll complete!")
    return True

# ONLY run this - ignore any other scroll functions
safe_linkedin_scroll()

# Enhanced job scraping with multiple selectors and error handling
def scrape_linkedin_jobs_with_soup():
    """Enhanced LinkedIn job scraping using Beautiful Soup"""
    print("🍜 Starting job scraping with Beautiful Soup...")
    
    try:
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        print("✅ Page parsed with Beautiful Soup")
        
        # Try multiple selectors to find job containers
        job_selectors = [
            '.job-card-container',
            '.job-card-list',
            '[data-job-id]',
            '.jobs-search-results__list-item',
            '.scaffold-layout__list-item',
            'li[data-occludable-job-id]'
        ]
        
        jobs = []
        for selector in job_selectors:
            jobs = soup.select(selector)
            if jobs:
                print(f"✅ Found {len(jobs)} jobs using selector: {selector}")
                break
        
        if not jobs:
            print("⚠️ No jobs found. Trying to find any job-related elements...")
            # Fallback: look for any elements with "job" in class name
            jobs = soup.find_all(attrs={'class': lambda x: x and 'job' in str(x).lower()})
            print(f"ℹ️ Found {len(jobs)} potential job elements as fallback")
        
        if not jobs:
            print("❌ No job listings found")
            return
        
        # Create timestamped CSV file
        filename = f'linkedin_jobs.csv'
        
        with open(filename, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "NO", "Job Title", "Company", "Location", "Link", 
                "Posted Date", "Job Type", "Scraped At"
            ])
            
            successful_scrapes = 0
            
            for i, job in enumerate(jobs):
                try:
                    # Extract job title
                    job_title = extract_text_soup(job, [
                        '.job-card-list__title',
                        '.job-card-container__link',
                        'h3 a',
                        '.job-title a',
                        '[data-control-name="job_search_job_title"]',
                        'a[data-control-name*="job_title"]'
                    ])
                    
                    # Extract company
                    company = extract_text_soup(job, [
                        '.job-card-container__company-name',
                        '.job-card-list__company-name',
                        'h4 a',
                        '.company-name',
                        '[data-control-name="job_search_company_name"]',
                        'a[data-control-name*="company"]'
                    ])
                    
                    # Extract location
                    location = extract_text_soup(job, [
                        '.job-card-container__metadata-item',
                        '.job-card-list__metadata',
                        '.job-card-container__metadata',
                        '.job-location',
                        '[data-test="job-location"]'
                    ])
                    
                    # Extract job link
                    link = extract_link_soup(job, [
                        'a[data-control-name*="job_title"]',
                        'a[href*="/jobs/view/"]',
                        '.job-card-container__link',
                        '.job-card-list__title a',
                        'h3 a'
                    ])
                    
                    # Extract posted date
                    posted_date = extract_text_soup(job, [
                        '.job-card-container__listed-status',
                        '.job-card-list__posted-date',
                        'time',
                        '[data-test="job-posted-date"]'
                    ], required=False) or "NULL"
                    
                    # Extract job type
                    job_type = extract_text_soup(job, [
                        '.job-card-container__job-insight',
                        '.job-card-list__job-insight',
                        '[data-test="job-type"]'
                    ], required=False) or "NULL"
                    
                    # Clean up the data
                    job_title = clean_text(job_title)
                    company = clean_text(company)
                    location = clean_text(location)
                    
                    # Save ALL jobs - use "NULL" for missing fields
                    job_title = job_title or "NULL"
                    company = company or "NULL" 
                    location = location or "NULL"
                    link = link or "NULL"
                    posted_date = posted_date or "NULL"
                    job_type = job_type or "NULL"
                    
                    writer.writerow([
                        i + 1, job_title, company, location, link,
                        posted_date, job_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ])
                    print(f"✅ {i + 1}: {job_title} at {company} in {location}")
                    successful_scrapes += 1
                        
                except Exception as e:
                    print(f"⚠️ Error scraping job {i+1}: {e}")
                    continue
            
            print(f"🎉 Successfully scraped {successful_scrapes}/{len(jobs)} jobs")
            print(f"📁 Saved to: {filename}")
            
    except Exception as e:
        print(f"❌ Beautiful Soup scraping failed: {e}")

def extract_text_soup(job_element, selectors, required=True):
    """Extract text using multiple CSS selectors with Beautiful Soup"""
    for selector in selectors:
        try:
            element = job_element.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        except Exception as e:
            continue
    
    if required:
        print(f"⚠️ Could not find element with selectors: {selectors}")
    return ""

def extract_link_soup(job_element, selectors):
    """Extract href attribute using multiple CSS selectors"""
    for selector in selectors:
        try:
            element = job_element.select_one(selector)
            if element and element.get('href'):
                href = element.get('href')
                # Make sure it's a full URL
                if href.startswith('/'):
                    href = 'https://www.linkedin.com' + href
                return href
        except Exception as e:
            continue
    return "NULL"  # Return NULL instead of "No link found"

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    
    # Remove common unwanted characters
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    return text.strip()

def debug_job_structure():
    """Debug function to see the HTML structure of jobs"""
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find any element that might contain jobs
        potential_jobs = soup.find_all(attrs={'class': lambda x: x and 'job' in str(x).lower()})[:3]
        
        print("🔍 DEBUG: First 3 job-related elements found:")
        for i, job in enumerate(potential_jobs):
            print(f"\n--- Job Element {i+1} ---")
            print(f"Tag: {job.name}")
            print(f"Classes: {job.get('class', [])}")
            print(f"Text preview: {job.get_text()[:100]}...")
            
            # Look for links
            links = job.find_all('a')
            print(f"Links found: {len(links)}")
            for link in links[:2]:  # Show first 2 links
                print(f"  - {link.get('href', 'No href')} | Text: {link.get_text()[:50]}")
            
    except Exception as e:
        print(f"❌ Debug failed: {e}")

# Run the Beautiful Soup scraper
scrape_linkedin_jobs_with_soup()

# Uncomment to debug HTML structure if needed
# debug_job_structure()



driver.quit()
