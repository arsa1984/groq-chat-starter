import psycopg2

conn = psycopg2.connect(
    dbname="PostgreSQL", 
    user="arsakalhor84@gmail.com",             
    password="arsa1984",     
    host="localhost",          
    port="5432"                   
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
version = cursor.fetchone()
print("Connected to:", version)
cursor.close()
conn.close()
