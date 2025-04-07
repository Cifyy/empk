import sqlite3,pickle
from dbRequests import weekdayToService

class stopDepartureCreator():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('dataBase.db')
        self.c = self.conn.cursor()  
    
        self.query = """
            SELECT route_short_name, arrival_time 
            FROM stop_times INNER JOIN (trips INNER JOIN routes ON trips.route_id = routes.route_id) ON trips.trip_id = stop_times.trip_id
            WHERE stop_id = ? AND service_id = ?
            ORDER BY arrival_time ASC
            """
        self.addQuery = """
            CREATE TABLE IF NOT EXISTS departures_by_stop (
                stop_id text,
                dayOfTheWeek integer,
                departures blob
            )
        """
        self.insertQuery = """
            INSERT INTO departures_by_stop 
            (stop_id, dayOfTheWeek, departures)
            VALUES (?,?,?)
        """

    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()
    
    def stops(self): 
        query = "SELECT stop_id FROM stops"
        self.c.execute(query)
        stops = self.c.fetchall() 
        self.conn.commit()
        return sorted(stops, key=lambda x: x[0], reverse=False)

    def createTableForStop(self,stop_id,dayOfTheWeek):
        self.c.execute(self.query,(stop_id,weekdayToService(dayOfTheWeek)))
        self.conn.commit()

        data = self.c.fetchall()
        binaryData = pickle.dumps(data)

        self.c.execute(self.insertQuery,(stop_id,dayOfTheWeek,binaryData))
        self.conn.commit()

    def createDataBase(self):
        self.c.execute("DROP TABLE IF EXISTS departures_by_stop") 
        
        self.c.execute(self.addQuery) 
        stops = self.stops()

        days = [1,5,6,7]
        progress = 0
        total = len(stops)*len(days)

        for day in days:
            for stop in stops:
                print("Currently on:",progress,"Day:",day," ",progress/total)
                self.createTableForStop(stop[0],day)
                progress += 1

    def retrieve(self,stop_id,dayOfTheWeek):
        query = """
            SELECT departures
            FROM departures_by_stop
            WHERE stop_id = ? AND dayOfTheWeek = ? 
        """
        self.c.execute(query,(stop_id,dayOfTheWeek))
        self.conn.commit()

        binaryData = self.c.fetchall()
        data = pickle.loads(binaryData[0][0])
        return data
        

if __name__ == '__main__':
    import time
    dwa = stopDepartureCreator()
    dwa.createDataBase()
    print(dwa.retrieve("stop_1054_257002",7))

        