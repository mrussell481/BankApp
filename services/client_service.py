from abc import ABC, abstractmethod
from typing import List
from entities.client import Client


class ClientService(ABC):

    @abstractmethod
    def create_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def show_all_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def show_client_by_id(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def delete_client(self, client_id: int) -> bool:
        pass
