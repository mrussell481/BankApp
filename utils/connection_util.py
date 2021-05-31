from psycopg2 import connect
from psycopg2._psycopg import OperationalError
import os



#host='revdatabase1.clpplk5gj1yg.us-east-2.rds.amazonaws.com',
 #           database='postgres',
 #           user='mrussell481',
 #           password='nubnut2658',
 #           port='5432'


def create_connection():
    try:
        conn = connect(
            host=os.environ.get('HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('PORT')
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
