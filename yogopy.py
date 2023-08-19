import subprocess
import json
import time
import sys
from loguru import logger


class YogoInbox:
    def __init__(self, username):
        #self._yogo_binary_interaction("./yogo inbox flush "+username)
        self.username = username
    
    def _yogo_binary_interaction(self, cmd, verbose=False):
        try:
            query = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            query.wait()
            _, _output = query.communicate()
            _output = str(_output)[2:-3]
            _output = _output.replace("\\", "")
            _output = json.loads(_output)
            return _output
        except Exception:
            return None

    def listen_for_verification_code(self, refresh=5):
        
        time.sleep(2)
        while True:
            time.sleep(refresh)
            output = self._yogo_binary_interaction("./yogo inbox list "+self.username+" 1 --json")
            try: last_mail = output["mails"][0]; break
            except IndexError as e: logger.debug("Inbox was empty! retrying in 5 seconds("+str(e)+")")
            
        
        logger.info("Started listening to verification code email.")
        
        while True:
            time.sleep(refresh)
            if "is your OpusClip code" in last_mail['title']:
                logger.info("Found Opus login code: " + str(last_mail['title'])[:6])
                return str(last_mail['title'])[:6]
            
    def listen_for_clip_link(self, refresh=60):
        
        while True:
            output = self._yogo_binary_interaction("./yogo inbox list "+self.username+" 1 --json")
            try: last_mail = output["mails"][0]; break
            except IndexError: pass
            time.sleep(5)
        while True:
            try:
                output = self._yogo_binary_interaction("./yogo inbox list "+self.username+" 1 --json")
                last_mail = output["mails"][0]
                if "Your clips are ready" in last_mail['title']:
                    output = self._yogo_binary_interaction("./yogo inbox show "+self.username+" 1 --json")
                    output = str(output).split("nnView clips ( ")
                    output = output[1]
                    output = output.split(" )nnBuild with")
                    return output[0]
                
                time.sleep(refresh)
            except TypeError:
                pass

#/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div[INDEX]/div[2]/div/div/div/div/div[2]/div[2]/button
#"./yogo inbox list test1 1 --json"
#yopper9999
#credsf-trial-1