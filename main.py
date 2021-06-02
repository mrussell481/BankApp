from flask import Flask, request, jsonify
from daos.client_dao_impl import ClientDaoImplementation
from daos.account_dao_impl import AccountDaoImplementation
from exceptions.client_not_found import ClientNotFound
from exceptions.account_not_found import AccountNotFound
from exceptions.bad_request import BadRequest
from services.client_service_impl import ClientServiceImpl
from services.account_service_impl import AccountServiceImpl
from entities.client import Client
from entities.account import Account
# Exceptions go here.
import logging

app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

client_dao = ClientDaoImplementation()
account_dao = AccountDaoImplementation()
client_service = ClientServiceImpl(client_dao)
account_service = AccountServiceImpl(account_dao)


@app.route("/clients", methods=["POST"])
def create_client():
    body = request.json
    client = Client(body["clientId"], body["clientName"])
    client_service.create_client(client)
    return f"Created a new client. Your ID number is {client.client_id}.", 201


@app.route("/clients/<client_id>/accounts", methods=["POST"])
def create_account(client_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    body = request.json
    account = Account(body["accountId"], body["accountName"], body["accountType"], body["funds"],
                        body["refClientId"])
    account.c_id = client_id
    account_service.create_account(account)
    return f"Created a new account with ID {account.account_id}.", 201


@app.route("/clients", methods=["GET"])
def show_all_clients():
    clients = client_service.show_all_clients()
    json_clients = [c.as_json_dict() for c in clients]
    return jsonify(json_clients), 200


@app.route("/clients/<client_id>", methods=["GET"])
def show_client_by_id(client_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    client = client_service.show_client_by_id(int(client_id))
    return jsonify(client.as_json_dict()), 200


@app.route("/clients/<client_id>/accounts", methods=["GET"])
def show_client_accounts(client_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    less_amount = request.args.get("amountLessThan")
    greater_amount = request.args.get("amountGreaterThan")
    if less_amount is not None and greater_amount is not None:
        accounts = account_service.show_account_by_range(int(client_id), int(less_amount), int(greater_amount))
        json_accounts = [a.as_json_dict() for a in accounts]
        return jsonify(json_accounts)
    else:
        accounts = account_service.show_client_accounts(int(client_id))
        json_accounts = [a.as_json_dict() for a in accounts]
        return jsonify(json_accounts)


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
def show_account_by_id(client_id: int, account_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    try:
        account = account_service.show_account_by_id(client_id, account_id)
    except Exception:
        return f"Account {account_id} could not be found.", 404
    account = account_service.show_account_by_id(int(client_id), int(account_id))
    return jsonify(account.as_json_dict())


'''
@app.route("/clients/<client_id>/accounts?amountLessThan=<less_amount>&amountGreaterThan=<greater_amount>",
           methods=["GET"])
def show_account_by_range(client_id: str):
    less_amount=request.args.get("less_amount")
    greater_amount=request.args.get("greater_amount")
    accounts = account_service.show_account_by_range(int(client_id), int(less_amount), int(greater_amount))
    json_accounts = [a.as_json_dict() for a in accounts]
    return jsonify(json_accounts)
'''


@app.route("/clients/<client_id>", methods=["PUT"])
def update_client(client_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    body = request.json
    client = Client(body["clientId"], body["clientName"])
    client.client_id = int(client_id)
    client_service.update_client(client)
    return f"Updated info of client {client.client_id}."


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
def update_account(client_id: int, account_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    try:
        account = account_service.show_account_by_id(client_id, account_id)
    except Exception:
        return f"Account {account_id} could not be found.", 404
    body = request.json
    account = Account(body["accountId"], body["accountName"], body["accountType"], body["funds"], body["refClientId"])
    account.c_id = int(client_id)
    account.account_id = int(account_id)
    account_service.update_account(account)
    return f"Updated info of account {account.account_id}"


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
def add_remove_funds(client_id: int, account_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    try:
        account = account_service.show_account_by_id(client_id, account_id)
    except Exception:
        return f"Account {account_id} could not be found.", 404
    body = request.json
    try:
        change: int = body["withdraw"] * -1
        if account_service.add_remove_funds(client_id, account_id, change):
            return f"Successfully withdrew ${abs(change)} from account {account_id}."
        else:
            return f"Insufficient funds.", 422
    except KeyError:
        try:
            change: int = body["deposit"]
            account_service.add_remove_funds(client_id, account_id, change)
            return f"Successfully deposited ${change} into account {account_id}."
        except KeyError:
            return "Incorrect fund statement.", 422


@app.route("/clients/<client_id>/accounts/<account_id_1>/transfer/<account_id_2>", methods=["PATCH"])
def transfer_funds(client_id: int, account_id_1: int, account_id_2: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    try:
        account = account_service.show_account_by_id(client_id, account_id_1)
    except Exception:
        return f"Account {account_id_1} could not be found.", 404
    try:
        account = account_service.show_account_by_id(client_id, account_id_2)
    except Exception:
        return f"Account {account_id_2} could not be found.", 404
    body = request.json
    amount: int = body["amount"] * -1
    if account_service.transfer_funds(client_id, account_id_1, account_id_2, amount):
        return f"Successfully transferred ${abs(amount)} from account {account_id_1} to account {account_id_2}."
    else:
        return f"Insufficient funds.", 422


@app.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    test_list = account_service.show_client_accounts(client_id)
    if len(test_list) > 0:
        return "Please remove all accounts from this client first.", 422
    else:
        client_service.delete_client(int(client_id))
        return f"Client {client_id} has been removed.", 205


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
def delete_account(client_id: int, account_id: int):
    try:
        client = client_service.show_client_by_id(client_id)
    except Exception:
        return f"Client {client_id} could not be found.", 404
    try:
        account = account_service.show_account_by_id(client_id, account_id)
    except Exception:
        return f"Account {account_id} could not be found.", 404
    account_service.delete_account(client_id, account_id)
    return f"Account {account_id} from client {client_id} has been successfully removed.", 205


if __name__ == '__main__':
    app.run()
