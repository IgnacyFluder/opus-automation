import mail_system
import opus_fetcher
from loguru import logger
import os
import time
import platform
import yogopy


if platform.system() == "Linux":
    os.system("clear")
else:
    os.system('cls')

logger.info("Welcome to the OPUS.PRO account generator")

logger.add("./loguru.log", format="{time} {level} {message}[MAIN.PY]", level="INFO")


def run(vids:list):
    times = len(vids)
    while times != 0:
        times -= 1
        try:
            fetcher = opus_fetcher.Fetcher()
            fetcher.init()
            inbox, email = mail_system.get_inbox()
            #inbox  = yogopy.YogoInbox('forfouchtenredouts1956@yopmail.com')

            logger.info('Running program...('+str(times+1)+')')
            fetcher.register_step_1(email=email)
            
            code=inbox.listen_for_verification_code()
            fetcher.register_step_2(code=code, yt_link=vids[times])
            logger.success("Finished browsing the web!")
            link = inbox.listen_for_clip_link()
            logger.info("Link aquired! "+link)

            fetcher.download_videos(url=link)
            time.sleep(3)
            logger.success("Finished registering!")

            logger.success("Task NO. "+str(times+1)+" finished!")

        except UnboundLocalError:
            logger.warning("Unable to identify exception.")

        #make sure the browser closes
        except KeyboardInterrupt:
            try: 
                logger.error("Interrupted")
                fetcher.driver.close()
                break
            except Exception: pass

        except Exception as e:
            times +=1
            #ik this looks weird but it works .-.
            try:
                if fetcher.wish != None:
                    logger.warning("Main script ended work with exception. Class returned: "+fetcher.wish+"... retrying")
                    
                else:
                    logger.exception("Main script ended work with exception: "+str(e))
            except Exception:
                logger.exception("Main script ended work with exception: "+str(e))
    
    logger.info("Work finished! shutting off...")

run(['https://youtu.be/7doXTqVp16g'])