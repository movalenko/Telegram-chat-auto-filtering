from telethon.sync import TelegramClient, events
from config import api_hash, api_id, command_chat_id, gpt_key
from handlers import  show, add, remove, control_list





class Account:
    def __init__(self, api_hash, api_id, command_chat_id):
        
        #all the variables necessary for initialization of telegram account
        self.hash = api_hash
        self.id = api_id

        #client initialization
        self.client = TelegramClient("/home/aidos/Desktop/tg_bot/masha/anon.session", self.id, self.hash)


        #variables for client's web hooks working
        self.client.command_chat = command_chat_id
        self.client.control_list = set()
        self.client.processes = {}


        #variables for gpt prompt analyzer
        self.client.gpt_key = gpt_key


    def start(self):
        with self.client:

            #we add all our async event handlers from handlers.py
            self.client.add_event_handler(show, events.NewMessage(chats = self.command_chat, pattern=r'^/list$'))
            self.client.add_event_handler(add, events.NewMessage(chats = self.command_chat, pattern = r'^/add (\d+) (.+)$'))
            self.client.add_event_handler(remove, events.NewMessage(chats = self.command_chat, pattern=r"/remove \d+"))
            self.client.add_event_handler(control_list, events.NewMessage(chats = self.command_chat, pattern = r"/control_list"))

            #basically handles the loop 
            self.client.run_until_disconnected()


    def todo(self):
        pass

#account = Account(api_hash, api_id, command_chat_id)
#account.start()