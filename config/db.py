from psycopg2 import connect, sql
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("DB")
pgsqlConn = connect(url)