import tkinter as tk
from tkinter import messagebox, scrolledtext

class GymMemberManagement:
    def __init__(self):
        self.members = {}

    def add_member(self, name, membership_type, personal_trainer):
        if name.strip() == '':
            return "Name cannot be empty."
        if name not in self.members:
            self.members[name] = (membership_type, personal_trainer)
            return f"Member '{name}' added with '{membership_type}' membership."
        else:
            return "Member already exists."

    def view_members(self):
        if self.members:
            return "\n".join([f"Name: {name}, Membership Type: {membership_type}, PersonalTrainer: {'Yes' if personal_trainer else 'No'}"
                              for name, (membership_type, personal_trainer) in self.members.items()])
        else:
            return "No members."

    def remove_member(self, name):
        if name in self.members:
            del self.members[name]
            return f"Member '{name}' removed successfully."
        else:
            return "Member not found."

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x450")  # Set window size
        self.master.title("Gym Member Management System")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self, text="Name:", font=("Arial", 15))
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self, font=("Arial", 15), width=20)
        self.name_entry.grid(row=0, column=1)

        self.membership_type_label = tk.Label(self, text="Membership Type (Annual/Half-Year):", font=("Arial", 15))
        self.membership_type_label.grid(row=1, column=0, sticky="w")
        self.membership_type_entry = tk.Entry(self, font=("Arial", 15), width=20)
        self.membership_type_entry.grid(row=1, column=1)

        self.personal_trainer_label = tk.Label(self, text="Personal Trainer (Yes/No):", font=("Arial", 15))
        self.personal_trainer_label.grid(row=2, column=0, sticky="w")
        self.personal_trainer_entry = tk.Entry(self, font=("Arial", 15), width=20)
        self.personal_trainer_entry.grid(row=2, column=1)

        self.add_member_button = tk.Button(self, text="Add Member", font=("Arial", 15), command=self.add_member)
        self.add_member_button.grid(row=3, column=0, pady=5, padx=0)

        self.view_members_button = tk.Button(self, text="View Members", font=("Arial", 15), command=self.view_members)
        self.view_members_button.grid(row=4, column=0, pady=5, padx=1)

        self.remove_member_button = tk.Button(self, text="Remove Member", font=("Arial", 15), command=self.remove_member)
        self.remove_member_button.grid(row=5, column=0, pady=5, padx=1)

        self.quit = tk.Button(self, text="QUIT", fg="red", font=("Arial", 15), command=self.master.destroy)
        self.quit.grid(row=8, column=0, columnspan=3, pady=5)

        self.result_frame = tk.Frame(self)
        self.result_frame.grid(row=7, column=0, columnspan=3)
        self.result_text = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD, width=40, height=10, font=("Arial", 15))
        self.result_text.pack()

        self.cost_label = tk.Label(self, text="Final Bill Amount:", font=("Arial", 15))
        self.cost_label.grid(row=6, column=0, sticky="w")
        self.final_cost_entry = tk.Entry(self, font=("Arial", 15), width=20)
        self.final_cost_entry.grid(row=6, column=1)
        self.final_cost_entry.config(state='readonly')

    def add_member(self):
        name = self.name_entry.get()
        membership_type = self.membership_type_entry.get()
        personal_trainer = True if self.personal_trainer_entry.get().lower() == 'yes' else False

        # Calculate final bill amount based on membership type
        if membership_type.lower() == 'annual':
            final_cost = 15000
        elif membership_type.lower() == 'half-year':
            final_cost = 8000
        else:
            final_cost = 0

        # Add personal trainer cost
        if personal_trainer:
            final_cost += 8000

        # Display final bill amount
        self.final_cost_entry.config(state='normal')
        self.final_cost_entry.delete(0, tk.END)
        self.final_cost_entry.insert(0, str(final_cost))
        self.final_cost_entry.config(state='readonly')

        result = gym_management.add_member(name, membership_type, personal_trainer)
        self.result_text.insert(tk.END, result + '\n')
        self.clear_entries()

    def view_members(self):
        result = gym_management.view_members()
        self.result_text.insert(tk.END, result + '\n')

    def remove_member(self):
        name = self.name_entry.get()
        result = gym_management.remove_member(name)
        self.result_text.insert(tk.END, result + '\n')
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.membership_type_entry.delete(0, tk.END)
        self.personal_trainer_entry.delete(0, tk.END)

gym_management = GymMemberManagement()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
