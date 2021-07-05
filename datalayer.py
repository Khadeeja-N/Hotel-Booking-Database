import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import date, timedelta

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# Connecting to the database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database = db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

pw = "" #MySQL Terminal password
db = "hotels" # Name of the database

# Creates the database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

# Executes the queries sent to MySQL
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# Rooms table Query
create_room_table = """
CREATE TABLE room (
  room_id INT PRIMARY KEY,
  room_type VARCHAR(40) NOT NULL,
  room_descrip VARCHAR(100) NOT NULL,
  room_price VARCHAR(40) NOT NULL);
 """

# Booked rooms table Query
create_bookings_table = """
CREATE TABLE bookings (
    booking_num INT PRIMARY KEY,
    room_id INT,
  check_in VARCHAR(40) NOT NULL,
  check_out VARCHAR(40) NOT NULL,
  guest_name VARCHAR(40) NOT NULL
);
 """

def add_room(connection, room_id, room_type, room_descrip, room_price):
    pop_rooms = """
    INSERT INTO room VALUES
    (%s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        cursor.execute(pop_rooms, (room_id, room_type, room_descrip, room_price))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def update_room(connection, field_to_update, updated_value, room_id):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE room SET "+field_to_update+" = (%s) WHERE room_id = (%s)",(updated_value,room_id))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def delete_room(connection, room_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM room WHERE room_id = (%s)",(room_id,))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def add_booking(connection, start_year, start_month, start_date, end_year, end_month, end_date, room_id, guest_name):
    # Read Query
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute("""SELECT COUNT(*) FROM bookings;""")
        result = cursor.fetchall()
    except Error as err:
        print(f"Error: '{err}'")

    booking_num = 0
    for x in result:
        for y in x:
            booking_num = int(y)

    booking_num += 1
    
    s_date = start_year+"-"+start_month+"-"+start_date
    e_date = end_year+"-"+end_month+"-"+end_date
        
    cursor = connection.cursor()
    try:
        query = """INSERT INTO bookings VALUES
    (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (booking_num, room_id, s_date, e_date, guest_name))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    
    print("Your booking number is ", booking_num)


def delete_booking(connection, booking_num):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM bookings WHERE booking_num = (%s)",(booking_num,))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def room_between(connection, start_year, start_month, start_date, end_year, end_month, end_date):
    sdate = start_year+"-"+start_month+"-"+start_date
    edate = end_year+"-"+end_month+"-"+end_date

    cursor = connection.cursor()
    results = None
    try:
        query = """ SELECT DISTINCT r.* 
                    FROM room r
                    LEFT JOIN bookings ON r.room_id = bookings.room_id
                    WHERE (bookings.booking_num IS NULL) OR 
                    (bookings.check_in < %s OR bookings.check_in > %s) AND
                    (bookings.check_out < %s OR bookings.check_out > %s)
        """
        cursor.execute(query,(sdate, edate, sdate, edate))
        results = cursor.fetchall()
    except Error as err:
        print(f"Error: '{err}'")


    if not results:
        print("There are no rooms available between the requested dates.\n")
        return

    from_db = []

    for result in results:
        result = list(result)
        from_db.append(result)


    columns = ["Room ID", "Room Type", "Room Description", "Room Price"]
    df = pd.DataFrame(from_db, columns=columns)

    print(df.to_string())
    print("\n")


def room_price(connection, room_id):
    cursor = connection.cursor()
    results = None
    try:
        query = """ SELECT room_price 
                    FROM room r
                    WHERE room_id = %s
        """
        cursor.execute(query,(room_id,))
        results = cursor.fetchall()
    except Error as err:
        print(f"Error: '{err}'")

    for result in results:
        for price in result:
            print("$" + price)

  

# Main Loop 

# If the database does not exist, use this: 
connection = create_server_connection("localhost", "root", pw)
create_database_query = "CREATE DATABASE hotels"
create_database(connection, create_database_query)

execute_query(connection, create_room_table) 
execute_query(connection, create_bookings_table) 

# If the database already exists, use this:
connection = create_db_connection("localhost", "root", pw, db)


loop_ctr = 1
while loop_ctr > 0:
    print("Welcome to the hotel database\n")
    print("Please enter the command of your choice\n")
    print("ADD A ROOM: AR \n UPDATE ROOM: UR \n DELETE ROOM: DR\n ADD BOOKING: AB\n DELETE BOOKING: DB\n AVAILABLE ROOMS: AVR\n ROOM PRICE: RP\n")
    
    val = input("Your Command: ")
    if (val == "AR"):
       num_rooms = int(input("Enter the number of rooms you would like to add: "))
       for x in range(num_rooms):
           room_id = input("Room ID: ")
           room_type = input("Room Type: ")
           room_descrip = input("Room Description: ")
           room_price = input("Room Price: ")
           print("Thank you for the entry \n")
           add_room(connection, room_id, room_type, room_descrip, room_price)

    elif (val == "UR"):
        room_id = input("Room ID: ")
        field_to_update = input("Field To Update(room_id, room_type, room_descrip, room_price): ")
        updated_value = input("New Value: ")
        update_room(connection, field_to_update, updated_value, room_id)

    elif (val == "DR"):
        room_id = input("Room ID: ")
        delete_room(connection, room_id)

    elif (val == "AB"):
        syear = input("Start Year: ")
        smonth = input("Start Month: ")
        sdate = input("Start Date: ")

        eyear = input("End Year: ")
        emonth = input("End Month: ")
        edate = input("End Date: ")

        room_id = input("Room ID: ")
        guest_name = input("Guest Name: ")

        add_booking(connection, syear, smonth, sdate, eyear, emonth, edate, room_id, guest_name)

    elif (val == "DB"):
        booking_num = int(input("Booking Number: "))

        delete_booking(connection, booking_num)

    elif (val == "AVR"):
        syear = (input("Check-in Year: "))
        smonth = (input("Check-in Month: "))
        sdate = (input("Check-in Date: "))

        eyear = (input("Check-out Year: "))
        emonth = (input("Check-out Month: "))
        edate = (input("Check-out Date: "))

        room_between(connection, syear, smonth, sdate, eyear, emonth, edate)


    elif (val == "RP"):
         room_id = input("Room ID: ")
         room_price(connection, room_id)


        








    
   
   
   
    



    










   
