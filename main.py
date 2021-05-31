from flask import Flask, request, jsonify

import services.client_service_impl
from daos.client_dao_impl import ClientDaoImplementation
from daos.account_dao_impl import AccountDaoImplementation
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
    body = request.json
    account = Account(body["accountId"], body["accountName"], body["accountType"], body["funds"], body["refClientId"])
    account.c_id = client_id
    account_service.create_account(account)
    return f"Created a new account with ID {account.account_id}.", 201


@app.route("/clients", methods=["GET"])
def show_all_clients():
    clients = client_service.show_all_clients()
    json_clients = [c.as_json_dict() for c in clients]
    return jsonify(json_clients)


@app.route("/clients/<client_id>", methods=["GET"])
def show_client_by_id(client_id: str):
    client = client_service.show_client_by_id(int(client_id))
    return jsonify(client.as_json_dict())


@app.route("/clients/<client_id>/accounts", methods=["GET"])
def show_client_accounts(client_id: str):
    accounts = account_service.show_client_accounts(int(client_id))
    json_accounts = [a.as_json_dict() for a in accounts]
    return jsonify(json_accounts)


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
def show_account_by_id(client_id: str, account_id: str):
    account = account_service.show_account_by_id(int(client_id), int(account_id))
    return jsonify(account.as_json_dict())


@app.route("/clients/<client_id>/accounts?amountLessThan=<less_amount>&amountGreaterThan=<greater_amount>",
           methods=["GET"])
def show_account_by_range(client_id: str, less_amount: str, greater_amount: str):
    accounts = account_service.show_account_by_range(int(client_id), int(less_amount), int(greater_amount))
    json_accounts = [a.as_json_dict() for a in accounts]
    return jsonify(json_accounts)


@app.route("/clients/<client_id>", methods=["PUT"])
def update_client(client_id: str):
    body = request.json
    client = Client(body["clientId"], body["clientName"])
    client.client_id = int(client_id)
    client_service.update_client(client)
    return f"Updated info of client {client.client_id}"


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
def update_account(client_id: str, account_id: str):
    body = request.json
    account = Account(body["accountId"], body["accountName"], body["accountType"], body["funds"], body["refClientId"])
    account.c_id = int(client_id)
    account.account_id = int(account_id)
    account_service.update_account(account)
    return f"Updated info of account {account.account_id}"


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
def add_remove_funds(client_id: str, account_id: str):
    pass


@app.route("/clients/<client_id>/accounts/<account_id_1>/transfer/<account_id_2>", methods=["PATCH"])
def transfer_funds(client_id: str, account_id_1: str, account_id_2: str):
    pass


@app.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id: str):
    pass


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
def delete_account(client_id: str, account_id: str):
    pass


if __name__ == '__main__':
    app.run()
