import sqlite3,json
from nearest import nearest,sortStops

def weekdayToService(dayOfTheWeek):
    if dayOfTheWeek == 5: return "service_4"
    elif dayOfTheWeek == 6: return "service_2"
    elif dayOfTheWeek == 7: return "service_3"
    else: return "service_1"

class dbReqeustsHandler():
    def __init__(self) -> None:
        self.stops = sortStops()
        self.conn = sqlite3.connect('dataBase.db')
        self.c = self.conn.cursor()  
    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()
    
    def convToJson(self):
        columns = [column[0] for column in self.c.description]
        data = [dict(zip(columns, row)) for row in self.c.fetchall()]
        return json.dumps(data)
    
    def getDeparturesByStop(self,stop_id,dayOfTheWeek):
        query = """
        SELECT route_short_name, arrival_time 
        FROM stop_times INNER JOIN (trips INNER JOIN routes ON trips.route_id = routes.route_id) ON trips.trip_id = stop_times.trip_id
        WHERE stop_id = ? AND service_id = ?
        ORDER BY arrival_time ASC
        """
        self.c.execute(query,(stop_id,weekdayToService(dayOfTheWeek)))
        print(self.c.fetchone())
        return self.convToJson()

    def getStopInfo(self):
        query = "SELECT stop_id,stop_name,stop_lat,stop_lon FROM stops"
        self.c.execute(query)

        return self.convToJson()
    
    def getStopIDs(self):
        query = "SELECT stop_id FROM stops"
        self.c.execute(query)
        idList = []
        for row in self.c: idList.append(row[0])
        return idList
    
    def getGroupedStops(self):
        query = "SELECT * FROM groupedStops"
        self.c.execute(query)
        return self.convToJson()
    
    def getShapes(self):
        query = "SELECT * FROM shapes"
        self.c.execute(query)
        return self.convToJson()
    
    # def getNearestStops(self,lat,lon,amount):
    #     raw = nearest(lat,lon,self.stops,amount)

    #     dwa = depByStop()

    #     print(dwa.scheduleCreator(raw))

        # columns = ["id","name","distance"]
        # data = [dict(zip(columns, row)) for row in raw]
        # return json.dumps(data)
        

# tests 
# if __name__ == '__main__':
#     reque = dbReqeustsHandler()
#     print(reque.getStopIDs())
    # reque.getDeparturesByStop("stop_27_3601",1) 

    # conn = sqlite3.connect('test.db')
    # c = conn.cursor()  

    # c.execute("SELECT stop_name, trip_id, arrival_time, stop_sequence FROM Stop_times INNER JOIN Stops ON Stop_times.stop_id = Stops.stop_id")

    # res = c.fetchmany(5)
    # conn.commit()
    # print(res)

    # conn.commit()
    # conn.close()
