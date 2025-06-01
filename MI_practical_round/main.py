from fastapi import FastAPI

from postgres_conn import create_db_and_tables
from route.emp import route

app = FastAPI()
app.include_router(route)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    app.run("main:app", reload=True)
