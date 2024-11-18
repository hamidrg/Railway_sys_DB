import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


db_config = {
    'user': 'root',
    'password': 'hamidrg@@2008',
    'host': 'localhost',
    'port': '3306',
    'database': 'railway_sys'
}


def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


def execute_query(query, params=()):
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        else:
            conn.commit()
            messagebox.showinfo("Success", "Operation successful")
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def show_table_data(cols, table_name, condition):
    if condition == "-" or condition == "":
        query = f"SELECT {', '.join(cols)} FROM {table_name}"
    else:
        query = f"SELECT {', '.join(cols)} FROM {table_name} WHERE {condition}"
    rows = execute_query(query)
    if rows:
        for row in rows:
            tree.insert("", tk.END, values=row)


root = tk.Tk()
root.title("Railway Management System")


frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


tree = ttk.Treeview(frame)
columns = ("1", "2", "3", "4", "5", "6")
tree = ttk.Treeview(frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10)


def load_employee_data():
    emp_columns = ("EmpNo", "EmpFName", "EmpLName", "TrainNo", " ", " ")
    columns = ("1", "2", "3", "4", "5", "6")
    for col in columns:
        tree.heading(col, text=emp_columns[int(col)-1])
    tree.delete(*tree.get_children())
    show_table_data("*", "employee", "-")


def load_passenger_data():
    pass_columns = ("NCode", "FName", "LName", "Age", "Gender", " ")
    columns = ("1", "2", "3", "4", "5", "6")
    for col in columns:
        tree.heading(col, text=pass_columns[int(col)-1])
    tree.delete(*tree.get_children())
    show_table_data("*", "passenger", "-")


def load_ticket_data():
    ticket_columns = ("TicketID", "SeatNo", "Cost",
                      "ResDate", "NCode", "TrainNo")
    columns = ("1", "2", "3", "4", "5", "6")
    for col in columns:
        tree.heading(col, text=ticket_columns[int(col)-1])
    tree.delete(*tree.get_children())
    show_table_data("*", "ticket", "-")


def load_time_table_data():
    time_columns = ("TrainNo", "From_", "DepartureTime",
                    "To_", "ArrivalTime", " ")
    columns = ("1", "2", "3", "4", "5", "6")
    for col in columns:
        tree.heading(col, text=time_columns[int(col)-1])
    tree.delete(*tree.get_children())
    show_table_data("*", "time_table", "-")


def load_train_data():
    train_columns = ("TrainNo", "TName", "TCapacity", "TType", " ", " ")
    columns = ("1", "2", "3", "4", "5", "6")
    for col in columns:
        tree.heading(col, text=train_columns[int(col)-1])
    tree.delete(*tree.get_children())
    show_table_data("*", "train", "-")


def load_data():
    table_name = table_clicked.get()
    columns = columns_entry.get().split(',')
    condition = condition_entry.get()
    for col in range(0, len(columns)):
        tree.heading(col+1, text=columns[col])
    for i in range(len(columns)+1, 7):
        tree.heading(i, text=" ")
    tree.delete(*tree.get_children())
    show_table_data(columns, table_name, condition)


employee_button = ttk.Button(
    button_frame, text="Load Employee Data", command=load_employee_data)
employee_button.grid(row=0, column=0, padx=5, pady=5)

passenger_button = ttk.Button(
    button_frame, text="Load Passenger Data", command=load_passenger_data)
passenger_button.grid(row=0, column=1, padx=5, pady=5)

ticket_button = ttk.Button(
    button_frame, text="Load Ticket Data", command=load_ticket_data)
ticket_button.grid(row=0, column=2, padx=5, pady=5)

time_table_button = ttk.Button(
    button_frame, text="Load Time Table Data", command=load_time_table_data)
time_table_button.grid(row=0, column=3, padx=5, pady=5)

train_button = ttk.Button(
    button_frame, text="Load Train Data", command=load_train_data)
train_button.grid(row=0, column=4, padx=5, pady=5)


def insert_data():
    table_name = table_clicked.get()
    columns = columns_entry.get().split(',')
    values = values_entry.get().split(',')
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
    execute_query(query, values)


def update_data():
    table_name = table_clicked.get()
    set_clause = set_clause_entry.get()
    condition = condition_entry.get()
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
    execute_query(query)


def delete_data():
    table_name = table_clicked.get()
    condition = condition_entry.get()
    query = f"DELETE FROM {table_name} WHERE {condition}"
    execute_query(query)


crud_frame = ttk.Frame(root)
crud_frame.pack(padx=10, pady=10)

tables = ["passenger", "passenger", "ticket",
          "train", "time_table", "employee"]
table_clicked = tk.StringVar()
table_name_label = ttk.Label(crud_frame, text="Table Name:")
table_name_label.grid(row=0, column=0, padx=5, pady=5)
table_name_entry = ttk.OptionMenu(crud_frame, table_clicked, *tables)
table_name_entry.grid(row=0, column=1, padx=5, pady=5)

columns_label = ttk.Label(crud_frame, text="Columns (comma separated):")
columns_label.grid(row=1, column=0, padx=5, pady=5)
columns_entry = ttk.Entry(crud_frame)
columns_entry.grid(row=1, column=1, padx=5, pady=5)

values_label = ttk.Label(crud_frame, text="Values (comma separated):")
values_label.grid(row=2, column=0, padx=5, pady=5)
values_entry = ttk.Entry(crud_frame)
values_entry.grid(row=2, column=1, padx=5, pady=5)

set_clause_label = ttk.Label(crud_frame, text="Set Clause (for update):")
set_clause_label.grid(row=3, column=0, padx=5, pady=5)
set_clause_entry = ttk.Entry(crud_frame)
set_clause_entry.grid(row=3, column=1, padx=5, pady=5)

condition_label = ttk.Label(crud_frame, text="Condition (for update/delete):")
condition_label.grid(row=4, column=0, padx=5, pady=5)
condition_entry = ttk.Entry(crud_frame)
condition_entry.grid(row=4, column=1, padx=5, pady=5)

show_button = ttk.Button(crud_frame, text="Show Data", command=load_data)
show_button.grid(row=5, column=0, padx=5, pady=5)

insert_button = ttk.Button(crud_frame, text="Insert Data", command=insert_data)
insert_button.grid(row=5, column=1, padx=5, pady=5)

update_button = ttk.Button(crud_frame, text="Update Data", command=update_data)
update_button.grid(row=5, column=2, padx=5, pady=5)

delete_button = ttk.Button(crud_frame, text="Delete Data", command=delete_data)
delete_button.grid(row=5, column=3, padx=5, pady=5)

root.mainloop()
