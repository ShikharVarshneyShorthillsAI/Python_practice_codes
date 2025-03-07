from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HackerRankSolver:
    def __init__(self,url):
        self.scraper = webdriver.Chrome()
        self.url = url

    def gotohackerrank(self):
        self.scraper.get(self.url)
        # WebDriverWait(self.scraper, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "c-lmpoFR c-lmpoFR-bRcXDr-underline-hover c-lmpoFR-ijfCDXL-css")))

        a_tags = self.scraper.find_elements(By.TAG_NAME,"a")
        for i in a_tags:
            if i.get_attribute("class") == "c-lmpoFR c-lmpoFR-bRcXDr-underline-hover c-lmpoFR-ijfCDXL-css":
                login_tag = i
                print(i.text)

        print(login_tag.get_attribute("class"))        
        login_tag.click()


        # filling out the username
        input_tags = self.scraper.find_elements(By.TAG_NAME,"input")
        
        for i in input_tags:
            name = i.get_attribute("name")
            if name == "username":
                username_tag = i
            
            elif name == "password":
                password_tag = i

            # print(i.get_attribute("name"))
        
        print(username_tag.get_attribute("name"))
        username_tag.send_keys("shikharvarshney150400@gmail.com")

        password_tag.send_keys("Shikhar@789")

        submit_buttons = self.scraper.find_elements(By.TAG_NAME,"button")
        for i in submit_buttons:
            if i.get_attribute("class") == "c-cUYkx c-cUYkx-dshqME-variant-primary c-cUYkx-fGHEql-isFullWidth-true c-cUYkx-ABeol-size-large hr-inline-flex hr-justify-center hr-align-center hr-p-y-1" and i.text=="Log In":
                last_login_button = i
                break

        print(last_login_button.get_attribute("class"))
        last_login_button.click()

        button_tags = self.scraper.find_elements(By.TAG_NAME,"button")
        for i in button_tags:
            if i.get_attribute("class") == "ui-btn ui-btn-normal ui-btn-secondary upload-file mlR ui-btn-styled":
                upload_code_tag = i
                break

        print(upload_code_tag.get_attribute("class"))
        self.scraper.execute_script("arguments[0].click()",upload_code_tag)

        print("sdfsfsdfsdf")


        confirm_tags = self.scraper.find_elements(By.TAG_NAME,"button")
        for i in confirm_tags:
            if i.get_attribute("class") == "ui-btn ui-btn-normal ui-btn-primary confirm-button ui-btn-styled":

                confirm_yes_tag = i
                break

        print(confirm_yes_tag.get_attribute("class"))
        confirm_yes_tag.click()

        input_file_sources = self.scraper.find_elements(By.TAG_NAME,"input")
        for i in input_file_sources:
            if i.get_attribute("class") == "d-none":
                input_file_source = i

        
        print(input_file_source.get_attribute("class"))
        input_file_source.send_keys("/home/shtlp_0042/Desktop/test.c")

        # print(input_file_source.get_attribute("readonly"))


        submit_buttons= self.scraper.find_elements(By.TAG_NAME,"button")
        for i in submit_buttons:
            if i.text == "Upload":
                submit_button = i
                break

        print(submit_button.get_attribute("class"))
        print(submit_button.text)
        submit_button.click()

        submit_buttons = self.scraper.find_elements(By.TAG_NAME,"button")
        for i in submit_buttons:
            if i.get_attribute("class")=="ui-btn ui-btn-normal ui-btn-primary pull-right hr-monaco-submit ui-btn-styled" and i.text == "Submit Code":
                submit_button = i
        
        submit_button.click()

        pass
    
    def close_browser(self):
        self.scraper.quit()



obj = HackerRankSolver("https://www.hackerrank.com/challenges/sum-numbers-c/problem?isFullScreen=true")
obj.gotohackerrank()
time.sleep(5)
obj.close_browser()

