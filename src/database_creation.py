import mariadb
import sys

""" Before using this script to create the database: 
Create a user: CREATE USER user_test IDENTIFIED BY password1234;
Create the database: CREATE DATABASE technical_test;
Grant privilege on this database to this user: GRANT SELECT ON TABLE technical_test.* TO test_user;
GRANT CREATE ON TABLE technical_test.* TO test_user;
GRANT INSERT ON TABLE technical_test.* TO test_user;
"""

# Connection to MariaDB
try:
    conn = mariadb.connect(
        user="test_user",
        password="password1234",
        host="127.0.0.1",
        port=3306
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


# Get cursor
cur = conn.cursor()

#Change database and create table
query = """USE technical_test2;"""
cur.execute(query)
query = """CREATE TABLE power_consumption
(
    date DATE,
    time TIME,
    global_active_power DECIMAL(9,3),
    global_reactive_power DECIMAL(9,3),
    voltage DECIMAL(9,3),
    global_intensity DECIMAL(9,3),
    sub_metering_1 DECIMAL(9,3),
    sub_metering_2 DECIMAL(9,3),
    sub_metering_3 DECIMAL(9,3),
    CONSTRAINT PK_ PRIMARY KEY (date, time)
);"""
cur.execute(query)

query = """LOAD DATA LOCAL INFILE '../res/household_power_consumption_modified.txt' 
INTO TABLE power_consumption
FIELDS
  TERMINATED BY ';'
  LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(@date,Time,Global_active_power,Global_reactive_power,Voltage,Global_intensity,Sub_metering_1,Sub_metering_2,Sub_metering_3)
SET date = STR_TO_DATE(@date, '%d/%m/%Y');"""

cur.execute(query)

