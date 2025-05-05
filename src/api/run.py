import os
import dotenv
from omegaconf import OmegaConf

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.endpoints import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    dotenv.load_dotenv()

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY is not set in environment variables.")
    app.state.api_key = api_key

    app.state.scanner_config = OmegaConf.load(os.getenv("SCANNER_CONFIG_PATH"))
    app.state.report_processing_config = OmegaConf.load(os.getenv("REPORT_PROCESSING_CONFIG_PATH"))["health_expert"]

    yield

app = FastAPI(title="SCULPD Scanner API", lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("src.api.run:app", host="0.0.0.0", port=int(os.getenv("PORT", 8888)), reload=True)
