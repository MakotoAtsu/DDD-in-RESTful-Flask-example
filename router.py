from flask import Blueprint, jsonify, request

task_router = Blueprint('Task', __name__)


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

    return 'OK - ALL Tasks'


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
    return jsonify(body)


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

    return f'OK - PUT or DELETE task:{task_id}'


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
    return 'OK'
