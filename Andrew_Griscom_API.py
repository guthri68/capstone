import urllib.request
import json
import mysql.connector

DB_NAME = 'astronomy_app'
DB_HOST = '127.0.0.1'
DB_USER = 'node'
DB_PASS = 'node'

def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData

def main():
    #query for Google maps
    query = "rowan"

    #api key for Google maps
    api = "AIzaSyC9yDDqoW9z_xt8efoRiMPmzyMDtKzCjHI"

    # maps query url with api key
    urlData = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query + "&key=" + api;

    #method to get url json data
    jsonData = getResponse(urlData)

    #print raw json data
    #for x in jsonData["results"]:
     #   print(x)
   
    print()    
    
    # print formatted info from json data
    for i in jsonData["results"]:
        print(f'Name: {i["name"]}\nAddress: {i["formatted_address"]}\nLocation: {i["geometry"]["location"]}\n')
    
    #connect to mysql database
    try:
        #db_connection = mysql.connector.connect(host = "localhost", user = "root", passwd="ThePassword", database="Final_Project")
        db_connection = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    except:
            print("Doesnt work")
    
    #cursor to act as keyboard writing out mysql statements
    cursor = db_connection.cursor()
    
    #drops the table if exists
    cursor.execute("DROP TABLE IF EXISTS map")
    
    #sql statement to create a table called map
    sql = '''CREATE TABLE map(
        Name VARCHAR(100),
        Address VARCHAR(255),
        Location VARCHAR(255) 
    )'''

    #executes create table statement
    cursor.execute(sql)

    #executes a show tables statement
    cursor.execute("SHOW TABLES")

    print("The database has the following tables:\n")
    
    #loop to print out the tables in the database
    for db in cursor:
        print(str(db) + "\n")

    count = 0
    print("\nInserting records:\n")

    #loop to insert json data into the database
    for index in jsonData["results"]:

        #name of the query record from json data formatted to string
        value1 = str(index["name"])

        #Address of the query record from json data formatted to string
        value2 = str(index["formatted_address"])

        #Location of the record from the json data formatted to string
        value3 = str(index["geometry"]["location"])

        #insert statement for the table
        sql = """INSERT INTO map(Name, Address, Location)
            VALUES (%s, %s, %s)"""
        
        #all of the relevant data to be included in the insert statement
        values = (value1, value2, value3)    
       
        try:     
            #executes the insert statement       
            cursor.execute(sql, values)

            #commits the statements to the database table
            db_connection.commit()
            count += 1
            print(str(count) + " Records Inserted")
        except Exception as e:
            print(e)      
    
    print("List of records in the table:\n")
    
    #executes a select statement for the table
    cursor.execute('SELECT * from map')
    
    #loop to print out all the records from the select statement
    for row in cursor.fetchall():
        print (row)

    #close the cursor
    cursor.close()
    #close the database connection
    db_connection.close()
       
  
if __name__ == '__main__':
    main()