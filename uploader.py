import requests
import platform
import os
import time
import sys
from resources import *
from loguru import logger
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QTextEdit, QWidget, QDialog
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

#url = "https://www.facebook.com/v17.0/dialog/oauth?response_type=token&display=popup&client_id=24045900618357273&redirect_uri=http://localhost&auth_type=rerequest&scope=pages_show_list%2Cinstagram_basic%2Cinstagram_manage_comments%2Cinstagram_manage_insights%2Cinstagram_content_publish%2Cinstagram_manage_messages%2Cpages_read_engagement%2Cpages_manage_metadata%2Cpublic_profile"

def get_fb_credential(url):
    app = QApplication([])
    _w = QMainWindow()
    w = QDialog(_w)
    w.resize(600, 500)
    w.setWindowTitle('Login with Facebook')
    web = QWebEngineView(w)
    web.url().toString()
    web.load(QUrl(url))
    web.resize(600, 500)
    web.show()
    w.show()
    print("Please login to your facebook account and close the window after you get redirected to localhost")
    app.exec()
    code = web.url().toString()
    code = code.rsplit('access_token=')[1]
    return code.rsplit('&data_access_expiration')[0]


class FacebookInit:
    def __init__(self, client_id, client_secret, access_url) -> None:
        if platform.system() == "Linux":
            os.system("clear")
        else:
            os.system('cls')
        print("----------------ENTERING FACEBOOK AUTH MODE-----------------")
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_url = access_url
        self.graph_url = 'https://graph.facebook.com/v17.0/'

    def func_get_long_lived_access_token(self):
        self.code = get_fb_credential(self.access_url)
        url = self.graph_url + 'oauth/access_token'
        param = dict()
        param['grant_type'] = 'fb_exchange_token'
        param['client_id'] = self.client_id
        param['client_secret'] = self.client_secret
        param['fb_exchange_token'] = self.code
        response = requests.get(url = url,params=param)
        logger.debug("func_get_long_lived_access_token:response "+str(response))
        response =response.json()
        logger.debug("func_get_long_lived_access_token:response "+str(response))
        long_lived_access_tokken = response['access_token']
        self.long_lived_access_tokken = long_lived_access_tokken
        return long_lived_access_tokken

    def func_get_page_id(self, ):
        # GETS FB USER ID
        _url = self.graph_url + 'me'
        param = dict()
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url=_url, params=param)
        logger.debug("func_get_page_id:response "+str(response))
        response = response.json()
        user_id = response['id']
        logger.debug("func_get_page_id:user_id "+str(user_id))

        param['fields'] = 'id'
        
        response = requests.get(url='https://graph.facebook.com/' + user_id + "/accounts", params=param)

        response = response.json()
        
        return response['data'][0]['id']
    
    def _func_get_instagram_business_account(self, page_id):
        self.page_id = page_id
        url = 'https://graph.facebook.com/' + page_id
        param = dict()
        param['fields'] = 'instagram_business_account'
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url = url,params=param)
        logger.debug("\n _func_get_instagram_business_account:response "+str(response))
        response = response.json()
        logger.debug("\n _func_get_instagram_business_account:response "+str(response))
        try:
            instagram_account_id = response['instagram_business_account']['id']
        except Exception as e:
            logger.error("Instagram account not linked or other error occured:"+str(e))
            return {'error':'Instagram account not linked'}
        return instagram_account_id
        
    def get_post_data(self, media_id=''):
        url = self.graph_url + media_id
        param = dict()
        param['fields'] = 'caption,like_count,media_url,owner,permalink'
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url=url, params=param)
        response = response.json()
        return response


    def _func_get_media_id(self):
        instagram_account_id = self._func_get_instagram_business_account(page_id=self.page_id)
        url = self.graph_url + instagram_account_id +'/media'
        param = dict()
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url =url,params = param)
        response = response.json()
        media = []
        for i in response['data']:
            media_data = self.get_post_data(media_id =i['id'])
            media.append(media_data)
        return media
  

#
class Reel:
    def __init__(self, client_id, client_secret, access_url, page_id) -> None:
        fb = FacebookInit(client_id, client_secret, access_url)
        #make element accessible for future uprades
        self.fb = fb

        self.access_token = fb.func_get_long_lived_access_token()
        self.instagram_account_id = fb._func_get_instagram_business_account(page_id)
        self.graph_url = fb.graph_url
    
    def reels_post_video(self, video_url='',caption=''):
        logger.debug("reels_post_video:video_url "+str(video_url))

        param = dict()
        param['fields'] = 'username'
        param['access_token'] = self.access_token
        response = requests.get(url=self.graph_url + self.instagram_account_id, params=param)

        logger.info("Posting on account: "+response.json()['username'])
        logger.info("Preparing to post video...")
        url = self.graph_url + self.instagram_account_id + '/media'
        param = dict()
        param['access_token'] = self.access_token
        param['caption'] = caption
        param['video_url'] = video_url
        param['media_type'] = 'REELS'
        param['thumb_offset'] = '10'
        response = requests.post(url, params=param)
        logger.info("Video sent to facebook servers!")
        response = response.json()
        logger.debug("reels_post_video:response "+str(response))
        return response['id']

    def reels_status_of_upload(self, ig_container_id = ''):
        url = self.graph_url + ig_container_id
        param = {}
        param['access_token'] = self.access_token
        param['fields'] = 'status_code'
        response = requests.get(url,params=param)
        response = response.json()
        return response
    
    def reels_publish_id(self, id = ''):
        url = self.graph_url + self.instagram_account_id + '/media_publish'
        param = {}
        param['access_token'] = self.access_token
        param['creation_id'] = id
        response = requests.post(url,params=param)
        response = response.json()
        return response


def post_video(r, url, caption='Dont forget to like and follow! #jre #podcast #jreclips'):
    
    id = r.reels_post_video(url, caption)
    while True:
        logger.info("Waiting for upload to finish...")
        time.sleep(10)
        status = r.reels_status_of_upload(id)
        logger.debug("Status code: "+status['status_code'])
        if status['status_code'] == 'FINISHED':
            logger.debug(status)
            logger.debug(r.reels_publish_id(id))
            break