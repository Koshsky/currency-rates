import tkinter as tk
from tkinter import ttk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x400")
        self.root.configure(bg="#f0f0f0")

        # Переменная для хранения текущего выражения
        self.current = ""

        # Создаем поле ввода
        self.entry = ttk.Entry(root, justify=tk.RIGHT, font=("Arial", 20))
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Создаем стиль для кнопок
        style = ttk.Style()
        style.configure("Calculator.TButton", font=("Arial", 14))

        # Кнопки калькулятора
        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
        ]

        # Размещаем кнопки в сетке
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ttk.Button(root, text=button, style="Calculator.TButton", command=cmd).grid(
                row=row, column=col, padx=2, pady=2, sticky="nsew"
            )
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Добавляем кнопку очистки
        ttk.Button(root, text="C", style="Calculator.TButton", command=self.clear).grid(
            row=5, column=0, columnspan=4, padx=2, pady=2, sticky="nsew"
        )

        # Настраиваем веса строк и столбцов для респонсивности
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def click(self, char):
        if char == "=":
            try:
                result = eval(self.current)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.current = str(result)
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, e)
                self.current = ""
        else:
            self.current += char
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current)

    def clear(self):
        self.current = ""
        self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
