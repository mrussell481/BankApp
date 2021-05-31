from abc import ABC, abstractmethod
from typing import List
from entities.client import Client


# The following shows how inputs and outputs work in methods.
# Inputs represent what the database needs to know; creating and updating both require full book objects,
# but to retrieve a client, only the ID is required.
# Outputs are what a method changes into when it completes;
# The message that displays when a client is deleted doesn't change depending on ID, so only a bool is needed.
class ClientDAO(ABC):

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
