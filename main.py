from fastapi import FastAPI
from dbRequests import dbReqeustsHandler
from getData import readVersionFile
from fastapi import Response
from departureByStop import depByStop
import time

req = dbReqeustsHandler()
app = FastAPI()
nereq = depByStop()

@app.get("/")
async def root():
    return {"empk api"}

@app.get("/version")
async def root():
    resp = readVersionFile()
    return {"busVersion":resp[0] , "tramVersion":resp[1]}

@app.get("/stopDepart/")
async def read_item(stop: str = "0", weekDay: int = 1):
    if stop == 0: return "Invalid_Stop_ID"
    return Response(content=req.getDeparturesByStop(stop,weekDay), media_type="application/json")

@app.get("/stopList/")
async def root():
    return Response(content=req.getStopInfo(), media_type="application/json")

@app.get("/groupedStopList/")
async def root():
    return Response(content=req.getGroupedStops(), media_type="application/json")

@app.get("/getNearestStops/")
async def read_item(lat: float = -1, lon: float = -1, amount: int = 5, dayOfTheWeek: int = 1):
    if lat == -1 or lon == -1: return "Invalid Coordinates"
    start = time.time()
    response = nereq.getNearestStops(lat,lon,amount,dayOfTheWeek)
    end = time.time()
    print("Total Time:",end - start)
    return Response(content=response)

# @app.get("/stopsDepartures/")
# async def read_item(weekDay: int = 1):
#     return Response(content=req.get, media_type="application/json")

# @app.get("/shapes/")
# async def root():
#     return Response(content=req.getShapes(), media_type="application/json")
