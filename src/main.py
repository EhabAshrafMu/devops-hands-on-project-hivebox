from fastapi import FastAPI
import os

## Application metadata
APP_VERSION = "0.0.1"
APP_NAME = "HiveBox"

## Creating the FastAPI instance
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A scalable rest API for tracking environmental data from IoT devices.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

## Phase-2 implmenetation: Printing the app version
@app.get("/version")
async def get_version():
        return {"version": APP_VERSION,
                "name": APP_NAME}

#launch the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
