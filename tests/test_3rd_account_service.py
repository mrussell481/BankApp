from unittest.mock import MagicMock
from entities.account import Account
from services.account_service import AccountService
from services.account_service_impl import AccountServiceImpl
from daos.account_dao_impl import AccountDaoImplementation

test_account = Account(1, "Test Account", "Checking", 1, 2)

mock_dao = AccountDaoImplementation()
mock_dao.show_account_by_id = MagicMock(return_value=test_account)
test_account = mock_dao.show_account_by_id()

account_service: AccountService = AccountServiceImpl(mock_dao)


def test_add_remove_funds():
    assert account_service.add_remove_funds(2, 3, 90)


def test_transfer_funds():
    assert account_service.transfer_funds(2, 3, 4, 20)