
import uvicorn
from fastapi import FastAPI

from src.clients.controllers import router as clients_router
from src.gym_classes.controllers import router as gym_classes_router
from src.gym_passes.controllers import router as gym_passes_router


app = FastAPI()
app.include_router(gym_classes_router)
app.include_router(clients_router)
app.include_router(gym_passes_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
