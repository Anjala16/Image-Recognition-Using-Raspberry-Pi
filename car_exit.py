import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import sys
from gpiozero import LED
import time

red = LED(18)
green = LED(24)

print("--------------------------------------------------------------------")
print("Running car_exit.py code to update entry in car_logs table......")
print("--------------------------------------------------------------------")
print("Registeration number received is : " + sys.argv[1])

try:
   connection = mysql.connector.connect(host='localhost',
                             database='number_plate',
                             user='anjala',
                             password='anjala')

   input_registration_number = sys.argv[1]
   
   sqlQry = "SELECT * FROM car_logs WHERE registration_number = '" + input_registration_number + "' AND exit_time = '0000-00-00 00:00:00'"
   print(sqlQry)
   cursor = connection.cursor()
   cursor.execute(sqlQry)
   cursor.fetchall()

   if cursor.rowcount == 1:
        updQry = "UPDATE car_logs SET entry_time = entry_time, exit_time = NOW(), duration = NOW() - entry_time  WHERE registration_number = '" + input_registration_number + "'"
        cursor.execute(updQry)
        connection.commit()
        print ("Car exit recorded.....")
        green.on()
        time.sleep(5)
        green.off()      
   else:
        print("!!!!!!   Error  !!!! Possible reasons could be - 1) Car not entered in entry point. 2) Multiple entries of Car in car_entries table. 3) Car might be exited from exit point (car_logs.exit_time != '0000-00-00 00:00:00'.")
        red.on()
        time.sleep(5)
        red.off()

except mysql.connector.Error as error :
    connection.rollback() #rollback if any exception occured
    print("Failed inserting record {}".format(error))

finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

