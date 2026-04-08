from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.database import Base, engine
from src.products.router import product_router
from src.auth.router import user_router, auth


Base.metadata.create_all(bind=engine)

app = FastAPI()

auth.handle_errors(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    product_router,
    prefix="/api/v1",
)


app.include_router(
    user_router,
    prefix="/api/v1",
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")