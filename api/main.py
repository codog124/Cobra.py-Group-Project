import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from api.controllers import products
from api.controllers import analytics
from api.controllers import promotions
from api.controllers import customer_orders
from api.controllers import order_tracking
from api.controllers import payments
from api.controllers import reviews


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)
app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(promotions.router)
app.include_router(customer_orders.router)
app.include_router(order_tracking.router)
app.include_router(payments.router)
app.include_router(reviews.router)
if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)