# 🔗 LinkedIn Job Scraper

## 📄 Abstract
The LinkedIn Job Scraper is a Python-based automation tool designed to streamline the job search process by extracting job listings directly from LinkedIn. Utilizing Selenium for browser automation and BeautifulSoup for data parsing, the system searches for jobs based on user-defined keywords and location, collects essential job details, and exports the results into a CSV file. It also includes duplicate removal and generates a visual graph of job frequency by company.

---

## 🎯 Objective
Automate the extraction of job listings from LinkedIn using Python tools, store them in a structured format, clean duplicates, and visualize hiring trends.

---

## 🧰 Tools & Technologies Used

| Tool / Library       | Purpose                                           |
|----------------------|---------------------------------------------------|
| **Python**           | Core scripting language                           |
| **Selenium**         | Automate LinkedIn login and job search actions    |
| **BeautifulSoup**    | Extract job data from HTML content                |
| **pandas**           | Data cleaning, structuring, and CSV handling      |
| **matplotlib/seaborn** | Visualize job frequency per company            |
| **ChromeDriver**     | Required for running Selenium with Chrome         |
| **python-dotenv** *(optional)* | Secure login credentials from `.env` file |

---

## 🪜 Steps Involved

1. **Set up Environment**  
   Install dependencies and configure ChromeDriver.

2. **Login to LinkedIn**  
   Automate login using Selenium.

3. **Search for Jobs**  
   Input job title and location using Selenium.

4. **Scrape Job Data**  
   Extract title, company, location, and date using BeautifulSoup.

5. **Save to CSV**  
   Export structured data to `linkedin_jobs.csv`.

6. **Remove Duplicates**  
   Clean duplicate entries using `pandas.drop_duplicates()`.

7. **Visualize Results**  
   Plot company-wise job frequency using `matplotlib` or `seaborn`.

---

## 📂 Project Files

| File Name                    | Description                                                   |
|-----------------------------|---------------------------------------------------------------|
| `linkedin_scraper.py`       | Main script for automation and scraping                       |
| `requirements.txt`          | Required libraries for the project                            |
| `linkedin_jobs.csv`         | Output CSV containing scraped job listings                    |
| `job_frequency_by_company.png` | Visualization of job postings per company                |
| `README.md`                 | Project documentation                                         |
| `.env` *(optional)*         | Stores secure LinkedIn credentials                           |
| `utils.py` *(optional)*     | Helper functions (cleaning, visualization, etc.)              |

---

## ✅ Conclusion
The LinkedIn Job Scraper automates the job search workflow, extracts and organizes real-time job listings, removes redundancy, and visualizes trends — making it an efficient tool for data-driven job seekers and analysts.

---

## 🚀 Future Improvements
- Add pagination to scrape multiple pages
- Schedule periodic scraping (daily/weekly)
- Export to Excel or Google Sheets
- Add filters (remote jobs, company size, etc.)

---

## 📌 Note
This tool is for educational and personal use only. Be mindful of LinkedIn's Terms of Service when scraping data.

---
