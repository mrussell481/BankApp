from daos.client_dao import ClientDAO
from daos.client_dao_impl import ClientDaoImplementation
from entities.client import Client


client_dao: ClientDAO = ClientDaoImplementation()

test_client = Client(0, "Cool Guy")


def test_create_client():
    client_dao.create_client(test_client)
    assert test_client.client_id != 0  # test_client's ID should be updated in the backend after being set in the DB.


def test_show_all_clients():
    client1 = Client(0, "Tom")
    client2 = Client(0, "Dick")
    client3 = Client(0, "Chaney")
    client_dao.create_client(client1)
    client_dao.create_client(client2)
    client_dao.create_client(client3)
    clients = client_dao.show_all_clients()
    assert len(clients) >= 3


def test_show_client_by_id():
    testclient = client_dao.show_client_by_id(3)
    assert testclient.client_id == 3


def test_update_client():
    clientupdate = Client(3, "Moe")
    client = client_dao.update_client(clientupdate)
    assert client.client_name == "Moe"  # Same as with the create test.


def test_delete_client():
    result = client_dao.delete_client(4)
    assert result
