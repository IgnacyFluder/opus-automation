import requests
import platform
import os

import webview
webview.create_window('Hello world', 'https://pywebview.flowrl.com/')
webview.start(gui='gtk')


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
        print('\n Enter this website and authorize your app then copy and paste the url: ', self.access_url)
        code = input("\n Copy and paste the url: ")
        code = code.rsplit('access_token=')[1]
        self.code = code.rsplit('&data_access_expiration')[0]
        url = self.graph_url + 'oauth/access_token'
        param = dict()
        param['grant_type'] = 'fb_exchange_token'
        param['client_id'] = self.client_id
        param['client_secret'] = self.client_secret
        param['fb_exchange_token'] = self.code
        response = requests.get(url = url,params=param)
        print("\n response",response)
        response =response.json()
        print("\n response",response)
        long_lived_access_tokken = response['access_token']
        self.long_lived_access_tokken = long_lived_access_tokken
        return long_lived_access_tokken

    #def func_get_fb_user_id(self):
    #    url = "https://graph.facebook.com/USER-ID?access_token="+ self.long_lived_access_tokken 
    #    response = requests.get(url = url)
    #    response = response.json()
    #    return response['id']

    def func_get_page_id(self,):
        # GETS FB USER ID
        url = self.graph_url + 'me'
        param = dict()
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url = url,params=param)
        print("\n response", response)
        response = response.json()
        user_id = response['id']
        print("\n user_id",user_id)

        param['fields'] = 'id'
        
        response = requests.get(url = self.graph_url + user_id + "/accounts", params=param)

        response = response.json()
        
        return response['data'][0]['id']
    
    def _func_get_instagram_business_account(self, page_id = ''):
        url = self.graph_url + page_id
        param = dict()
        param['fields'] = 'instagram_business_account'
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url = url,params=param)
        print("\n response",response)
        response = response.json()
        print("\n response", response)
        try:
            instagram_account_id = response['instagram_business_account']['id']
        except:
            return {'error':'Instagram account not linked'}
        return instagram_account_id
    
    def func_get_instagram_business_account(self):
        #fb_user_id = self.func_get_fb_user_id()
        page_id = self.func_get_page_id()
        insta_id = self._func_get_instagram_business_account(page_id=page_id)
        return insta_id
        
    def get_post_data(self, media_id=''):
        url = self.graph_url + media_id
        param = dict()
        param['fields'] = 'caption,like_count,media_url,owner,permalink'
        param['access_token'] = self.long_lived_access_tokken
        response = requests.get(url=url, params=param)
        response = response.json()
        return response


    def _func_get_media_id(self):
        instagram_account_id = self.func_get_instagram_business_account()
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
    def __init__(self, client_id, client_secret, access_url) -> None:
        fb = FacebookInit(client_id, client_secret, access_url)
        #make element accessible for future uprades
        self.fb = fb

        self.access_token = fb.func_get_long_lived_access_token()
        self.instagram_account_id = fb.func_get_instagram_business_account()
        self.graph_url = fb.graph_url
    
    def reels_post_video(self, video_url='',caption=''):
        url = self.graph_url + self.instagram_account_id + '/media'
        param = dict()
        param['access_token'] = self.access_token
        param['caption'] = caption
        param['video_url'] = video_url
        param['media_type'] = 'VIDEO'
        param['thumb_offset'] = '10'
        response = requests.post(url, params=param)
        response = response.json()
        return response

    def reels_status_of_upload(self, ig_container_id = ''):
        url = self.graph_url + ig_container_id
        param = {}
        param['access_token'] = self.access_token
        param['fields'] = 'status_code'
        response = requests.get(url,params=param)
        response = response.json()
        return response
    
r = Reel('24045900618357273', 'e28962a6ef28942c9d5533f28cf7425e', 'https://www.facebook.com/v17.0/dialog/oauth?response_type=token&display=popup&client_id=24045900618357273&redirect_uri=http://localhost&auth_type=rerequest&scope=pages_show_list%2Cinstagram_basic%2Cinstagram_manage_comments%2Cinstagram_manage_insights%2Cinstagram_content_publish%2Cinstagram_manage_messages%2Cpages_read_engagement%2Cpages_manage_metadata%2Cpublic_profile')
r.reels_post_video('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4', 'First post using IG Graph api and python! ATTENTION: THIS VIDEO IS NOT INTENDED FOR COPYRIGHT ABUSE ITS JUST A WAY TO TEST OUR SYSTEM!')