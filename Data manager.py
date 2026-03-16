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
        with open(filepath, "r" encoding="utf-8") as f:
        

        