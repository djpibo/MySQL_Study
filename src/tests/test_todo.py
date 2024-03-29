# test_ : method convention to recognize for pytest
from database.orm import ToDo
from database.repository import ToDoRepository


def test_health_check_handler(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


# Reason for Using MOCK : To prepare insert/update ops in real database.
def test_get_todos(client, mocker):
    # mock : make some sample data without manipulating database
    mocker.patch.object(ToDoRepository, "get_todos",  # DB test
                        return_value=[
                            ToDo(id=1, contents="string", is_done=True),
                            ToDo(id=2, contents="string", is_done=True),
                            ToDo(id=3, contents="string", is_done=True)
                        ])
    response = client.get("/todos?order=DESC")  # api test
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 3, "contents": "string", "is_done": True},
            {"id": 2, "contents": "string", "is_done": True},
            {"id": 1, "contents": "string", "is_done": True}
        ]
    }


def test_get_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="string", is_done=True))
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "string", "is_done": True}

    # 404
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=None
    )
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found!"}


def test_create_todo(client, mocker):
    # mocker-spy is testing util for tracking method parameter
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch.object(
        ToDoRepository, "create_todo",
        return_value=ToDo(id=1, contents="string", is_done=True)
    )

    body = {
        "contents": "test",
        "is_done": False,
    }
    response = client.post("/todos", json=body)

    # using mocker-spy for test method-"create"
    # method-"create" is insert query
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "string", "is_done": True}


def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="string", is_done=True)
    )
    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch.object(
        ToDoRepository, "update_todo",
        return_value=ToDo(id=1, contents="string", is_done=False)
    )
    response = client.patch("/todos/1")
    undone.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "string", "is_done": False}

    # 404
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=None)
    response = client.get("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found!"}


def test_delete_todo(client, mocker):
    # 204
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=ToDo(id=1, contents="string", is_done=True))
    mocker.patch("api.todo.delete_todo", return_value=None)
    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(
        ToDoRepository, "get_todo_by_todo_id",
        return_value=None)
    response = client.get("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found!"}
