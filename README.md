# empk
A Python application made to fetch, process, and deliver public transport data from MPK Kraków. With a RESTful API, it enables users to access up-to-date departure schedules for individual stops and to identify the closest stops based on location.

## Overview 
The project's purpose is to aggregate public transportation data in a structured and accessible manner. Its core objective is to transform raw transit data into actionable, easily accessible information through an API.

#### Project features two executable files:
- Updater, runs daily at night, checking if newer public data is avaliable, based on version saved in versions.txt file. If an update exists it reinitializes the database with the latest data.
- Api, hosts a FastAPI process on port 8000.

| Endpoint                | Description                  | Parameters                                                                   |
| ----------------------- | ---------------------------- | ---------------------------------------------------------------------------- |
| `GET /stopDepart/`      | Departures by stop           | `stop=<str>`<br>`weekDay=<1-7>`                                            |
| `GET /stopList/`        | All stops list             | *(none)*                                                                     |
| `GET /groupedStopList/` | Stops grouped by name, with locations averaged | *(none)*                                                                     |
| `GET /getNearestStops/` | Nearest stops for a given location      | `lat=<float>`<br>`lon=<float>`<br>`amount=<int>`<br>`dayOfTheWeek=<1-7>` |
