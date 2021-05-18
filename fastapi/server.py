import os
from fastapi import FastAPI
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config

app = FastAPI()

def connect_db():
  """Connect to PostgreSQL server"""
  connection = None
  if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"]
  else:
<<<<<<< HEAD
    db = config(filename="config.toml")
=======
    db = config(filename="../config.toml")
>>>>>>> 8f8fc376387e6bc92e85279e429405d5b3d19524
    DATABASE_URL = f"postgresql://{db['user']}@{db['host']}/{db['database']}"
  print("DATABASE_URL", DATABASE_URL)
  try:
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

@app.get("/locations")
def get_locations():
  """List all locations"""
  connection = connect_db()
  cur = connection.cursor()
  cur.execute("SELECT * FROM locations")
  locations = cur.fetchall()
  return locations
