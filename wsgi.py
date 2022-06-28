from flask import Flask, redirect
from flasgger import Swagger
from router import task_router

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(task_router)


@app.route('/')
def index():
    return redirect('/apidocs')
