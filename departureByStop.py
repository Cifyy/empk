import sqlite3,json,time,pickle
from dbRequests import dbReqeustsHandler,weekdayToService
from nearest import nearest,sortStops

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class depByStop():
    def __init__(self,debug=False):
        self.debug = debug
        self.query = """
            SELECT route_short_name, arrival_time 
            FROM stop_times INNER JOIN (trips INNER JOIN routes ON trips.route_id = routes.route_id) ON trips.trip_id = stop_times.trip_id
            WHERE stop_id = ? AND service_id = ?
            ORDER BY arrival_time ASC
            """
        
        self.newQuery = """
            SELECT departures
            FROM departures_by_stop
            WHERE stop_id = ? AND dayOfTheWeek = ? 
        """

        req = dbReqeustsHandler()

        self.stops = sortStops()
        self.stopList = req.getStopIDs()
        self.conn = sqlite3.connect('dataBase.db')
        self.c = self.conn.cursor() 
    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()
    
    def scheduleCreator(self,stopStruct,dayOfTheWeek):
        start = time.time()
        final = {}
        for stopGroup in stopStruct:
            final[stopGroup[0]] = self.createStopsObject(stopGroup[2],stopGroup[1],dayOfTheWeek)
        end = time.time()
        if self.debug: print("     Schedule:",end-start)
        return final

    def createStopsObject(self,stopGroup,distance,dayOfTheWeek):
        start = time.time()
        setGroup = {}
        setGroup["distance"] = distance
        for stopID in stopGroup:
            setGroup[stopID] = self.createStopTable(stopID,dayOfTheWeek)
        end = time.time()
        if self.debug: print("         Stop Group:", end-start)
        return setGroup

    def LEGACY_createStopTable(self,stop_id,dayOfTheWeek): 
        start = time.time()
        self.c.execute(self.query,(stop_id,weekdayToService(dayOfTheWeek)))
        columns = [column[0] for column in self.c.description]
        data = [dict(zip(columns, row)) for row in self.c.fetchall()]
        end = time.time()
        if self.debug: print("             stopQuery:",end-start)
        return data
    
    def createStopTable(self,stop_id,dayOfTheWeek): 
        start = time.time()
        # self.c.execute(self.query,(stop_id,weekdayToService(dayOfTheWeek)))
        if dayOfTheWeek in [1,2,3,4]: dayOfTheWeek = 1
        self.c.execute(self.newQuery,(stop_id,dayOfTheWeek))
        self.conn.commit()

        binaryData = self.c.fetchall()
        data = pickle.loads(binaryData[0][0])

        columns = [column for column in ["route_short_name", "arrival_time"]]
        data = [dict(zip(columns, row)) for row in data]

        end = time.time()
        if self.debug: print("             NewstopQuery",end-start)
        return data

    
    def getNearestStops(self,lat,lon,amount,dayOfTheWeek=1):
        start = time.time()
        
        raw = nearest(lat,lon,self.stops,amount)
        end = time.time()
        
        print("nearest Time:",end-start)
        start = time.time()

        locationSchedule = self.scheduleCreator(raw,dayOfTheWeek)

        end = time.time()
        if self.debug: print("schedule time:",end-start)
        
        # start = time.time()
        # dumped = json.dumps(locationSchedule, cls=SetEncoder)
        # end = time.time()
        # print("dump time:",end-start)
        return json.dumps(locationSchedule, cls=SetEncoder)



if __name__ == '__main__':
    handler = depByStop()

    legacy = handler.LEGACY_createStopTable("stop_53_7703",1)
    new = handler.createStopTable("stop_53_7703",1)
    
    if new == legacy: print(":)")

    # dwa.getNearestStops(50.0017602,20.1467958,5)
    # dwa.getNearestStops()

        # def dumpJsonToFile(self):
        #     jsonData = self.createStopsObject()
        #     weekDay = 1
        #     with open(f'departuresByStop{weekDay}.json', 'w', encoding='utf-8') as f:
        #         json.dump(jsonData, f, ensure_ascii=False, indent=4)

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