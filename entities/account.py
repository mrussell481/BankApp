class Account:

    def __init__(self, account_id: int, account_name: str, account_type: str, funds: int, c_id: int):
        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type
        self.funds = funds
        self.c_id = c_id

    def as_json_dict(self):
        return {
            "accountId": self.account_id,
            "accountName": self.account_name,
            "accountType": self.account_type,
            "funds": self.funds,
            "refCustomerId": self.c_id
        }
