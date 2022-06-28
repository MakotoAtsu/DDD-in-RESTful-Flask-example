from flask import Blueprint, jsonify, request

task_router = Blueprint('Task', __name__)


@task_router.route('/tasks', methods=['GET'])
def list_all_tasks():
    return 'OK - ALL Tasks'


@task_router.route('/task', methods=['POST'])
def create_task():
    body = request.get_json()
    return jsonify(body)


@task_router.route('/task/<int:task_id>', methods=['PUT', 'DELETE'])
def update_task(task_id: int):
    body = request.get_json()

    return f'OK - PUT or DELETE task:{task_id}'
