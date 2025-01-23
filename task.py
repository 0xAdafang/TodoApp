class Task:
    def __init__(self, task_id : int, title : str, description : str = ""):
        self.task_id = task_id
        self.title = title
        self.description = description
    
    def update(self, title : str = None, description : str = None):
        if title:
            self.title = title
        if description:
            self.description = description
        
    def to_dict(self):
        return{"id" : self.task_id, "title" : self.title, "description" : self.description}
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["id"], data["title"], data["description"])