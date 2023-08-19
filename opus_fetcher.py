import undetected_chromedriver as chromedriver
from undetected_chromedriver import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
from fp.fp import FreeProxy
from loguru import logger
import random
import mail_system, yogopy

######################################################################
#timeout should be high for slow proxies such as the free ones i used#
TIMEOUT = 20#30 #in seconds(rec. for paid: 20, rec. for free: 30)#####
PROXY_TYPE = "paid"#"free" options are: "paid"(recommended) or "free"#
PAID_PROXY_BACKBONE = "p.webshare.io:9999"#leave blank for free proxy#
DO_SLEEP = True#leave true for most uses, changing to false sometimes#
#raises unwanted exceptions###########################################
######################################################################



def search_for_element_and_click(browser ,by, selector, _=None):
    while True:
        try:
            element = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((by, selector)))
            if DO_SLEEP: time.sleep(2+(random.randint(0,200)/100))
            element.click()
            break
        except TimeoutException:
            pass


    

def search_for_element_and_send_keys(browser ,by, selector, input_):
    while True:
        try:
            element = WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((by, selector)))
            if DO_SLEEP: time.sleep(2+(random.randint(0,200)/100))
            element.click()
            element.send_keys(input_)
            break
        except TimeoutException:
            pass
    

class Fetcher:
    def __init__(self):
        logger.debug("[OPUS_FETCHER.PY] running with the following settings: TIMEOUT = "+str(TIMEOUT)+", PROXY_TYPE="+str(PROXY_TYPE)+", PAID_PROXY_BACKBONE="+str(PAID_PROXY_BACKBONE)+", DO_SLEEP="+str(DO_SLEEP))
        count = 1
        self.wish = None
        self.email = "moms-are-hot999@yopmail.com"

        while True:
            try:
                
                # proxy type selecion execution
                if PROXY_TYPE == "free":
                    self.proxy = FreeProxy(timeout=3).get()
                elif PROXY_TYPE == "paid":
                    self.proxy = PAID_PROXY_BACKBONE

                # setting up browser
                self.opt = Options()
                self.opt.add_argument("--proxy-server="+self.proxy)

                self.driver = chromedriver.Chrome(headless=False,use_subprocess=False, options=self.opt)
                self.driver.get('https://clip.opus.pro/dashboard?utm_source=opus')
                
                frame = WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "app-iframe")))
                self.driver.switch_to.frame(frame)
                
                break
            except TimeoutException:
                logger.info("Bad proxy! Searching for new one...("+str(count)+")"); count+=1
                self.driver.close()
                time.sleep(1)

    def register_step_1(self, email):
        self.email = email
        #insert email
        search_for_element_and_send_keys(self.driver, By.ID, ':r0:', email)
        #Click submit button
        search_for_element_and_click(self.driver, By.CSS_SELECTOR,'button.MuiButtonBase-root:nth-child(3)')
    
    def register_step_2(self, code, yt_link, lenght="30s~60s"):
        if not lenght == "Auto" and not lenght == "<30s" and not lenght == "30s~60s" and not lenght == "60s~90s" and not lenght == "90s~3m":
            raise Exception("Lenght attribute is not correct, allowed strings are: Auto, <30s, 30s~60s, 60s~90s, 90s~3m.")

        #Insert email code
        search_for_element_and_send_keys(self.driver, By.ID, ':r3:', code)
        #Click on submit button
        search_for_element_and_click(self.driver, By.CSS_SELECTOR,'button.MuiButtonBase-root:nth-child(4)')
        #Check if ip had been blocked
        time.sleep(3)
        try:
            element = WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Refresh"]')))
            element.click()
            self.wish = "IP Blocked! "
            self.driver.close()
            raise Exception("IP Blocked")
        except TimeoutException:
            pass
        """
        try:
            element = WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(.,'Looks like you're connecting through a VPN')]]")))
            element.click()
            self.wish = "IP Blocked! "
            self.driver.close()
            raise Exception("IP Blocked")
        except TimeoutException:
            pass"""
        
        #Click on free trial acceptance button
        search_for_element_and_click(self.driver, By.XPATH, '//button[text()="Start clipping"]')
        #insert yt link
        search_for_element_and_send_keys(self.driver, By.ID, ':r5:', yt_link)
        #Select lenght
        search_for_element_and_click(self.driver, By.XPATH, '//button[text()="'+lenght+'"]')
        #Click on submit button
        search_for_element_and_click(self.driver, By.XPATH, '//*[@id="__next"]/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/button')
        time.sleep(10)
        logger.info('Tracking url: '+self.driver.current_url)
        self.driver.close()
    
    def download_videos(self, url, headless=False):
        #/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[VAR]/div[2]/div/div/div/div/div[2]/div[2]/button
        self.opt = Options()
        self.opt.add_argument("--proxy-server="+self.proxy)

        self.driver = chromedriver.Chrome(headless=headless, use_subprocess=False, options=self.opt)
        self.driver.get(url)

        
        search_for_element_and_click(self.driver, By.XPATH, '//p[text()="Have questions?"]')
        time.sleep(5)
        search_for_element_and_click(self.driver, By.XPATH, '//p[text()="Have questions?"]')

        time.sleep(3)
        search_for_element_and_click(self.driver, By.XPATH, '//button[text()="Download"]')

        frame = WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "app-iframe")))
        self.driver.switch_to.frame(frame)

        self.register_step_1(self.email)
        time.sleep(1)
        inbox = yogopy.YogoInbox(self.email)
        code = inbox.listen_for_verification_code()
        time.sleep(2)

        #Insert email code
        search_for_element_and_send_keys(self.driver, By.ID, ':r3:', code)
        #Click on submit button
        search_for_element_and_click(self.driver, By.CSS_SELECTOR,'button.MuiButtonBase-root:nth-child(4)')

        #Check if ip had been blocked
        try:
            element = WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Refresh"]')))
            element.click()
            self.wish = "IP Blocked!"
            self.driver.close()
            raise Exception("IP Blocked")
        except TimeoutException:
            pass
        
        #Scroll down to load dynamic content
        time.sleep(5)
        for i in range(1,50):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        while True:
            try:
                _ = WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Download"]')))
                elements = self.driver.find_elements(By.XPATH, '//button[text()="Download"]')
                if DO_SLEEP: time.sleep(2+(random.randint(0,200)/100))
                for element in elements:
                    element.click()
                    if DO_SLEEP: time.sleep(5+(random.randint(0,200)/100))
                break
            except TimeoutException:
                pass

        time.sleep(5)
        for i in range(1,50):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        logger.info("Finished downloading!")


        time.sleep(222)


        #self.driver.find_elements(By.XPATH, '//button[text()="Download"]')

#fe = Fetcher()
#while True: fe.download_videos('https://clip.opus.pro/clip/P00816122thP?utm_source=opus')

##__next > div > div > div > div > div > div.MuiStack-root.css-gojse6 > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedSecondary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedSecondary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.css-1q5zgi7