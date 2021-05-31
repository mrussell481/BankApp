from typing import List
from daos.client_dao import ClientDAO
from entities.client import Client
from utils.connection_util import connection


class ClientDaoImplementation(ClientDAO):

    def create_client(self, client: Client) -> Client:
        cursor = connection.cursor()
        sql = """insert into client (client_name) values ('{}') returning client_id""".format(client.client_name)
        cursor.execute(sql)
        connection.commit()
        c_id = cursor.fetchone()[0]
        client.client_id = c_id
        return client

    def show_all_clients(self) -> List[Client]:
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        client_list=[]
        for x in records:
            client_list.append(Client(*x))
        return client_list

    def show_client_by_id(self, client_id: int) -> Client:
        sql = """select * from client where client_id = {}""".format(client_id)
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchone()
        client = Client(*record)
        return client

    def update_client(self, client: Client) -> Client:
        cursor = connection.cursor()
        sql = """update client set client_name = '{}' where client_id = {};""".format(client.client_name, client.client_id)
        cursor.execute(sql)
        connection.commit()
        print("Yello World")
        return client

    def delete_client(self, client_id: int) -> bool:
        pass
