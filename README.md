# REST API

## Realization

### Creation of the database

After downloading the data, I checked the format of the data with a python script (`res/script_regex.py`). This script was made to check that the given data were respecting the pattern I expected, to know what kind of data type I should use for this CSV. During this part, I realised that some lines were missing data and were filled with '?' instead. I checked that the rest of the numbers were floats with exactly 3 digits after the comma and less that 6 digits before. As it was the case, I decided to choose the `DECIMAL(9,3)` type for these numbers, in order to save memory.  

I created the database using **MariaDB**. I will explain the steps of the creation in the following paragraphs. 


I started by creating the database, and inside of it, the table: 
```sql
CREATE DATABASE technical_test;
USE technical_test;
CREATE TABLE power_consumption
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
);
```

Before importing the data in the database, I created a modified txt file where every '?' would be replaced with nothing, so that these data will be `NULL` in the database:
```sh
sed 's/?//g' household_power_consumption.txt > household_power_consumption_modified.txt
```

After that, I could import the data of the `household_power_consumption_modified.txt` file. I had to be carefull with the date format that was different (`dd/mm/yyyy` in the .txt, and `yyyy-mm-dd` in the database)
```sql
LOAD DATA LOCAL INFILE '../res/household_power_consumption_modified.txt' 
INTO TABLE power_consumption
FIELDS
  TERMINATED BY ';'
  LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(@date,Time,Global_active_power,Global_reactive_power,Voltage,Global_intensity,Sub_metering_1,Sub_metering_2,Sub_metering_3)
SET date = STR_TO_DATE(@date, '%d/%m/%Y');
```

After these steps, the database was created and contained the expected number of lines (2075259).

Then, I created a user to access the database from Python:
```sql
CREATE USER user_test IDENTIFIED BY password1234;
```

As you can see, this password isn't very secure, but it was only for test purposes.  
I then granted this user with the permission to access the `technical_test` database:
```sql
GRANT SELECT ON TABLE technical_test.* TO test_user;
```

To help with the creation of the database, I created a python script to automate part of it. This script is commented and can be found in `src/database_creation.py`. 

### Creation of the API


To create the server (`src/server.py`), I decided to use Python with the Flask framework. I also needed to use the `mariadb` connector, to access the database.  
I created three classes: 
- `ConsumptionList` to get every data about the house consumption, or add a new measure with a `POST` query.
- `ConsumptionListDate` to get every consumption data corresponding to a certain date.
- `ConsumptionData` to get the consumption data of the given date and time, or delete the data of this date and time. I also wanted to add the possibility to update data for a date and time with `PUT`, but I didn't have enough time.

To give the times and dates in the url, I decided to give them in a particular format : `ddmmyyyy` for the date, and `hhmmss` for the time.

I then tested the API with the RESTED firefox extension.


### Next steps

I would have liked to complete the API with the `PUT` query, and then set the project with a setup file to allow other users to use this project easily on other computers (or deploy it with docker).


## Explanation of the API 


- **GET** `/consumption` : get all data in the `power_consumption` database
- **POST** `/consumption` : add a new consumption data on a new date and hour
- **GET** `/consumption/{consumption_date}` get all consumption data on a particular date
- **GET** `/consumption/{consumption_date}/{consumption_time}` get the consumption data on the given date and time
- **DELETE** `/consumption/{consumption_date}/{consumption_time}` delete the data for the specified date and time

Note: the consumption date must be in the format `ddmmyyyy` and the consumtion hour in the format `hhmmss`.




