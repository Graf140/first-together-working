from contextlib import asynccontextmanager
from fastapi import FastAPI
from apps.gps_tracking_service.config.redis import get_redis
from apps.shared.schemas.gps_tracking_service import StartTrackRequest, AddTrackPointRequest, FinishTrackRequest
from apps.gps_tracking_service.repositories.postgress import start_track, add_point, finish_track

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = get_redis()
    yield
    await app.state.redis.close()

app = FastAPI(title="GPS Tracking Service", lifespan=lifespan)

@app.post("/v1/track/start")
async def start_track_endpoint(req: StartTrackRequest):
    await start_track(req.user_id)
    return {"status": "started", "user_id": req.user_id}

@app.post("/v1/track/point")
async def add_point_endpoint(req: AddTrackPointRequest):
    await add_point(req.user_id, req.point)
    return {"status": "point added"}

@app.post("/v1/track/finish")
async def finish_track_endpoint(req: FinishTrackRequest):
    track_id = await finish_track(req.user_id)
    return {"status": "finished", "track_id": track_id}