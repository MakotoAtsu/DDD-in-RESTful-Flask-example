from distutils.log import error
import pytest
from domain.model import Todo_Task


def test_task_change_name_will_success():
    # arrange
    task = Todo_Task('before')

    # act
    task.change_name('after')

    # assert
    assert 'after' == task.name


def test_task_cannot_change_invalid_name():
    # arrange
    task = Todo_Task('before')

    # act & assert
    with pytest.raises(ValueError):
        task.change_name('')


def test_task_change_status():
    # arrange
    task = Todo_Task('task')
    assert False == task.status

    # act
    task.change_task_status(True)

    # assert
    assert True == task.status
