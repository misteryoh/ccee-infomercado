import os
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class SeleniumDriver:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __init__(self, driver_path:str=None, binary_path:str=None, download_path:str=None):
        
        """SeleniumDriver constructor, returns a headless Webdriver instance

        :param driver_path (Optional): Browser driver path
        :param download_path (Optional): Download folder path
        """
        prefs = {
            'download.default_directory': download_path
        }

        self.driver = None
        self.driver_path = driver_path if driver_path is not None else None
        self.binary_path = binary_path if binary_path is not None else None
        self.prefs = prefs if download_path is not None else None

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("prefs", self.prefs)
        options.binary_location = self.binary_path

        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
            
    def get_session(self):

        return self.driver
    
    def download_files(self, download_url:str):

        """Download a file from indicated URL 

        :param download_url (Optional): Download URL
        """

        self.driver.get(download_url)
        time.sleep(10)
        #content_disposition = self.driver.execute_script("return window.performance.getEntries()[0].responseHeaders.filter(header => header.name === 'Content-Disposition')[0].value")
        #filename = content_disposition.split('filename=')[1].strip('"')
        #print(filename)

        #return filename

