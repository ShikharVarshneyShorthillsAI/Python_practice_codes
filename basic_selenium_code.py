from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumScraper:
    def __init__(self, url):
        """Initialize the WebDriver and open the given URL."""
        self.driver = webdriver.Chrome()  # Initialize ChromeDriver
        self.url = url

    def open_page(self):
        """Opens the webpage and waits for it to fully load."""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def get_all_links(self):
        """Fetches all links (<a> tags) on the webpage."""
        links = self.driver.find_elements(By.TAG_NAME, "a")  # Get all <a> elements
        return [link.get_attribute("href") for link in links if link.get_attribute("href")]

    def close_browser(self):
        """Closes the browser session."""
        self.driver.quit()

# Usage
if __name__ == "__main__":
    url = "https://techtree.iiitd.edu.in/"  # Change this to the website you want to scrape
    scraper = SeleniumScraper(url)
    
    scraper.open_page()
    links = scraper.get_all_links()

    print("Extracted Links:")
    for link in links:
        print(link)

    scraper.close_browser()
