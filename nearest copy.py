import sqlite3
from math import sin, cos, sqrt, atan2, radians


def sortStops():
    conn = sqlite3.connect('dataBase.db')
    c = conn.cursor()  
    query = "SELECT stop_id,stop_name,stop_lat,stop_lon FROM stops"
    c.execute(query)
    stops = c.fetchall() 
    conn.commit()
    conn.close()
    return sorted(stops, key=lambda x: x[3], reverse=False)

# def bis(lat,stops):
#         N = len(stops)
#         if stops[N-1][2] <= lat: return N-1
#         if lat <= stops[0][2] : return 0  
#         s,e = 0,N-1
#         md = 0
#         c = 0
#         while not (stops[md][2] <= lat and stops[md+1][2] >= lat):
#             c += 1
#             if c == 100: break
#             print(s,e)
#             md = (s+e) // 2
#             if stops[md][2] > lat:
#                 e = md
#             else: 
#                 s = md
#         return md

def bis(lon,stops):
    for i in range(len(stops)):
        if i == len(stops)-1: return len(stops)-1
        if lon <= stops[i][3]: return i
    return 0

def dist321(x1,y1,x2,y2): return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)

def dist(x1,y1,x2,y2):
    lat1,lon1,lat2,lon2 = radians(x1),radians(y1),radians(x2),radians(y2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return 6373.0 * c * 1000

def insrt(element,ind,candidates):
    i = 0
    while element > candidates[i][1]: 
        i += 1
        if i == len(candidates): break
    candidates.insert(i,(ind,element))

def nearest(lat,lon,stops,amount=10):
    N = len(stops)
    print(N)
    fnd = bis(lon,stops)
    fna = fnd
    candidates = [(fnd,dist(lat,lon,stops[fnd][2],stops[fnd][3]))]
    compIndex = 0

    strd = dist(lat,lon,lat,stops[fna][3])
    stra = dist(lat,lon,lat,stops[fna][3])

    while strd <= candidates[compIndex][1] or stra <= candidates[compIndex][1] or len(candidates) < amount:
        
        if (fnd <= 0 and stra >= candidates[compIndex][1]) or (fna >= N-1 and strd > candidates[compIndex][1]): break

        if fnd > 0 and strd < candidates[compIndex][1]:
            curd = dist(lat,lon,stops[fnd][2],stops[fnd][3])
            insrt(curd,fnd,candidates)
            fnd -= 1
            if fnd > 0: 
                strd = dist(lat,lon,lat,stops[fnd][3])
                if compIndex + 1 < amount: compIndex += 1

        if fna < N and stra < candidates[compIndex][1]:
            cura = dist(lat,lon,stops[fna][2],stops[fna][3])
            insrt(cura,fna,candidates)
            fna += 1
            if fna < N: 
                stra = dist(lat,lon,lat,stops[fna][3])
                if compIndex + 1 < amount: compIndex += 1

    returnData = []

    for i in range(min(amount,len(candidates))):
        returnData.append([candidates[i][0],stops[candidates[i][0]][1],round(candidates[i][1])])

        #print(stops[candidates[i][0]][1],round(candidates[i][1]))
    #return candidates[0:amount]
    
    # print (returnData)
    return returnData

# stops = sortStops()

# import time
# # vals = nearest(50.0017602,20.1467958,stops,10) Tyniec
# # vals = nearest(50.0138937,19.8725095,stops,10) #ja
# start = time.time()
# vals = nearest(50.0620246,19.9357855,stops,1000) #rynek
# end = time.time()
# print(end-start)
# vals = nearest(50.8817595,20.5227226,stops,15) #kielce
# vals = nearest(50.0184921,19.4110393,stops,5) # LEWO SRODEK

# for i in range(len(vals)):
#     print(stops[vals[i][0]][1])

# print(stops[bis(19.8702,stops)][1])
        
# ind = bis(19.8665163,stops)
# sml = 999
# smi = ind
# for i in range(ind,ind+70):
#     if(dist(50.0135236,19.8716419,stops[i][2],stops[i][3]) < sml):
#         smi = i
#         sml = dist(50.0135236,19.8716419,stops[i][2],stops[i][3])
#     print(stops[i][1],dist(50.0135236,19.8716419,stops[i][2],stops[i][3]))
# print(stops[smi][1])

    # while strd <= candidates[compIndex][1] or stra <= candidates[compIndex][1] or len(candidates) < amount:
        
    #     if fnd == 0 or strd > candidates[compIndex][1]:
    #         cura = dist(lat,lon,stops[fna][2],stops[fna][3])
    #         insrt(cura,fna,candidates)
    #         fna += 1
    #         stra = dist(lat,lon,lat,stops[fna][3])
    #         if compIndex + 1 < amount: compIndex += 1
    #         continue
        
    #     if fna == N-1 or stra > candidates[compIndex][1]:
    #         curd = dist(lat,lon,stops[fnd][2],stops[fnd][3])
    #         insrt(curd,fnd,candidates)
    #         fnd -= 1
    #         strd = dist(lat,lon,lat,stops[fnd][3])
    #         if compIndex + 1 < amount: compIndex += 1
    #         continue
        
    #     curd = dist(lat,lon,stops[fnd][2],stops[fnd][3])
    #     cura = dist(lat,lon,stops[fna][2],stops[fna][3])

    #     insrt(curd,fnd,candidates)
    #     insrt(cura,fna,candidates)
        
    #     fnd -= 1
    #     fna += 1
        
    #     if compIndex + 1 < amount: compIndex += 1
        
    #     strd = dist(lat,lon,lat,stops[fnd][3])
    #     stra = dist(lat,lon,lat,stops[fna][3])