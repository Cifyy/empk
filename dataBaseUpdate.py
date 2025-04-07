import sqlite3,schedule,time 
from getData import *
import datetime

def time2seconds(strt) -> int:  return (int(strt[0:2])*3600 + int(strt[3:5])*60)

class updateHandler():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('dataBase.db')
        self.c = self.conn.cursor()  
        
        self.currentBusVersion = ""   
        self.currentTramVersion = ""  

        if os.path.exists("version.txt"):
            version = readVersionFile()
            if version: self.currentBusVersion,self.currentTramVersion = version

        if self.currentBusVersion == "" or self.currentTramVersion == "":
            print("Initializating...")
            fetchNewData()
            self.updateAll()

    def __del__(self) -> None:
        self.conn.commit()
        self.conn.close()

    def updateStopTimes(self,type):
        try:
            path = f"RawData\\{type}_Data\\stop_times.txt"
            newData = getEntries(path,[1,2,4,5,7,8])
            if not newData: raise ValueError
            newData.pop(0)

            self.c.execute("""
            CREATE TABLE IF NOT EXISTS stop_times  (
                trip_id text,
                arrival_time integer,
                stop_id text,
                stop_sequence text,
                pickup_type text, 
                drop_off_type text
            )""")
            self.conn.commit()


            for i,_ in enumerate(newData):
                newData[i][0] += type
                newData[i][1] = time2seconds(newData[i][1])
            
            self.c.executemany("INSERT INTO stop_times VALUES (?,?,?,?,?,?)",newData)
            self.conn.commit()
        except: 
            raise ValueError
    
    def updateRoutes(self,type):
        try:
            path = f"RawData\\{type}_Data\\routes.txt"
            newData = getEntries(path,[1,3])
            if not newData: raise ValueError
            newData.pop(0)
            
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                route_id text,
                route_short_name text
            )""")
            self.conn.commit()
        
            for i,_ in enumerate(newData): 
                newData[i][0] += type
                newData[i][1] = newData[i][1][1:-1]

            if len(newData) == 0 : return 
            self.c.executemany("INSERT INTO routes VALUES (?,?)",newData)
            self.conn.commit()
        except: 
            raise ValueError
    
    def updateStops(self,type):
        try: 
            path = f"RawData\\{type}_Data\\stops.txt"
            newData = getEntries(path,[1,3,5,6])
            if not newData: raise ValueError
            newData.pop(0)

            self.c.execute("""
            CREATE TABLE IF NOT EXISTS stops  (
                stop_id text,
                stop_name text,
                stop_lat Real,
                stop_lon Real
            )""")
            self.conn.commit()
            
            for i,_ in enumerate(newData): newData[i][1] = newData[i][1][1:-1]

            self.c.executemany("INSERT INTO stops VALUES (?,?,?,?)",newData)
            self.conn.commit()
            
            #group Stops
            
            query = """
                SELECT stop_name, ROUND(avg(stop_lat),6) , ROUND(avg(stop_lon),6)
                FROM stops
                GROUP BY stop_name
            """
            self.c.execute(query)
            results = self.c.fetchall()
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS groupedStops  (
                stop_name text,
                stop_lat Real,
                stop_lon Real
            )""")
            self.c.executemany("INSERT INTO groupedStops VALUES (?, ?, ?)", results)
            self.conn.commit()
            
        except: 
            raise ValueError
    
    def updateTrips(self,type):
        try:
            path = f"RawData\\{type}_Data\\trips.txt"
            newData = getEntries(path,[1,2,3,4,6,7])
            if not newData: raise ValueError
            newData.pop(0)
            
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS trips  (
                trip_id text,
                route_id text,
                service_id text,
                trip_headsign text,
                direction_id text,
                block_id text
            )""")
            self.conn.commit()

            for i,_ in enumerate(newData):
                newData[i][0] += type
                newData[i][1] += type

            self.c.executemany("INSERT INTO trips VALUES (?,?,?,?,?,?)",newData)
            self.conn.commit()
        except: 
            raise ValueError
    
    def updateShapes(self):
        try:
            path = f"RawData\\B_Data\\shapes.txt"
            newData = getEntries(path,[1,2,3,4])
            if not newData: raise ValueError
            newData.pop(0)
            
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS shapes  (
                shape_id text,
                shape_pt_lat Real,
                shape_pt_lon Real,
                shape_dist_traveled integer
            )""")
            self.conn.commit()
            
            self.c.executemany("INSERT INTO shapes VALUES (?,?,?,?)",newData)
            self.conn.commit()
        except: 
            raise ValueError
        
    def updateAll(self):
        print("Started")
        self.currentBusVersion = getLastDateFromFile(r"RawData\B_Data\stop_times.txt")
        self.currentTramVersion = getLastDateFromFile(r"RawData\T_Data\stop_times.txt")
        
        updateVersionFile(self.currentBusVersion,self.currentTramVersion)
        
        types = ["B","T"]

        self.c.execute("DROP TABLE IF EXISTS stop_times") 
        self.c.execute("DROP TABLE IF EXISTS routes") 
        self.c.execute("DROP TABLE IF EXISTS stops") 
        self.c.execute("DROP TABLE IF EXISTS groupedStops") 
        self.c.execute("DROP TABLE IF EXISTS trips") 
        self.c.execute("DROP TABLE IF EXISTS shapes") 
        self.conn.commit()
        now = datetime.date.today().strftime('%d-%m-%Y')

        for type in types: 

            try: self.updateStopTimes(type)
            except ValueError: 
                print(f"Failed to Update {type} StopTimes at: ",now)
                return
            try: self.updateRoutes(type)
            except ValueError: 
                print(f"Failed to Update {type} Routes at: ",now)
                return
            try: self.updateStops(type)
            except ValueError: 
                print(f"Failed to Update {type} Stops at: ",now)
                return
            try: self.updateTrips(type)
            except ValueError: 
                print(f"Failed to Update {type} Trips at: ",now)
                return
        try: self.updateShapes()
        except ValueError: 
                print(f"Failed to Update shapes at: ",now)
                return
        print(f"Data Base Successfully Updated to:\nBus Version:  {self.currentBusVersion}\nTram Version: {self.currentTramVersion}")

    def checkForUpdate(self):
        if not fetchNewData():
            print("Failed To Locate Raw Files")
            return
        saved = readVersionFile()
        if not saved:
            print("Failed to read version")
            return 
        if self.currentBusVersion >= saved[0] or self.currentTramVersion >= saved[1]: 
            print("Up to date!: ", datetime.date.today().strftime('%d-%m-%Y'))
            return

        self.updateAll()
        
if __name__ == '__main__':
    
    updater = updateHandler()

    schedule.every().day.at("03:00").do(updater.checkForUpdate)

    while True:
        schedule.run_pending()
        time.sleep(10)