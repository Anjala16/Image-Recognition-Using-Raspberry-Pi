import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import sys
from subprocess import call
from gpiozero import LED
import time

red = LED(18)
green = LED(24)

print("--------------------------------------------------------------------")
print("Running car_entry.py code to register entry in car_logs table......")
print("--------------------------------------------------------------------")
print("Registeration number received is : " + sys.argv[1])
try:
   connection = mysql.connector.connect(host='localhost',
                             database='number_plate',
                             user='anjala',
                             password='anjala')

   input_registration_number = sys.argv[1] 
   
   sqlQry = "SELECT * FROM car_registrations WHERE registration_number = '" + input_registration_number + "'"
   cursor = connection.cursor()
   cursor.execute(sqlQry)
   cursor.fetchall()

   print("No. of car registered with number " + input_registration_number + " = " + str(cursor.rowcount))

   if cursor.rowcount == 0:
        print("!!!!!!Car not registered....will not be allowed for parking!!!!!")
        red.on()
        time.sleep(5)
        red.off()
   else:
        
        # check if car already inside parking
        chkCarInsideParkingQry = "SELECT * FROM car_logs WHERE registration_number = '" + input_registration_number + "' AND exit_time = '0000-00-00 00:00:00'"
        cursor.execute(chkCarInsideParkingQry)
        cursor.fetchall()
        if cursor.rowcount > 0:
            print("Car is already inside parking area..... record found in car_logs table")
            red.on()
            time.sleep(5)
            red.off()
        else:
            insertQry = "INSERT INTO car_logs(registration_number, entry_time) VALUES ('" + input_registration_number + "', NOW())"
            result  = cursor.execute(insertQry)
            connection.commit()
            green.on()
            print ("Record inserted successfully into car_logs table")
            time.sleep(5)
            green.off()
except mysql.connector.Error as error :
    connection.rollback() #rollback if any exception occured
    print("Failed inserting record {}".format(error))

finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
