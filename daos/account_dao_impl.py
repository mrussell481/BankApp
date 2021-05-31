from typing import List
from daos.account_dao import AccountDAO
from entities.account import Account
from utils.connection_util import connection


class AccountDaoImplementation(AccountDAO):

    def create_account(self, account: Account) -> Account:
        cursor = connection.cursor()
        sql = """select * from account where c_id = {} """.format(account.c_id)
        cursor.execute(sql)
        accounts = cursor.fetchall()
        account_list = []
        for x in accounts:
            account_list.append(x)
        if len(account_list) == 0:
            account.account_id = 1
        else:
            account.account_id = (account_list[-1][0]) + 1
        sql = """insert into account (account_id, account_name, account_type, funds, c_id) values (
                    {}, '{}', '{}', {}, {})""".format(account.account_id, account.account_name, account.account_type,
                                                      account.funds, account.c_id)
        cursor.execute(sql)
        connection.commit()
        return account

    def show_client_accounts(self, client_id: int) -> List[Account]:
        cursor = connection.cursor()
        sql = """select * from account where c_id = {}""".format(client_id)
        cursor.execute(sql)
        records = cursor.fetchall()
        account_list = []
        for x in records:
            account_list.append(Account(*x))
        return account_list

    def show_account_by_id(self, client_id: int, account_id: int) -> Account:
        cursor = connection.cursor()
        sql = """select * from account where c_id = {} and account_id = {}""".format(client_id, account_id)
        cursor.execute(sql)
        record = cursor.fetchone()
        account = Account(*record)
        return account

    def show_account_by_range(self, client_id: int, less_amount: int, greater_amount: int) -> List[Account]:
        cursor = connection.cursor()
        sql = """select * from account where c_id = {} and funds between {} and {}""".format(client_id, less_amount, greater_amount)
        cursor.execute(sql)
        records = cursor.fetchall()
        account_list = []
        for x in records:
            account_list.append(Account(*x))
        return account_list

    def update_account(self, account: Account) -> Account:
        cursor = connection.cursor()
        sql = """update account set account_name = '{}', account_type = '{}'
         where c_id = {} and account_id = {}""".format(account.account_name, account.account_type,
                                                       account.c_id, account.account_id)
        cursor.execute(sql)
        connection.commit()
        return account

    def add_remove_funds(self, client_id: int, account_id: int, change: int) -> Account:
        pass

    def transfer_funds(self, client_id: int, account_id_1: int, account_id_2: int, change: int) -> bool:
        pass

    def delete_account(self, client_id: int, account_id: int) -> bool:
        pass
