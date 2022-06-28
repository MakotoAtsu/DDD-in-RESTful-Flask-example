from flask import Flask
from router import task_router

app = Flask(__name__)
app.register_blueprint(task_router)


@app.route('/')
def index():
    return "OK"
