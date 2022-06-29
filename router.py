from flask import Blueprint, jsonify, request
from service import create_new_task, get_all_tasks, remove_task, update_task

task_router = Blueprint('Task', __name__)


def get_body_value(key: str):
    body = request.get_json()
    if (not body):
        raise KeyError(f'Body is required')
    if (key not in body):
        raise KeyError(f'Missing required parameter : {key}')
    return body[key]


@task_router.route('/tasks', methods=['GET'])
def list():
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
        200:
            description: all exist todo tasks
            schema:
                $ref: '#/definitions/list_tasks_response'

    """
    tasks = get_all_tasks()
    return jsonify({
        "result": tasks
    })


@task_router.route('/task', methods=['POST'])
def create():
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

    try:
        name = get_body_value('name')
        if not isinstance(name, str):
            raise KeyError("'name' must be string")

        task = create_new_task(name)
        return jsonify({
            'result': task
        }), 201

    except KeyError as err:
        return err.args[0], 400


@task_router.route('/task/<int:task_id>', methods=['PUT'])
def update(task_id: int):
    """
    Update a specific todo task info
    ---
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

    try:
        if get_body_value('id') != task_id:
            raise KeyError("body's id is not match path")

        name = get_body_value('name')
        if not isinstance(name, str):
            raise KeyError("'name' must be string")

        status_num = get_body_value('status')
        if (status_num == 1):
            status = True
        elif (status_num == 0):
            status = False
        else:
            raise KeyError("The value of status must be '1' or '2'")

        task = update_task(task_id, name, status)

        return jsonify({
            'result': task
        })
    except KeyError as msg:
        return msg.args[0], 400
    except:
        return '', 400


@task_router.route('/task/<int:task_id>/name', methods=['PUT'])
def updata_name(task_id: int):
    """
    Update a specific todo task info
    ---
    definitions:
        name_model:
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
            $ref: '#/definitions/name_model'

    responses:
        200:
            description: Specific todo task has been changed
            schema:
                $ref: '#/definitions/todo_task_response'

    """
    try:
        name = get_body_value('name')
        if not isinstance(name, str):
            raise KeyError("'name' must be string")

        task = update_task(task_id, name=name)

        return jsonify({
            'result': task
        })
    except KeyError as msg:
        return msg.args[0], 400
    except:
        return '', 400


@task_router.route('/task/<int:task_id>/status', methods=['PUT'])
def update_status(task_id: int):
    """
    Update a specific todo task info
    ---
    definitions:
        status_model:
            type: object
            properties:
                status:
                    type: number

    parameters:
        - name: task_id
          in: path
          type: number
          required: true
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/status_model'

    responses:
        200:
            description: Specific todo task has been changed
            schema:
                $ref: '#/definitions/todo_task_response'

    """

    try:
        status_num = get_body_value('status')
        if (status_num == 1):
            status = True
        elif (status_num == 0):
            status = False
        else:
            raise KeyError("The value of status must be number : '0' or '1'")

        task = update_task(task_id, status=status)

        return jsonify({
            'result': task
        })
    except KeyError as msg:
        return msg.args[0], 400
    except:
        return '', 400


@task_router.route('/task/<int:task_id>', methods=['DELETE'])
def delete(task_id: int):
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
    return ''
