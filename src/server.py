from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import datetime
import mariadb
import sys

HEADERS = ["date", "time", "global_active_power", "global_reactive_power", "voltage", "global_intensity", "sub_metering_1", "sub_metering_2", "sub_metering_3"]



app = Flask(__name__)
api = Api(app)

# Connection to MariaDB
try:
    conn = mariadb.connect(
        user="test_user",
        password="password1234",
        host="127.0.0.1",
        port=3306,
        database="technical_test"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


# Get cursor
cur = conn.cursor()
parser = reqparse.RequestParser()


class ConsumptionList(Resource):
    def get(self):
        cur.execute("SELECT * FROM power_consumption;")
        compl_json = []
        data = []
        l = cur.fetchall()
        for line in l:
            date = line[0].strftime("%d/%m/%Y")
            data.append(date)
            time = str(line[1])
            data.append(time)
            for i in range(2,len(line)):
                data.append(str(line[i]))
            json_obj = consumption_as_json(data)
            compl_json.append(json_obj)
            data = []
        response = {"result": compl_json}
        response["status_code"] = 200
        return json.dumps(response)

    def post(self):
        values = ""
        headers_values = "("
        first = True
        for elem in HEADERS:
            if first:
                first=False
            else:
                headers_values+=','
            parser.add_argument(elem)
            headers_values += elem
        headers_values += ')'
        args = parser.parse_args()
        for elem in HEADERS:
            if (elem=="date"):
                date = datetime.datetime.strptime(args[elem], "%d/%m/%Y").strftime("%Y-%m-%d")
                values += "'"+date+"'"
            elif (elem=="time"):
                values += ",'" + args[elem] + "'"
            else:
                values += ",'" + args[elem] + "'"
        query = "INSERT INTO power_consumption "+headers_values+" VALUES("+values+");"
        print(query)
        cur.execute(query)
        conn.commit()
    pass

class ConsumptionListDate(Resource):
    def get(self, consumption_date):
        new_date = change_date_format(consumption_date)
        cur.execute("SELECT * FROM power_consumption WHERE date LIKE '"+new_date+"';")
        compl_json = []
        data = []
        l = cur.fetchall()
        if len(l)==0:
            return "Not found", 404
        for line in l:
            date = line[0].strftime("%d/%m/%Y")
            data.append(date)
            time = str(line[1])
            data.append(time)
            for i in range(2,len(line)):
                data.append(str(line[i]))
            print(data)
            json_obj = consumption_as_json(data)
            print(json_obj)
            compl_json.append(json_obj)
            data = []
        response = {"result": compl_json}
        response["status_code"] = 200
        return json.dumps(response)
    pass

class ConsumptionData(Resource):
    def get(self, consumption_date, consumption_hour):
        date = change_date_format(consumption_date)
        hour = change_hour_format(consumption_hour)
        cur.execute(
            "SELECT * FROM power_consumption WHERE date LIKE '" + date + "' AND TIME LIKE '"+hour+"';")  # ;")
        data = []
        l = cur.fetchall()
        if len(l)!=1:
            return "Not found", 404
        
        line = l[0]
        date = line[0].strftime("%d/%m/%Y")
        data.append(date)
        time = str(line[1])
        data.append(time)
        for i in range(2, len(line)):
            data.append(str(line[i]))
        json_obj = consumption_as_json(data)
        response = {"result": json_obj}
        response["status_code"] = 200
        return json.dumps(json_obj)

    def put(self, consumption_date, consumption_hour):
        date = change_date_format(consumption_date)
        hour = change_hour_format(consumption_hour)

    def delete(self, consumption_date, consumption_hour):
        date = change_date_format(consumption_date)
        hour = change_hour_format(consumption_hour)
        print("DELETE FROM power_consumption WHERE date LIKE '" + date + "' AND TIME LIKE '" + hour + "';")
        cur.execute("DELETE FROM power_consumption WHERE date LIKE '" + date + "' AND TIME LIKE '" + hour + "';")
        conn.commit()
        return '',204
    pass

# Put every data of a consumption element in json format
def consumption_as_json(dat):
    result = '{'
    #result = ''
    for i in range(len(HEADERS)):
        if i > 0:
            result += ','
        result += '"' + HEADERS[i] + '": ' + dat[i]
    result += '}'
    return result

# Convert data format from ddmmyyy to yyyy-mm-dd
def change_date_format(date):
    if len(date)!= 8:
        return "Bad date format"
    new_date = date[4:]+'-'+date[2:4]+'-'+date[0:2]
    print(new_date)
    return new_date

# Convert hour format from hhmmss to hh:mm:ss
def change_hour_format(hour):
    if len(hour)!= 6:
        return "Bad hour format"
    new_hour = hour[0:2]+':'+hour[2:4]+':'+hour[4:]
    print(new_hour)
    return new_hour

api.add_resource(ConsumptionList, '/consumption')
api.add_resource(ConsumptionListDate, '/consumption/<consumption_date>')
api.add_resource(ConsumptionData, '/consumption/<consumption_date>/<consumption_hour>')


if __name__ == "__main__":
    app.run(debug=True)