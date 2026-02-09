"""HiveBox FastAPI application for environmental sensor data tracking."""

import os
import json
from datetime import datetime, timedelta
from io import BytesIO
import redis
from minio import Minio
import httpx
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge
from apscheduler.schedulers.background import BackgroundScheduler


# Define basic variables for the app, valkey and minio
APP_VERSION = "0.0.2"
APP_NAME = "HiveBox"
VALKEY_HOST = os.getenv("VALKEY_HOST", "localhost")
VALKEY_PORT = int(os.getenv("VALKEY_PORT", 6379))
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "password123")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", 'hivebox-data')
STORAGE_INTERVAL = int(os.getenv("STORAGE_INTERVAL", 300))
#Define custom Prometheus metrics (For caching)
cache_hits = Counter(
    'hivebox_cache_hits_total',
    'Total number of cache hits'
)

cache_misses = Counter(
    'hivebox_cache_misses_total', 
    'Total number of cache misses'
)

temperature_gauge = Gauge(
    'hivebox_current_temperature_celsius',
    'Current average temperature in Celsius'
)

storage_operations = Counter(
    'hivebox_storage_operations_total',
    'Total number of storage operations to MinIO'
)

sensebox_errors = Counter(
    'hivebox_sensebox_errors_total',
    'Total number of errors fetching from senseBoxes'
)
# Make senseBox IDs configurable via environment variables
SENSEBOX_IDS = os.getenv(
    "SENSEBOX_IDS",
    "5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c"
).split(",")

OPENSENSEMAP_API_URL = "https://api.opensensemap.org/boxes"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A scalable rest API for tracking environmental data from IoT devices.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Create a Valkey connection
def get_valkey_client():
    """Create and return a Valkey/Redis client connection."""
    try:
        client = redis.Redis(
            host=VALKEY_HOST,
            port=VALKEY_PORT,
            decode_responses=True  # Returns strings instead of bytes
        )
        # Test connection
        client.ping()
        return client
    except redis.ConnectionError as e:
        print(f"Failed to connect to Valkey: {e}")
        return None

# Create a MinIO connection
def get_minio_client():
    """Create and return a MinIO S3-compatible client connection."""
    try:
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False  # HTTP instead of HTTPS for local dev
        )
        return client
    except Exception as e:
        print(f"Failed to connect to MinIO: {e}")
        return None

# Helper functions to fetch temperatures from the boxes
async def fetch_temperatures_from_senseboxes() -> list[float]:
    temperatures: list[float] = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        for sensebox_id in SENSEBOX_IDS:
            try:
                response = await client.get(f"{OPENSENSEMAP_API_URL}/{sensebox_id.strip()}")
                response.raise_for_status()
                data = response.json()

                for sensor in data.get("sensors", []):
                    if "temperatur" in sensor.get("title", "").lower():
                        last_measurement = sensor.get("lastMeasurement") or sensor.get("LastMeasurement")
                        if not last_measurement:
                            break

                        created_at = last_measurement.get("createdAt")
                        value = last_measurement.get("value")
                        if created_at is None or value is None:
                            break

                        timestamp_str = created_at.replace("Z", "+00:00")
                        timestamp = datetime.fromisoformat(timestamp_str)
                        age = datetime.now(timestamp.tzinfo) - timestamp

                        if age < timedelta(days=7):
                            temperatures.append(float(value))
                        break  # done with this box

            except Exception as e:
                print(f"Error fetching from sensebox {sensebox_id}: {e}")
                sensebox_errors.inc()
                continue

    return temperatures if temperatures else [0.0]

def determine_status(temperature: float) -> str:
    if temperature < 10:
        return "Too cold"
    elif temperature <= 36:
        return "Good"
    else:
        return "Too hot"

def store_to_minio(data: dict):
    minio = get_minio_client()
    if not minio:
        print("MinIO client unavailable, skipping storage")
        return
    try:
        # ensure that the MinIO bucket exists
        if not minio.bucket_exists(MINIO_BUCKET):
            minio.make_bucket(MINIO_BUCKET)

        filename = f"temperature={datetime.now().isoformat()}.json"

        #Convertthe data to JSON bytes
        json_data = json.dumps(data, indent=2)
        json_bytes = json_data.encode('utf-8')

        # Upload to MinIO
        minio.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=filename,
            data=BytesIO(json_bytes),
            length=len(json_bytes),
            content_type='application/json'
        )

        storage_operations.inc()
        print(f"Data stored successfully to MinIO: {filename}")

    except Exception as e:
        print(f"Failed to store data to MinIO: {e}")


async def get_temperature_data():
    # Try cache first
    valkey = get_valkey_client()
    if valkey:
        cached_data = valkey.get("temperature_data")
        if cached_data: #if cached data is a available, then it's a cache hit
            cache_hits.inc()
            data = json.loads(cached_data)
            temperature_gauge.set(data["average"])
            data["cached"] = True
            return data
    # in case it's a cache miss
    cache_misses.inc()

    temperatures = await fetch_temperatures_from_senseboxes()
    
    if not temperatures:
        # All senseBoxes failed
        return {
            "error": "Unable to fetch temperature data",
            "average": 0,
            "status": "Unknown",
            "timestamp": datetime.now().isoformat(),
            "cached": False
        }
    
    # Calculate average
    avg_temp = sum(temperatures) / len(temperatures)
    status = determine_status(avg_temp)
    
    result = {
        "average": round(avg_temp, 2),
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "count": len(temperatures),
        "cached": False
    }
    
    # STEP 3: Store in cache with TTL
    if valkey:
        valkey.setex(
            "temperature_data",
            CACHE_TTL,  # Expire after 5 minutes
            json.dumps(result)
        )
    
    # STEP 4: Update metrics
    temperature_gauge.set(avg_temp)
    
    return result

# We define a bg job to store data in MinIO every 5 mins

def scheduled_storage_job():
    print(f"Storing data inside MinIO. [TIMESTAMP: {datetime.now()}]")

    import asyncio

    async def async_job():
        data = await get_temperature_data()
        if data and not data.get("error"):
            store_to_minio(data)

    asyncio.run(async_job())

# Initialize Prometheus metrics
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Initialize the backgound storage job

scheduler = BackgroundScheduler()

# What happenese during startup and shutdown
@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    
    Responsibilities:
    1. Ensure MinIO bucket exists
    2. Start background scheduler for auto-storage
    3. Log startup information
    """
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Ensure MinIO bucket exists
    minio = get_minio_client()
    if minio:
        try:
            if not minio.bucket_exists(MINIO_BUCKET):
                minio.make_bucket(MINIO_BUCKET)
                print(f"✅ Created MinIO bucket: {MINIO_BUCKET}")
            else:
                print(f"✅ MinIO bucket exists: {MINIO_BUCKET}")
        except Exception as e:
            print(f"⚠️  MinIO bucket check failed: {e}")
    
    # Start background scheduler
    scheduler.add_job(
        scheduled_storage_job,
        'interval',
        seconds=STORAGE_INTERVAL,
        id='storage_job'
    )
    scheduler.start()
    print(f"✅ Background scheduler started (interval: {STORAGE_INTERVAL}s)")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.
    
    Cleanup:
    - Stop background scheduler gracefully
    - Close connections (handled automatically by FastAPI)
    """
    print("🛑 Shutting down...")
    scheduler.shutdown()
    print("✅ Scheduler stopped")



@app.get("/")
async def root():
    """Root endpoint returning welcome message."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": "Environmental sensor data API for beekeepers",
        "endpoints": {
            "/version": "Get application version",
            "/health": "Health check",
            "/temperature": "Get current temperature average",
            "/store": "Manually trigger data storage",
            "/readyz": "Readiness probe for Kubernetes",
            "/metrics": "Prometheus metrics"
        }
    }

@app.get("/temperature")
async def temperature():
    return await get_temperature_data()

@app.get("/version")
async def get_version():
    """Version endpoint returning app version and name."""
    return {"version": APP_VERSION, "name": APP_NAME}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": APP_VERSION}

@app.get("/store")
async def manual_store():
    """Manually trigger data storage to MinIO."""
    data = await get_temperature_data()
    
    if data.get("error"):
        return {
            "status": "error",
            "message": "Unable to fetch temperature data",
            "timestamp": datetime.now().isoformat()
        }
    
    store_to_minio(data)
    
    return {
        "status": "success",
        "message": "Data stored to MinIO",
        "data": data,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/readyz")
async def readiness_probe():
    from fastapi import Response

    # Check if we can reach most of the boxes
    temperatures = await fetch_temperatures_from_senseboxes()
    required_boxes = (len(SENSEBOX_IDS) // 2) +1

    if len(temperatures) < required_boxes:
        return Response(
            content=json.dumps({
                "ready": False,
                "reason": f"Only {len(temperatures)}/{len(SENSEBOX_IDS)} senseBoxes accessible (need {required_boxes})"
            }),
            status_code=503,
            media_type="application/json"
        )
    # Check if the cache is fresh
    valkey = get_valkey_client()
    if valkey:
        cached_data = valkey.get("temperature_data")
        if cached_data:
            data = json.loads(cached_data)
            cache_time = datetime.fromisoformat(data.get("timestamp"))
            age = datetime.now(cache_time.tzinfo) - cache_time
            
            if age > timedelta(minutes=5):
                print(" Cache is stale, but pod is still ready.")
        else:
            print("No cache yet, but pod is still ready") 

    if not valkey:
        return Response(
            content=json.dumps({"ready": False, "reason": "Valkey unavailable"}),
            status_code=503,
            media_type="application/json"
        )
    # Check the cache age
    data = json.loads(cached_data)
    cache_time = datetime.fromisoformat(data.get("timestamp"))
    age = datetime.now(cache_time.tzinfo) - cache_time

    if age > timedelta(minutes=5):
        return Response(
            content=json.dumps({
                "ready": False,
                "reason": f"Cache is stale ({age.seconds}s old)"
            }),
            status_code=503,
            media_type="application/json"
        )

# If all checks passed
    return {
        "ready": True,
        "senseboxes_accessible": len(temperatures),
        "cache_status": "fresh"
    }


# The /metrics endpoint is automatically created by Prometheus instrumentator

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

# if __name__ == "__main__":
#     print("Testing connections...")
    
#     # Test Valkey
#     print("\n1. Testing Valkey connection:")
#     valkey = get_valkey_client()
#     if valkey:
#         print("✅ Valkey connected successfully!")
#         # Try setting and getting a value
#         valkey.set("test_key", "Hello from Valkey!")
#         value = valkey.get("test_key")
#         print(f"   Stored and retrieved: {value}")
#     else:
#         print("❌ Valkey connection failed")
    
#     # Test MinIO
#     print("\n2. Testing MinIO connection:")
#     minio = get_minio_client()
#     if minio:
#         print("✅ MinIO connected successfully!")
#         # Check if bucket exists
#         if not minio.bucket_exists(MINIO_BUCKET):
#             print(f"   Creating bucket: {MINIO_BUCKET}")
#             minio.make_bucket(MINIO_BUCKET)
#         print(f"   Bucket '{MINIO_BUCKET}' is ready!")
#     else:
#         print("❌ MinIO connection failed")
    
#     print("\n✨ Connection tests complete!\n")