from random import randint, choice
from random_word import RandomWords
from loguru import logger
import resources
import yogopy

def get_inbox():
    rw = RandomWords()

    inbox_username = rw.get_random_word() + rw.get_random_word() + str(randint(1900, 2008))
    #inbox_username = "nenaesquecomotunohayninguna"

    input_email = inbox_username+choice(resources.DOMAIN_LIST)
    #input_email = inbox_username + "@yopmail.com"

    inbox = yogopy.YogoInbox(inbox_username)

    logger.debug('Email used: '+input_email)

    return inbox, input_email
