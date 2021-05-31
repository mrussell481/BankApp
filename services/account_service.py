from abc import ABC, abstractmethod
from typing import List
from entities.account import Account


class AccountService(ABC):


    @abstractmethod
    def create_account(self, account: Account) -> Account:  # "[Account name] created successfully."
        pass

    @abstractmethod
    def show_client_accounts(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def show_account_by_id(self, client_id: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def show_account_by_range(self, client_id: int, less_amount: int, greater_amount: int) -> List[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> Account:  # "[Account name] updated successfully."
        pass

    @abstractmethod
    def add_remove_funds(self, client_id: int, account_id: int, change: int) -> Account:  # "Added funds to [Account name]."
        pass

    @abstractmethod
    def transfer_funds(self, client_id: int, account_id_1: int, account_id_2: int, change: int) -> bool:  # "Transfer successful."
        pass

    @abstractmethod
    def delete_account(self, client_id: int, account_id: int) -> bool:  # "Account removed."
        pass
