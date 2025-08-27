"""HiveBox FastAPI application for environmental sensor data tracking."""

import os
from datetime import datetime, timedelta

import httpx
from fastapi import FastAPI

APP_VERSION = "0.0.1"
APP_NAME = "HiveBox"

# The 3 senseBox devices we'll get temperature from
SENSEBOX_IDS = [
    "5eba5fbad46fb8001b799786",
    "5c21ff8f919bf8001adf2488",
    "5ade1acf223bd80019a1011c"
]
OPENSENSEMAP_API_URL = "https://api.opensensemap.org/boxes"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A scalable rest API for tracking environmental data from IoT devices.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


@app.get("/")
async def root():
    """Root endpoint returning welcome message."""
    return {"message": f"Welcome to {APP_NAME} API v{APP_VERSION}"}


@app.get("/version")
async def get_version():
    """Version endpoint returning app version and name."""
    return {"version": APP_VERSION, "name": APP_NAME}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": APP_VERSION}


def extract_temperature_from_box(box_data, one_hour_ago):
    """Extract temperature from senseBox data if available and fresh."""
    for sensor in box_data.get("sensors", []):
        if sensor.get("title", "").lower() in ["temperatur", "temperature"]:
            last_measurement = sensor.get("lastMeasurement")
            if last_measurement:
                measurement_time = datetime.fromisoformat(
                    last_measurement["createdAt"].replace("Z", "+00:00")
                ).replace(tzinfo=None)

                if measurement_time >= one_hour_ago:
                    return float(last_measurement["value"])
            break
    return None


@app.get("/temperature")
async def get_temperature():
    """Get average temperature from configured senseBox devices."""
    try:
        temperatures = []
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)

        async with httpx.AsyncClient(timeout=10.0) as client:
            for box_id in SENSEBOX_IDS:
                try:
                    response = await client.get(f"{OPENSENSEMAP_API_URL}/{box_id}")
                    if response.status_code == 200:
                        box_data = response.json()
                        temp_value = extract_temperature_from_box(box_data, one_hour_ago)
                        if temp_value is not None:
                            temperatures.append(temp_value)
                except httpx.RequestError:
                    continue

        if not temperatures:
            return {
                "error": "No recent temperature data available",
                "average_temperature": None
            }

        average_temp = sum(temperatures) / len(temperatures)
        return {
            "average_temperature": round(average_temp, 2),
            "sensor_count": len(temperatures),
            "timestamp": current_time.isoformat()
        }

    except (httpx.RequestError, ValueError, KeyError) as exc:
        return {
            "error": f"Failed to fetch temperature data: {str(exc)}",
            "average_temperature": None
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
    