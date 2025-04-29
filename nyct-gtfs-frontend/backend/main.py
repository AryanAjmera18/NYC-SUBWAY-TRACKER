from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nyct_gtfs import NYCTFeed

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of feed KEYS, not URLs
FEEDS = ["1", "A", "B", "G", "J", "N", "L", "SIR"]

@app.get("/trains")
def get_trains():
    try:
        trains = []

        for feed_key in FEEDS:
            feed = NYCTFeed(feed_key)
            for trip in feed.trips:
                if trip.stop_time_updates:
                    next_stop = trip.stop_time_updates[0]
                    trains.append({
                        "trip_id": trip.trip_id,
                        "route_id": trip.route_id,
                        "direction": trip.direction,
                        "headsign": trip.headsign_text,
                        "current_status": trip.location_status,
                        "next_stop_name": next_stop.stop_name,
                        "next_stop_eta": str(next_stop.arrival)
                    })

        return trains
    
    except Exception as e:
        return {"error": str(e)}
