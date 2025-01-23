import json
import os
from todolist import Todolist

class Storage:
    @staticmethod
    def save_to_file(file_path : str, todo_list: Todolist):
        with open(file_path, "w") as file:
            json.dump(todo_list.to_dict(), file, indent=4)
        print(f"Liste sauvegardée dans {file_path}.")
        

    @staticmethod
    def load_from_file(file_path : str) -> Todolist:
        
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f"Fichier {file_path} vide ou inexistant, création d'une nouvelle liste.")
            return Todolist()
        
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                todo_list = Todolist()
                todo_list.from_dict(data)
                print(f"Liste chargée depuis {file_path}.")
                return todo_list
        except FileNotFoundError:
            print(f"Fichier {file_path} introuvable, création d'une nouvelle liste.")
            return Todolist()
        