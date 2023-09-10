import mail_system
import opus_fetcher
from loguru import logger
import os
import time
import platform
import uploader
from resources import FB_CREDENTIALS
#import yogopy

if platform.system() == "Linux":
    os.system("clear")
else:
    os.system('cls')

logger.info("Welcome to the OPUS.PRO auto uploader!")

logger.add("./loguru.log", format="{time} {level} {message}[MAIN.PY]", level="INFO")


def run(vids:list, headless=False, reel=None):
    times = len(vids)
    while times > 0:
        times -= 1
        try:
            fetcher = opus_fetcher.Fetcher()
            fetcher.init(headless=headless)
            inbox, email = mail_system.get_inbox()
            #inbox  = yogopy.YogoInbox('forfouchtenredouts1956@yopmail.com')

            logger.info('Running program...('+str(times+1)+')')
            fetcher.register_step_1(email=email)
            
            code=inbox.listen_for_verification_code()
            fetcher.register_step_2(code=code, yt_link=vids[times])
            logger.success("Finished browsing the web!")
            link = inbox.listen_for_clip_link()
            logger.info("Link aquired! "+link)

            urls = fetcher.download_videos(url=link)
            time.sleep(3)
            logger.success("Finished link harvesting!")
            logger.info("Video upload started...")
            logger.warning("Upload proccess is not fully developed yet!")

            if reel == None:
                reel = uploader.Reel(
                    FB_CREDENTIALS['client_id'],
                    FB_CREDENTIALS['client_secret'],
                    FB_CREDENTIALS['access_url'],
                    FB_CREDENTIALS['page_id']
                )
                

            for url in urls:
                uploader.post_video(reel, url)
                
            logger.success("Task NO. "+str(times+1)+" finished!")
            
            return urls

        except UnboundLocalError:
            logger.warning("Unable to identify exception.")

        #make sure the browser closes
        except KeyboardInterrupt:
            try: 
                logger.error("Interrupted")
                fetcher.driver.close()
                raise KeyboardInterrupt
            except Exception: pass


        except Exception as e:
            times +=1
            #ik this looks weird but it works .-.
            try:
                if "IP Blocked!" in str(e):
                    logger.warning("IP Blocked! Retrying...")
                elif fetcher.wish != None:
                    logger.warning("Main script ended work with exception. Class returned: "+fetcher.wish+"... retrying")
                else:
                    logger.exception("Main script ended work with exception: "+str(e))
                    raise Exception("Something unexpected happened!")
            except Exception:
                logger.exception("Main script ended work with exception: "+str(e))
                raise Exception("Something unexpected happened!")
            
def run_raw(url, headless=False):
    logger.info("Initiated raw")
    fetcher = opus_fetcher.Fetcher()
    inbox, email = mail_system.get_inbox()
    fetcher.email = email
    urls = fetcher.download_videos(url=url, headless=headless)
    logger.info("Started upload")
    for url in urls:
        uploader.post_video(url)
    logger.success("Task(raw) finished!")

def remove_chrome():
    os.system('taskkill /F /IM chrome.exe')

#run(['https://www.youtube.com/watch?v=Bj0ovoo2dMg', 'https://www.youtube.com/watch?v=d5XTDmm0KUQ'], headless=False)