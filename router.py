from typing import Any
from flask import Blueprint, jsonify, request
from service import create_new_task, get_all_tasks, remove_task, update_task_status

task_router = Blueprint('Task', __name__)


def get_body_value(body: Any, key: str):
    if (key not in body):
        raise KeyError(f'Missing required parameter : {key}')
    return body[key]


@task_router.route('/tasks', methods=['GET'])
def list_all_tasks():
    """
    Get all todo tasks
    ---
    definitions:
        Todo_Task:
            type: object
            properties:
                id: 
                    type: number
                name:
                    type: string
                status:
                    type: number

        list_tasks_response:
            type: object
            properties:
                result:
                    type: array
                    items: 
                        $ref: '#/definitions/Todo_Task'

    responses:
        201:
            description: all exist todo tasks
            schema:
                $ref: '#/definitions/list_tasks_response'

    """
    tasks = get_all_tasks()
    return jsonify({
        "result": tasks
    })


@task_router.route('/task', methods=['POST'])
def create_task():
    """
    Create a new todo task
    ---
    definitions:
        create_model:
            type: object
            properties:
                name:
                    type: string

        todo_task_response:
            type: object
            properties:
                result:
                    $ref: '#/definitions/Todo_Task'

    parameters:
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/create_model'
    responses:
        201:
            description: A new todo task has been created
            schema:
                $ref: '#/definitions/todo_task_response'

    """

    body = request.get_json()
    if not body:
        return 'require body', 400
    name = body['name']
    if not name:
        return 'Missing parameter : \'name\''

    task = create_new_task(name)
    return jsonify({
        'result': task
    })


@task_router.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    """
    Update a specific todo task info
    ---
    definitions:
        update_model:
            type: object
            properties:
                name:
                    type: string

    parameters:
        - name: task_id
          in: path
          type: number
          required: true
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/Todo_Task'

    responses:
        200:
            description: Specific todo task has been changed
            schema:
                $ref: '#/definitions/todo_task_response'

    """
    body = request.get_json()

    if not body:
        return 'body is required', 400

    if not body['id'] or body['id'] != task_id:
        return "body's id is not match path"

    name = ''
    status = True

    try:
        name = get_body_value(body, 'name')
        status_num = get_body_value(body, 'status')
        if (status_num == 1):
            status = True
        elif (status_num == 0):
            status = False
        else:
            raise KeyError("The value of status must be '1' or '2'")

        task = update_task_status(task_id, name, status)

        return jsonify({
            'result': task
        })
    except KeyError as msg:
        return msg.args[0], 400
    except:
        return '', 400


@task_router.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """
    delete a specific todo task 
    ---
    parameters:
        - name: task_id
          in: path
          type: number
          required: true

    responses:
        200:
            description: Specific todo task already remove
    """

    remove_task(task_id)
    return '', 200
