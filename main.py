from fastapi import FastAPI, Request

from api.routes.events import router as events_router

app = FastAPI(title="NC plus one", debug=True)
app.include_router(events_router)
