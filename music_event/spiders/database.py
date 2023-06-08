import psycopg2

# Connection parameters
host = 'localhost'
port = '5432'
database = 'music_event'
user = 'postgres'
password = 'deol9646'

# Connect to the PostgreSQL server
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    conn.autocommit = True
except:
    conn = psycopg2.connect(
        host=host,
        port=port,
        database='postgres',  # Connect to the default 'postgres' database
        user=user, 
        password=password
    )
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    conn.autocommit = True

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (database,))
    exists = cursor.fetchone()

    if not exists:
        # Create the database
        create_database_query = f"CREATE DATABASE {database}"
        cursor.execute(create_database_query)
        print(f"Database '{database}' created successfully.")

    else:
        print(f"Database '{database}' already exists. CONTINUE USING....")
        # Create the table if it doesn't exist
       

conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)
create_table_query = """
        CREATE TABLE IF NOT EXISTS event (
            title TEXT,
            url TEXT,
            price TEXT,
            date_time TEXT,
            location TEXT
        )
    """
cursor.execute(create_table_query)
     



# def get_database_list():
    # SQL query to retrieve the list of databases
    # query = "SELECT datname FROM pg_database WHERE datistemplate = false;"

    # # Execute the query
    # cursor.execute(query)

    # # Fetch all the rows from the result set
    # rows = cursor.fetchall()

    # # Print the list of databases
    # print("List of databases:")
    # for row in rows:
    #     print(row[0])


# input=input('YOU WANT DATABASE LIST Y/N:')

# if input=='Y' or input=='y':
#     get_database_list()

# # Commit the transaction
# conn.commit()

# # Close the cursor
# cursor.close()

# # Close the connection
# conn.close()




#
# Query to retrieve table names
# query = """
#     SELECT table_name
#     FROM information_schema.tables
#     WHERE table_schema = 'public'
# """

# # Execute the query
# cursor.execute(query)

# # Fetch all table names
# tables = cursor.fetchall()

# # Print the table names
# print("Tables:")
# for table in tables:
#     print(table[0])