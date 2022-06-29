from pytest_mock import MockerFixture
from wsgi import app


def get_app_client():
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()


def test_create_endpoint_will_call_create_service(mocker: MockerFixture):

    # arrange
    test_client = get_app_client()
    expected = {
        "id": 0,
        "name": "Task1",
        "status": 0
    }
    mocked_create = mocker.patch('router.create_new_task')
    mocked_create.return_value = expected

    # act
    response = test_client.post('/task',
                                json={
                                    "name": "Task1"
                                })

    # assert
    mocked_create.assert_called_once_with('Task1')
    assert 201 == response.status_code
    assert {"result": expected} == response.json


def test_create_endpoint_will_return_400_if_missing_name(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_create = mocker.patch('router.create_new_task')

    # act
    response = test_client.post('/task',
                                json={
                                    "name1": "Task1"
                                })

    # assert
    assert 400 == response.status_code
    mocked_create.assert_not_called()


def test_list_all_endpoint_will_call_get_all_tasks_service(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_list = mocker.patch('router.get_all_tasks')
    expected = [
        {
            "id": 5,
            "name": "pending",
            "status": 0
        },
        {
            "id": 6,
            "name": "done",
            "status": 1
        }
    ]
    mocked_list.return_value = expected

    # act
    response = test_client.get('/tasks')

    # assert
    mocked_list.assert_any_call()
    assert 200 == response.status_code
    assert {"result": expected} == response.json


def test_update_endpoint_will_call_update_service(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_update = mocker.patch('router.update_task')
    expected = {
        "id": 3,
        "name": "new name",
        "status": 1
    }
    mocked_update.return_value = expected

    # act
    response = test_client.put('/task/3', json=expected)

    # assert
    mocked_update.assert_called_once_with(3, 'new name', True)
    assert 200 == response.status_code
    assert {"result": expected} == response.json


def test_update_endpoint_will_return_400_if_target_not_found(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_update = mocker.patch('router.update_task')
    mocked_update.side_effect = KeyError('not found')

    # act
    response = test_client.put('/task/3', json={
        "id": 3,
        "name": "new name",
        "status": 1
    })

    # assert
    assert 400 == response.status_code


def test_update_particular_member_of_task_will_call_update_service_with_name_parameter(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_update = mocker.patch('router.update_task')
    expected = {
        "id": 3,
        "name": "new name",
        "status": 1
    }
    mocked_update.return_value = expected

    # act
    response = test_client.put('/task/3/name', json={
        "name": "new name"
    })

    # assert
    mocked_update.assert_called_once_with(3, name='new name')
    assert 200 == response.status_code
    assert {"result": expected} == response.json


def test_update_particular_member_of_task_will_call_update_service_with_status_parameter(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_update = mocker.patch('router.update_task')
    expected = {
        "id": 3,
        "name": "new name",
        "status": 1
    }
    mocked_update.return_value = expected

    # act
    response = test_client.put('/task/3/status', json={
        "status": 1
    })

    # assert
    mocked_update.assert_called_once_with(3, status=True)
    assert 200 == response.status_code
    assert {"result": expected} == response.json


def test_delete_endpoint_will_call_delete_service(mocker: MockerFixture):
    # arrange
    test_client = get_app_client()
    mocked_delete = mocker.patch('router.remove_task')

    # act
    response = test_client.delete('/task/10')

    # assert
    mocked_delete.assert_called_once_with(10)
    assert 200 == response.status_code
