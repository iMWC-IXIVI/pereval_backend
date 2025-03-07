from fastapi import FastAPI


app = FastAPI(
    title='Pereval',
    version='1.0.0'
)


@app.get('/')
def start_project():
    return {'message': 'success'}
