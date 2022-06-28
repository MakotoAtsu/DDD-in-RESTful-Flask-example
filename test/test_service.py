import pytest
from pytest_mock import MockerFixture
from domain.model.todo_task import Todo_Task
from service import create_new_task, get_all_tasks, remove_task, update_task, repo


def test_create_new_task_will_save_to_repo(mocker: MockerFixture):
    # arrange
    expected = Todo_Task('new task')
    expected.id = 10
    mocked_create = mocker.patch.object(
        repo, 'create', return_value=expected)

    # act
    result = create_new_task('new task')

    # assert
    mocked_create.assert_called_once()
    assert {
        'id': 10,
        'name': 'new task',
        'status': 0
    } == result


def test_update_task_will_save_into_repo(mocker: MockerFixture):
    # arrange
    task = Todo_Task('old')
    task.id = 5
    mocked_get = mocker.patch.object(repo, 'read', return_value=task)
    mocked_update = mocker.patch.object(repo, 'update', return_value=task)

    # act
    result = update_task(5, 'new name', True)

    # assert
    assert 'new name' == task.name
    assert True == task.status
    mocked_get.assert_called_once_with(5)
    mocked_update.assert_called_once_with(task)
    assert {
        'id': task.id,
        'name': task.name,
        'status': task.status
    } == result


def test_update_task_will_raise_error_if_task_id_not_exist(mocker: MockerFixture):
    # arrange
    mocked_get = mocker.patch.object(repo, 'read', return_value=None)
    mocked_update = mocker.patch.object(repo, 'update')

    # act
    with pytest.raises(KeyError) as msg:
        update_task(15)

    # assert
    mocked_get.assert_called_once_with(15)
    mocked_update.assert_not_called()


def test_delete_task_will_delete_from_repo(mocker: MockerFixture):
    # arrange
    mocked_delete = mocker.patch.object(repo, 'delete')

    # act
    remove_task(10)

    # assert
    mocked_delete.assert_called_once_with(10)


def test_list_all_will_get_from_repo(mocker: MockerFixture):
    # arrange
    all_tasks: list[Todo_Task] = []
    for i in range(0, 10):
        task = Todo_Task(f'Task {i}')
        task.id = i
        task.status = (i % 3 == 0)
        all_tasks.append(task)

    mocked_list = mocker.patch.object(repo, 'list_all', return_value=all_tasks)

    # act
    result = get_all_tasks()

    # assert
    mocked_list.assert_called_once()
    assert [{
        'id': t.id,
        'name': t.name,
        'status': 1 if t.status else 0
    } for t in all_tasks] == result
