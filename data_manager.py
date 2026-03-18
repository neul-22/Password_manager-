import json
import os

class DataManager:
    def __init__(self, accounts_file: str = "accounts.json", 
                                                            users_file: str = "users.json"):
        self.accounts_file = accounts_file
        self.users_file = users_file
        
        self._init_file(self.accounts_file, {"accounts": []})
        self._init_file(self.users_file, {"users": []})

    def _init_file(self, filepath: str, default_data: dict):
        if not os.path.exists(filepath):
            self._write_json(filepath, default_data)

    def _read_json(self, filepath: str) -> dict:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _write_json_(self, filepath: str, data: dict):
         with open(filepath, "w", encoding="utf-8") as f:
             json.dump(data, f, indent=2, ensure_ascii=False)

    
    def get_all_account(self) -> list[dict]:
        return self._read_json(self.accounts_file).get("accounts", [])
    def save_all_account(self, account: list[dict]):
        self._write_json_(self.accounts_file, {"accounts": account})
    def add_account(self, account: dict):
        accounts = self.get_all_account()
        accounts.append(account)
        self.save_all_account(accounts)
    def delete_account(self, index: int):
        accounts = self.get_all_account()
        accounts.pop(index)
        self.save_all_account(accounts)

    def get_all_users(self) -> list[dict]:
        return self._read_json(self.users_file).get("users", [])
    def save_all_users(self, users: list[dict]):
        self._write_json_(self.users_file, {"users": users})
    def add_user(self, user: dict):
        users = self.get_all_users()
        users.append(user)
        self.get_all_users(users) 
    def delete_user(self, username: str):
        users = self.get_all_users()
        users = [u for u in users if u["username"] != username]
        self.save_all_users(users)
                
                           
        
                                                      
        

        