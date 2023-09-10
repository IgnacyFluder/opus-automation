from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
#Any modifications to this file may cause the program to not work properly, please use the ui to change settings
###########RESOURCES#############
DOMAIN_LIST = ['@yopmail.com']
TIMEOUT = 25
PROXY_TYPE = 'paid'
PAID_PROXY_BACKBONE = 'p.webshare.io:9999'
DO_SLEEP = False
IGNORED_EXCEPTIONS=(NoSuchElementException,StaleElementReferenceException,ElementClickInterceptedException,)
SETTER = [DOMAIN_LIST, TIMEOUT, PROXY_TYPE, PAID_PROXY_BACKBONE, DO_SLEEP]
SETTER_NAMES = ['DOMAIN_LIST', 'TIMEOUT', 'PROXY_TYPE', 'PAID_PROXY_BACKBONE', 'DO_SLEEP']
SETTER_HINTS = ['List of domains to use for email creation', 'Timeout for selenium(to this is added from 0.1 to 0.9 more seconds for more security)', 'Proxy type', 'Proxy backbone', 'Sleep between actions']
SETTER_TYPES = [list, int, str, str, bool]
FB_CREDENTIALS = {
    'client_id':'',
    'client_secret':'',
    'access_url':'',
    'page_id':''
}