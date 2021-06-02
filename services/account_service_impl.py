from typing import List
from daos.account_dao import AccountDAO
from entities.account import Account
from services.account_service import AccountService
from exceptions.account_not_found import AccountNotFound
# Exceptions here


class AccountServiceImpl(AccountService):

    def __init__(self, account_dao: AccountDAO):
        self.account_dao = account_dao

    def create_account(self, account: Account) -> Account:
        return self.account_dao.create_account(account)

    def show_client_accounts(self, client_id: int) -> List[Account]:
        return self.account_dao.show_client_accounts(client_id)

    def show_account_by_id(self, client_id: int, account_id: int) -> Account:
        return self.account_dao.show_account_by_id(client_id, account_id)

    def show_account_by_range(self, client_id: int, less_amount: int, greater_amount: int) -> List[Account]:
        return self.account_dao.show_account_by_range(client_id, less_amount, greater_amount)

    def update_account(self, account: Account) -> Account:
        return self.account_dao.update_account(account)

    def add_remove_funds(self, client_id: int, account_id: int, change: int) -> bool:
        test_account = self.account_dao.show_account_by_id(client_id, account_id)
        if (test_account.funds + change) < 0:
            return False
        return self.account_dao.add_remove_funds(client_id, account_id, change)

    def transfer_funds(self, client_id: int, account_id_1: int, account_id_2: int, change: int) -> bool:
        test_account = self.account_dao.show_account_by_id(client_id, account_id_1)
        if (test_account.funds + change) < 0:
            return False
        return self.account_dao.transfer_funds(client_id, account_id_1, account_id_2, change)

    def delete_account(self, client_id: int, account_id: int) -> bool:
        return self.account_dao.delete_account(client_id, account_id)
