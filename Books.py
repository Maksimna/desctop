from tkinter import messagebox
import pymysql
import tkinter as tk
from tkinter import Tk, ttk
import time

class Main():
    def SQL_connect(self):
        self.Con = pymysql.Connect(
            host='localhost',
            user='root',
            password='4444',
            database='mydb',
            port=3306
        )
        print(f'Успешно подключено к базе данных MySQL')
        
    def SQL_select(self):
        self.Cur = self.Con.cursor()
        self.Cur.execute('SELECT id, title, price, author_name, shelves FROM books WHERE id>0')
        self.result = self.Cur.fetchall()
        print(self.result)
                
    def main_page(self):
        self.SQL_connect()
        self.SQL_select()
        
        self.main = Tk()
        self.main.geometry('900x600')
        self.main.resizable(0, 0)
        
        self.tree = ttk.Treeview(self.main, height=20)
        self.tree["columns"] = ("id", "title", "price", "author_name", "shelves")
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.CENTER, width=80)
        self.tree.column("title", anchor=tk.W, width=300)
        self.tree.column("price", anchor=tk.CENTER, width=100)
        self.tree.column("author_name", anchor=tk.CENTER, width=300)
        self.tree.column("shelves", anchor=tk.CENTER, width=80)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("id", text="ID", anchor=tk.CENTER)
        self.tree.heading("title", text="Заголовок", anchor=tk.W)
        self.tree.heading("price", text="Цена", anchor=tk.CENTER)
        self.tree.heading("author_name", text="Автор", anchor=tk.CENTER)
        self.tree.heading("shelves", text="Полка", anchor=tk.W)
        
        self.tree.pack(pady=20)
        self.tree_data()
        
        self.button = ttk.Button(text='Записать', command=self.validation_page)
        self.button.place(x=50, y=500)
        self.button = ttk.Button(text='Удалить', command=self.validation_page_on_delite)
        self.button.place(x=50, y=550)
        
        self.main.mainloop()
        
    def book_page(self):
        self.book = Tk()
        self.book.geometry('400x450')
        self.book.resizable(0,0)
        
        title_label = ttk.Label(self.book, text="Заголовок:")
        title_label.pack(pady=5)
        self.title_entry = ttk.Entry(self.book)
        self.title_entry.pack(pady=5)

        price_label = ttk.Label(self.book, text="Цена:")
        price_label.pack(pady=5)
        self.price_entry = ttk.Entry(self.book)
        self.price_entry.pack(pady=5)
        
        author_label = ttk.Label(self.book, text="Автор:")
        author_label.pack(pady=5)
        self.author_entry = ttk.Entry(self.book)
        self.author_entry.pack(pady=5)
        
        shelves_label = ttk.Label(self.book, text="Полка:")
        shelves_label.pack(pady=5)
        self.shelves_entry = ttk.Entry(self.book)
        self.shelves_entry.pack(pady=5)
        
        self.add_button = ttk.Button(self.book, text='Добавить', command=self.add_record)
        self.add_button.pack(pady=21)
        
        self.book.mainloop()    
    
    def validation_page(self):
        self.Cur.execute('SELECT id, status, name, surname FROM staff WHERE id>0')
        self.keys = self.Cur.fetchall()
        print(self.keys)
                
        self.validation = Tk()
        self.validation.geometry('400x120')
        self.validation.resizable(0,0)
        
        label = ttk.Label(self.validation, text="Введите идентификатор сотрудника для проведения операции:")
        label.pack(pady=5)
        self.id_entry = ttk.Entry(self.validation, width=25)
        self.id_entry.pack(pady=5)
        
        self.add_button = ttk.Button(self.validation, text='Провести операцию', command=self.try_validation)
        self.add_button.place(x=140, y=80)
        
        self.validation.mainloop()
        
    def validation_page_on_delite(self):
        self.Cur.execute('SELECT id, status, name, surname FROM staff WHERE id>0')
        self.keys = self.Cur.fetchall()
        print(self.keys)
                
        self.validation = Tk()
        self.validation.geometry('400x120')
        self.validation.resizable(0,0)
        
        label = ttk.Label(self.validation, text="Введите идентификатор сотрудника для проведения операции:")
        label.pack(pady=5)
        self.id_entry = ttk.Entry(self.validation, width=25)
        self.id_entry.pack(pady=5)
        
        self.add_button = ttk.Button(self.validation, text='Провести операцию', command=self.try_validation_on_delite)
        self.add_button.place(x=140, y=80)
        
        self.validation.mainloop()
        
    def try_validation(self):
        self.auth = 0
        entry_search = int(self.id_entry.get())
        print(entry_search)

        user_search = list(filter(
            lambda user: user[0] == entry_search,
            self.keys
        ))
        for u in user_search:
            u = u[0]
        if u == entry_search:
            self.validation.destroy()
            
            self.auth = 1
            
            messagebox.showinfo("Внимание", f"Доступ разрешен")
            self.book_page()
            
        
        if not user_search:
            return print('Сотрудник не найден!')
        
    def try_validation_on_delite(self):
        self.auth = 0
        entry_search = int(self.id_entry.get())

        user_search = list(filter(
            lambda user: user[0] == entry_search,
            self.keys
        ))
        for u in user_search:
            u = u[0]
        if u == entry_search:
            self.validation.destroy()
            
            self.auth = 1
            
            self.delete_record()
        
        if not user_search:
            return print('Сотрудник не найден!')
        
    def tree_data(self):
        for r in self.result:
            self.tree.insert("", "end", values=r)
            
    def clear_data(self):
        self.tree.delete(*self.tree.get_children())
            
    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись для удаления")
            return
        ids_to_delete = [self.tree.item(item, "values")[0] for item in selected_item]
        
        string = ",".join(ids_to_delete)
        print(string)
            
        delete_query = f"DELETE FROM books WHERE id IN ({string})"
        print(delete_query)
        self.Cur.execute(delete_query)
        self.Con.commit()

        # Удаление записи из Treeview
        # self.tree.delete(selected_item)
        self.clear_data()
        self.SQL_select()
        self.tree_data()
        messagebox.showinfo("Успех", "Запись успешно удалена")
        
    def add_record(self):
        title = self.title_entry.get()
        price = self.price_entry.get()
        author = self.author_entry.get()
        shelve = self.shelves_entry.get()

        if not title or not price or not author or not shelve:
            messagebox.showwarning("Предупреждение", "Пропущены поля")
            return

        try:
            price = int(price)
            print(price)
        except ValueError:
            messagebox.showwarning("Предупреждение", "Цена должна быть числом")
            return

        # Добавление записи в базу данных
        p = f"INSERT INTO books (title, price, author_name, shelves) VALUES ('{title}', '{price}', '{author}', '{shelve}')"
        print(p)
        self.Cur.execute(p)
        self.Con.commit()

        # Обновление Treeview
        self.clear_data()
        self.SQL_select()
        self.tree_data()
        
        self.book.destroy()

        messagebox.showinfo("Успех", "Запись успешно добавлена")
            
if __name__ == "__main__":
    App = Main()
    App.main_page()