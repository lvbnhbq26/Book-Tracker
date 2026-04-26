import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

DATA_FILE = "books.json"

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")

        self.books = self.load_data()
        self.filtered_books = list(self.books) # Список для отображения после фильтрации

        # --- Input Frame ---
        input_frame = ttk.LabelFrame(root, text="Добавление книги", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.author_entry = ttk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.genre_entry = ttk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Страниц:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.pages_entry = ttk.Entry(input_frame, width=15)
        self.pages_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        add_button = ttk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Filter Frame ---
        filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.filter_genre_entry = ttk.Entry(filter_frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(filter_frame, text="Страниц >:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.filter_pages_entry = ttk.Entry(filter_frame, width=10)
        self.filter_pages_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)

        filter_button = ttk.Button(filter_frame, text="Применить", command=self.apply_filters)
        filter_button.grid(row=2, column=0, columnspan=2, pady=10)

        clear_filter_button = ttk.Button(filter_frame, text="Сбросить", command=self.clear_filters)
        clear_filter_button.grid(row=3, column=0, columnspan=2, pady=5)

        # --- Books Table ---
        table_frame = ttk.Frame(root, padding="10")
        table_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")

        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=120)
        self.tree.column("pages", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.update_treeview()

        # --- Menu ---
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=filemenu)
        filemenu.add_command(label="Сохранить", command=self.save_data)
        filemenu.add_command(label="Загрузить", command=self.load_data_and_update_tree)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=root.quit)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # Обработка закрытия окна

    def load_data(self):
        """Загружает данные книг из JSON файла."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_data(self):
        """Сохраняет текущие данные книг в JSON файл."""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены.")
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные.")

    def add_book(self):
        """Добавляет книгу на основе введенных данных."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        # Валидация ввода
        if not all([title, author, genre, pages_str]):
            messagebox.showerror("Ошибка ввода", "Все поля должны быть заполнены.")
            return

        try:
            pages = int(pages_str)
            if pages <= 0:
                messagebox.showerror("Ошибка ввода", "Количество страниц должно быть положительным числом.")
                return
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Поле 'Количество страниц' должно содержать число.")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }

        self.books.append(book)
        self.filtered_books.append(book) # Добавляем и в отфильтрованный список
        self.update_treeview()
        self.clear_input_fields()
        messagebox.showinfo("Успех", "Книга успешно добавлена!")

    def clear_input_fields(self):
        """Очищает поля ввода."""
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def update_treeview(self, books_to_display=None):
        """Обновляет данные в таблице Treeview."""
        if books_to_display is None:
            books_to_display = self.filtered_books

        # Очистка текущих данных
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавление новых данных
        for book in books_to_display:
            self.tree.insert("", tk.END, values=(
                book.get("title", ""),
                book.get("author", ""),
                book.get("genre", ""),
                book.get("pages", "")
            ))

    def apply_filters(self):
        """Применяет фильтры к списку книг."""
        filter_genre = self.filter_genre_entry.get().strip().lower()
        filter_pages_str = self.filter_pages_entry.get().strip()
        filter_pages = None

        if filter_pages_str:
            try:
                filter_pages = int(filter_pages_str)
                if filter_pages <= 0:
                    messagebox.showwarning("Предупреждение", "Фильтр 'Страниц >' должен быть положительным числом.")
                    filter_pages = None
            except ValueError:
                messagebox.showwarning("Предупреждение", "Пожалуйста, введите числовое значение для фильтра 'Страниц >'.")

        self.filtered_books = []
        for book in self.books:
            genre_match = not filter_genre or filter_genre in book.get("genre", "").lower()
            pages_match = True
            if filter_pages is not None:
                pages_match = book.get("pages", 0) > filter_pages

            if genre_match and pages_match:
                self.filtered_books.append(book)

        self.update_treeview()

    def clear_filters(self):
        """Сбрасывает все примененные фильтры."""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.filtered_books = list(self.books) # Возвращаем полный список
        self.update_treeview()

    def load_data_and_update_tree(self):
        """Загружает данные и обновляет таблицу."""
        self.books = self.load_data()
        self.filtered_books = list(self.books)
        self.update_treeview()
        if not self.books:
            messagebox.showinfo("Информация", "База данных книг пуста.")

    def on_closing(self):
        """Обрабатвает закрытие окна, предлагая сохранить данные."""
        if messagebox.askokcancel("Выход", "Хотите сохранить изменения перед выходом?"):
            self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
