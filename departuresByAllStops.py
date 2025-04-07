import sqlite3   
from dbRequests import dbReqeustsHandler,weekdayToService
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class depByStop():
    def __init__(self):
        self.query = """
            SELECT route_short_name, arrival_time 
            FROM stop_times INNER JOIN (trips INNER JOIN routes ON trips.route_id = routes.route_id) ON trips.trip_id = stop_times.trip_id
            WHERE stop_id = ? AND service_id = ?
            ORDER BY arrival_time ASC
            """
        req = dbReqeustsHandler()
        self.stopList = req.getStopIDs()
        self.conn = sqlite3.connect('dataBase.db')
        self.c = self.conn.cursor() 
    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()
    
    def createStopsObject(self):
        jsonSet = {}
        amountOfStops = len(self.stopList)
        c = 1
        for stopID in self.stopList:
            print(f'{c}/{amountOfStops} {round(c/amountOfStops*100,2)}%')
            c += 1
            jsonSet[stopID] = self.createStopTable(stopID,1)
        jsonData = json.dumps(jsonSet, cls=SetEncoder)
        return jsonData

    def createStopTable(self,stop_id,dayOfTheWeek):
        self.c.execute(self.query,(stop_id,weekdayToService(dayOfTheWeek)))
        
        columns = [column[0] for column in self.c.description]
        data = [dict(zip(columns, row)) for row in self.c.fetchall()]
        return data

    def dumpJsonToFile(self):
        jsonData = self.createStopsObject()
        weekDay = 1
        with open(f'departuresByStop{weekDay}.json', 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)

# if __name__ == '__main__':
    # dt = depByStop()
    # dt.dumpJsonToFile()

    # c.execute(query,(stop_id,weekdayToService(dayOfTheWeek)))
    # def getEntry(query,stop_id,serviceID):
        
    # stops = [
    #     {"id": 1, "latitude": 123.456, "longitude": 789.012},
    #     {"id": 2, "latitude": 456.789, "longitude": 987.654},
    #     {"id": 3, "latitude": 321.654, "longitude": 654.321}
    # ]

    # nested_json = []

    # for stop in stops:
    #     nested_json.append({
    #         "id": stop["id"],
    #         "latitude": stop["latitude"],
    #         "longitude": stop["longitude"]
    #     })
    # import json
    # nested_json_str = json.dumps(nested_json, indent=4)
    # print(nested_json_str)