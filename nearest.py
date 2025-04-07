import sqlite3
from math import sin, cos, sqrt, atan2, radians
import time

def sortStops():
    conn = sqlite3.connect('dataBase.db')
    c = conn.cursor()  
    query = "SELECT stop_id,stop_name,stop_lat,stop_lon FROM stops"
    c.execute(query)
    stops = c.fetchall() 
    conn.commit()
    conn.close()
    return sorted(stops, key=lambda x: x[3], reverse=False)

def bis(lon,stops):
    lt = 0
    rt = len(stops) - 1

    while lt <= rt:
        md = (lt+rt) // 2
        if lon > stops[md][3]:
            lt = md + 1
        elif lon < stops[md][3]:
            rt = md - 1
        else: return md

    if lt < len(stops) and stops[lt][3] == lon: 
        return lt
    
    if lt == len(stops): return len(stops)

    return 0

    # for i in range(len(stops)):
    #     if i == len(stops)-1: return len(stops)-1
    #     if lon <= stops[i][3]: return i

    
# T = [0,0.43,1.59,1.87,1.96,2.5,2.8]
# print(bis(3,T))

def dist321(x1,y1,x2,y2): return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)

def dist(x1,y1,x2,y2):
    lat1,lon1,lat2,lon2 = radians(x1),radians(y1),radians(x2),radians(y2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return 6373.0 * c * 1000

def insrt(element,ind,candidates,name):
    i = 0
    for x in candidates:
        if x[2] == name: return False
    while element > candidates[i][1]: 
        i += 1
        if i == len(candidates): break
    candidates.insert(i,(ind,element,name))
    return True

def idToName(stopID,stops): 
    for stop in stops:
        if stopID == stop[0]:
            return stop[1]
    
def nearest(lat,lon,stops,amount=10):
    N = len(stops)
    fnd = bis(lon,stops)
    fna = fnd
    candidates = [(fnd,dist(lat,lon,stops[fnd][2],stops[fnd][3]),stops[fnd])]
    compIndex = 0

    strd = dist(lat,lon,lat,stops[fna][3])
    stra = dist(lat,lon,lat,stops[fna][3])

    # start = time.time()

    c = 0
    while strd <= candidates[compIndex][1] or stra <= candidates[compIndex][1] or len(candidates) < amount:
        c += 1
        if (fnd <= 0 and stra >= candidates[compIndex][1]) or (fna >= N-1 and strd > candidates[compIndex][1]): break

        if fnd > 0 and strd < candidates[compIndex][1]:
            curd = dist(lat,lon,stops[fnd][2],stops[fnd][3])
            if insrt(curd,fnd,candidates,idToName(stops[fnd][0],stops)) == False: compIndex -= 1
            fnd -= 1
            if fnd > 0: 
                strd = dist(lat,lon,lat,stops[fnd][3])
                if compIndex + 1 < amount: compIndex += 1

        if fna < N and stra < candidates[compIndex][1]:
            cura = dist(lat,lon,stops[fna][2],stops[fna][3])
            if insrt(cura,fna,candidates,idToName(stops[fna][0],stops)) == False: compIndex -= 1
            fna += 1
            if fna < N: 
                stra = dist(lat,lon,lat,stops[fna][3])
                if compIndex + 1 < amount: compIndex += 1
    # end = time.time()
    # print("searching took",end-start)
    returnData = []

    for i in range(min(amount,len(candidates))):
        returnData.append([stops[candidates[i][0]][1],round(candidates[i][1])])

    stopToSchedule = stopScheduler(stops,returnData)
    return stopToSchedule

def stopScheduler(allStops,stops):
    
    allStopList = []
    for curStop in stops:
        forName = []
        for stop in allStops:
            if curStop[0] == stop[1]:
                forName.append(stop[0])
        allStopList.append((curStop[0],curStop[1],forName))
    
    return allStopList
    #print(allStopList)


# print(idToName("stop_3_502",sortStops()))

#vals = nearest(50.0017602,20.1467958,sortStops(),10) #Tyniec
#vals = nearest(50.0138937,19.8725095,sortStops(),10) #ja
# vals = nearest(50.0620246,19.9357855,sortStops(),10) #rynek
# vals = nearest(50.8817595,20.5227226,stops,15) #kielce
# vals = nearest(50.0184921,19.4110393,stops,5) # LEWO SRODEK

