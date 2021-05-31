from typing import List
from daos.client_dao import ClientDAO
from entities.client import Client
# Import Exceptions here
from services.client_service import ClientService


class ClientServiceImpl(ClientService):

    def __init__(self, client_dao: ClientDAO):
        self.client_dao = client_dao

    def create_client(self, client: Client) -> Client:
        return self.client_dao.create_client(client)

    def show_all_clients(self) -> List[Client]:
        return self.client_dao.show_all_clients()

    def show_client_by_id(self, client_id: int) -> Client:
        return self.client_dao.show_client_by_id(client_id)

    def update_client(self, client: Client) -> Client:
        return self.client_dao.update_client(client)

    def delete_client(self, client_id: int) -> bool:
        return self.client_dao.delete_client(client_id)
