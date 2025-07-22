from fastapi import FastAPI, Request
from users.routes import router as user_router
from video_converter.routes import router as converter_router
from utils.database import Base, engine
from middlewares.logging import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(user_router, prefix="", tags=["users"])
app.include_router(converter_router, prefix="/converter", tags=["converter"])
