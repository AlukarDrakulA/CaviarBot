from aiogram.utils import executor
from config import dp
from handlers import client
from database.atlasconfig import atlasAccess


client.register_handlers_client(dp)

def main():
    atlasAccess()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()    
