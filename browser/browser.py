import sys


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import os 


class Browser:
    def __init__(self,headless = True,test = False,remote_driver = True,
                 remote_address = "browser", remote_port=4444,use_cookies = False,
                 profile_path = "", default_timeout = 5):
        self.testing = test
        self.chrome_options = webdriver.ChromeOptions()
        self.use_cookies = use_cookies
        self.profile_path = profile_path
        self.default_timeout = default_timeout


        #Chrome options 
        if sys.platform == "win32":
            prefs = {"profile.default_content_settings.popups": 0,    
            "download.prompt_for_download": False,
            "download.directory_upgrade": False}
            self.chrome_options.add_experimental_option("prefs",prefs)

        if headless:
            self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument('--ignore-ssl-errors=yes')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument('--disable-dev-shm-usage')        
        self.chrome_options.add_experimental_option('excludeSwitches',
                                                     ['enable-logging'])
        
        if self.profile_path != "":
            print("profile path",self.profile_path)
            os.makedirs(self.profile_path, exist_ok=True)
            self.chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
            # self.chrome_options.add_argument(f"--profile-directory={self.profile_path}")
        if remote_driver:
            self.driver = webdriver.Remote(command_executor=f'http://{remote_address}:{remote_port}/wd/hub',options=self.chrome_options)
        else:
            self.driver = webdriver.Chrome(service=ChromeDriverManager().install(), # type: ignore  # noqa: E501
                                           options=self.chrome_options) 
            
        self.driver.implicitly_wait(5)

    def find_elements(self,by, value, timeout=5):
        #set timeout
        self.driver.implicitly_wait(timeout)
        #find elements
        elements = self.driver.find_elements(by,value )
        #reset timeout to default
        self.driver.implicitly_wait(self.default_timeout)
        if len(elements) > 0:
            return elements[0]
        return None
    
    def wait_for_element(self,by, element_id, timeout=5):
        '''wait for element to be clickable
            returns the element if found
        '''
        wait = WebDriverWait(self.driver, timeout)
        #wait for the bubble to disappear
        ret = wait.until(EC.element_to_be_clickable((by, element_id)))

        if ret is not None:
            return ret
        return None
    

                
    def close(self):
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception:
                # console.print_exception(show_locals=True)
                pass


    def __del__(self):
        self.close()

    def get_downloads_list(self) -> list:
        if not self.driver.current_url.startswith("chrome://downloads"):
            self.driver.get("chrome://downloads/")
        for i in range(3):

            files =  self.driver.execute_script( \
            "return  document.querySelector('downloads-manager')  "
            " .shadowRoot.querySelector('#downloadsList')         "
            " .items.filter(e => e.state === 'COMPLETE')          "
            " .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url); "
            )
            if len(files) > 0:
                return files
        return []

    def execute_script(self,script):
        return self.driver.execute_script(script)

    def click_button(self, button_id):
        #search for all buttons
        buttons = self.driver.find_elements(By.XPATH, button_id)
        if len(buttons) > 0:
            #click the first button
            buttons[0].click()
            return True
        return False
    