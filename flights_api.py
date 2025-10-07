from fastapi import FastAPI
import logging
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time
import random


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  


class Flight(BaseModel):
    dep: str = 'Manchester'
    arr: str
    airline : str
    dep_date: datetime
    dep_land_date : datetime
    ret_date : Optional[datetime] = None
    ret_land_date : Optional[datetime] = None

class FlightsResponse(BaseModel):
    status: str
    message: str
    flights: List[Flight]

 

app = FastAPI()

@app.get("/hello")
def hello_world(name : str = 'Ismaeel'):
  logger.info(f'hello world request for {name}')
  return {"message" : f"hello, {name}"}

@app.get("/flights/", response_model=FlightsResponse)
def flights(destination : str, dep_date : date, ret_date : date):
  logger.info(f"Request: destination={destination}, dep_date={dep_date}, ret_date={ret_date}")
  
  return get_flights_info(destination, dep_date, ret_date)



def get_flights_info(destination, dep_date, ret_date):
  flights = []
  airlines = ['Ryanair', 'British Airways', 'Turkish Airways', 'Qatar Airways', 'Emirates']
  try:
    num_flights = random.randint(1, 4)
    for i in range(num_flights):
      airline = random.choice(airlines)
      flights.append(Flight(arr = destination,
                      airline = airline,
                      dep_date = random_time_on_date(dep_date, True),
                      dep_land_date = random_time_on_date(dep_date, False),
                      **({"ret_date": random_time_on_date(ret_date, True),
                      "ret_land_date": random_time_on_date(ret_date, False)} if ret_date is not None else {})

    return FlightsResponse(status = "ok", message = "Flights found.", flights = flights)
  except Exception as e:
    logger.error("Error generating flights", exc_info=True)
    return FlightsResponse(status = "error", message = "Error in finding Flights information. Please try again later.", flights=[])


def random_time_on_date(date_obj, first_half=True):
    random_hour = random.randint(0, 12) if first_half else random.randint(12, 23)
    return datetime.combine(date_obj, time(random_hour))
