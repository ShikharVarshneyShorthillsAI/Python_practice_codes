import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class CourseScraper:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.url = url
        self.course_data = []
    
    def open_page(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    def scrape_courses(self):
        table_rows = self.driver.find_elements(By.TAG_NAME, 'tr')
        print(f"Number of rows in the table: {len(table_rows)}")
        
        for row in table_rows:
            tds = row.find_elements(By.TAG_NAME, 'td')
            if len(tds) > 3:
                course_name = tds[1].text
                course_code = tds[3].text
                print(f"Course name: {course_name}, Course code: {course_code}")
                self.course_data.append({"course_name": course_name, "course_code": course_code})
    
    def save_to_json(self, filename="courses.json"):
        with open(filename, "w") as file:
            json.dump(self.course_data, file, indent=4)
        print(f"Course data saved to {filename}")
    
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = CourseScraper("https://techtree.iiitd.edu.in/")
    scraper.open_page()
    scraper.scrape_courses()
    scraper.save_to_json()
    scraper.close()
