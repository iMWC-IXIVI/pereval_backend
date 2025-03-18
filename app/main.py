from fastapi import FastAPI

from api.v1 import router


app = FastAPI(
    title='Pereval',
    version='1.0.0'
)
app.include_router(router=router)
