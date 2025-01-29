from task import Task


class Todolist:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        
    def add_task(self, title: str, description : str = ""):
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        print(f"Tâche '{title}' ajoutée avec succès.")
    
    def remove_task(self, task_id : int):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        print(f"Tâche {task_id} supprimée avec succès.")
    
    def update_task(self, task_id : int, title : str, description : str = None):
        for task in self.tasks:
            if task.task_id == task_id:
                task.update(title, description)
                print("Tâche {task_id} modifiée avec succès.")
                return
        print(f"Tâche {task_id} non trouvée.")
        
    def list_tasks(self):
        if not self.tasks:
            print("Aucune tâche disponible.")
        for task in self.tasks:
            print(f"{task.task_id}: {task.title} - {task.description}")
    
    def from_dict(self, data : list):
        self.tasks = [Task.from_dict(item) for item in data]
        self.next_id = max([task.task_id for task in self.tasks], default =0) + 1
    
    def to_dict(self):
        return [task.to_dict() for task in self.tasks]
