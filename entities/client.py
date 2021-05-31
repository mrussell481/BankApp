class Client:

    def __init__(self, client_id: int, client_name: str):
        self.client_id = client_id
        self.client_name = client_name

    def as_json_dict(self):
        return {
            "clientId": self.client_id,
            "clientName": self.client_name
        }
