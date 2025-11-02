import os 
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()
engine = create_engine(os.getenv('DB_URL'))

if __name__ == '__main__':
    pass



