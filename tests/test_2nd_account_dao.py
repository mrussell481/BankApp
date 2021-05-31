from daos.account_dao import AccountDAO
from daos.account_dao_impl import AccountDaoImplementation
from entities.account import Account


account_dao: AccountDAO = AccountDaoImplementation()

test_account = Account(0, "FirstAccount", "Checking", 100, 1)
account1 = Account(0, "CoolAccount", "Savings", 200, 2)
account3 = Account(0, "GoolAccount", "Savings", 400, 2)
account2 = Account(0, "BoolAccount", "Savings", 600, 2)
account4 = Account(0, "Range Account", "Checking", 1000, 2)


def test_create_account():
    account_dao.create_account(test_account)
    assert test_account.account_id != 0  # Must be set after being created in the DB.


def test_show_client_accounts():
    account_dao.create_account(account1)
    account_dao.create_account(account2)
    account_dao.create_account(account3)
    accounts = account_dao.show_client_accounts(account1.c_id)
    assert len(accounts) >= 3


def test_show_account_by_id():
    third_account = account_dao.show_account_by_id(2, 3)
    assert third_account.account_id == 3


def test_show_account_by_range():
    if len(account_dao.show_account_by_range(2, 950, 1030)) == 1:
        account_range = account_dao.show_account_by_range(2, 950, 1030)
        assert len(account_range) == 1
    else:
        account_dao.create_account(account4)
        account_range = account_dao.show_account_by_range(2, 950, 1030)
        assert len(account_range) == 1


def test_update_account():
    test_account.account_type = "Money Market"
    updated_account = account_dao.update_account(test_account)
    assert updated_account.account_type == test_account.account_type


def test_add_remove_funds():
    # old_account = account_dao.show_account_by_id(2, 3)
    withdraw = account_dao.add_remove_funds(2, 3, -12)
    assert withdraw


def test_transfer_funds():
    result = account_dao.transfer_funds(account1.c_id, account1.account_id, account2.account_id, 50)
    assert result


def test_delete_account():
    result = account_dao.delete_account(account3.c_id, account3.account_id)
    assert result
