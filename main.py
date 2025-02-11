import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from todolist import Todolist
from storage import Storage
4444
class TodoApp:
    
    def __init__(self, root, file_path):
        self.file_path = file_path
        self.todo_list = Storage.load_from_file(file_path)
        
        root.title("To-Do List App")
        root.geometry("600x600")
        
        main_frame = ttk.Frame(root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurer le conteneur principal pour s'étendre avec la fenêtre
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Liste des tâches
        self.task_listbox = ttk.Treeview(
            main_frame,
            columns=("ID", "Title", "Description"),
            show="headings",
            height=15
        )
        self.task_listbox.heading("ID", text="ID")
        self.task_listbox.heading("Title", text="Titre")
        self.task_listbox.heading("Description", text="Description")

        # Cacher la colonne "ID"
        self.task_listbox.column("ID", anchor=CENTER, width=50, stretch=False)
        self.task_listbox.column("Title", anchor=CENTER, width=150)
        self.task_listbox.column("Description", anchor=CENTER, width=300)

        self.task_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=10, padx=10)
        
        # Configurer la liste pour s'étendre avec la fenêtre
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Champs d'entrée
        entry_frame = ttk.Frame(main_frame)
        entry_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.title_entry = ttk.Entry(entry_frame, width=30, bootstyle="primary")
        self.title_entry.grid(row=0, column=0, padx=10, pady=5)

        self.desc_entry = ttk.Entry(entry_frame, width=30, bootstyle="primary")
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.add_placeholder(self.title_entry, "Titre")
        self.add_placeholder(self.desc_entry, "Description")
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Ajouter", bootstyle=SUCCESS, command=self.add_task).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Supprimer", bootstyle=DANGER, command=self.remove_task).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Modifier", bootstyle=INFO, command=self.update_task).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Sauvegarder", bootstyle=SECONDARY, command=self.save_tasks).grid(row=0, column=3, padx=5, pady=5)
        
        # Menu des thèmes
        self.theme_menu = ttk.Menubutton(main_frame, text="Thème", bootstyle="primary")
        theme_menu = ttk.Menu(self.theme_menu, tearoff=False)
        self.theme_menu["menu"] = theme_menu
        
        for theme in root.style.theme_names():
            theme_menu.add_command(
                label=theme,
                command=lambda t=theme: root.style.theme_use(t)        
            )
        
        self.theme_menu.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.refresh_task_list()
    
    def add_placeholder(self, entry, placeholder):
   
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.configure(bootstyle="primary")
        
        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.configure(bootstyle="secondary")

        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
     
    def refresh_task_list(self):
       
        for item in self.task_listbox.get_children():
            self.task_listbox.delete(item)
        for task in self.todo_list.tasks:
            self.task_listbox.insert("", "end", values=(task.task_id, task.title, task.description))
            
    def add_task(self):
       
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        if title:
            self.todo_list.add_task(title, description)
            self.refresh_task_list()
            messagebox.showinfo("Succès", "Tâche ajoutée avec succès.")
        else:
            messagebox.showerror("Erreur", "Le titre de la tâche ne peut pas être vide.")
    
    def remove_task(self):
       
        selected = self.task_listbox.selection()
        if selected:
            task_id = int(self.task_listbox.item(selected[0])["values"][0])  # Récupérer l'ID
            self.todo_list.remove_task(task_id)
            self.refresh_task_list()
            messagebox.showinfo("Succès", f"Tâche {task_id} supprimée avec succès.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une tâche à supprimer.")

    def update_task(self):
       
        selected = self.task_listbox.selection()
        if selected:
            task_id = int(self.task_listbox.item(selected[0])["values"][0])  # Récupérer l'ID
            title = self.title_entry.get().strip()
            description = self.desc_entry.get().strip()
            if title:
                self.todo_list.update_task(task_id, title, description)
                self.refresh_task_list()
                messagebox.showinfo("Succès", f"Tâche {task_id} mise à jour avec succès.")
            else:
                messagebox.showerror("Erreur", "Le titre de la tâche ne peut pas être vide.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une tâche à mettre à jour.")
    def save_tasks(self):
        
        Storage.save_to_file(self.file_path, self.todo_list)
        messagebox.showinfo("Succès", "Tâches sauvegardées avec succès.")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = TodoApp(root, "data/tasks.json")
    root.mainloop()
