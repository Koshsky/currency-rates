import threading
import time
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

import requests
import xmltodict


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы валют")
        self.root.geometry("400x600")  # Увеличиваем высоту окна
        self.root.configure(bg="#f0f0f0")

        # Создаем стиль
        style = ttk.Style()
        style.configure("Currency.TLabel", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        style.configure("Rate.TLabel", font=("Arial", 16))
        style.configure("Update.TButton", font=("Arial", 12))
        style.configure("History.TButton", font=("Arial", 11))

        # Создаем фрейм для курсов валют
        self.rates_frame = ttk.Frame(root, padding="10")
        self.rates_frame.grid(row=0, column=0, sticky="nsew")

        # Заголовок
        ttk.Label(
            self.rates_frame, text="Курсы валют ЦБ РФ", style="Header.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Метки для USD
        ttk.Label(
            self.rates_frame, text="Доллар США (USD):", style="Currency.TLabel"
        ).grid(row=1, column=0, pady=5, sticky="w")

        self.usd_rate = ttk.Label(
            self.rates_frame, text="Загрузка...", style="Rate.TLabel"
        )
        self.usd_rate.grid(row=1, column=1, pady=5)

        # Метки для EUR
        ttk.Label(self.rates_frame, text="Евро (EUR):", style="Currency.TLabel").grid(
            row=2, column=0, pady=5, sticky="w"
        )

        self.eur_rate = ttk.Label(
            self.rates_frame, text="Загрузка...", style="Rate.TLabel"
        )
        self.eur_rate.grid(row=2, column=1, pady=5)

        # Время последнего обновления и дата курса
        self.update_time = ttk.Label(
            self.rates_frame, text="Последнее обновление: -", style="Currency.TLabel"
        )
        self.update_time.grid(row=3, column=0, columnspan=2, pady=5)

        self.rate_date = ttk.Label(
            self.rates_frame, text="Дата курса: сегодня", style="Currency.TLabel"
        )
        self.rate_date.grid(row=4, column=0, columnspan=2, pady=5)

        # Кнопки управления
        buttons_frame = ttk.Frame(self.rates_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10)

        # Кнопка обновления текущего курса
        self.update_button = ttk.Button(
            buttons_frame,
            text="Текущий курс",
            style="Update.TButton",
            command=lambda: self.update_rates(),
            width=15,
        )
        self.update_button.grid(row=0, column=0, padx=5)

        # Кнопка для вчерашнего курса
        ttk.Button(
            buttons_frame,
            text="Вчера",
            style="History.TButton",
            command=lambda: self.update_rates(days_ago=1),
            width=15,
        ).grid(row=0, column=1, padx=5)

        # Кнопка для курса неделю назад
        ttk.Button(
            buttons_frame,
            text="Неделю назад",
            style="History.TButton",
            command=lambda: self.update_rates(days_ago=7),
            width=15,
        ).grid(row=0, column=2, padx=5)

        # Калькулятор конвертации
        ttk.Label(
            self.rates_frame, text="Калькулятор конвертации", style="Header.TLabel"
        ).grid(row=6, column=0, columnspan=2, pady=10)

        # Поле ввода суммы
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(
            self.rates_frame, textvariable=self.amount_var, font=("Arial", 12)
        )
        self.amount_entry.grid(row=7, column=0, columnspan=2, pady=5)

        # Выбор валюты
        self.currency_var = tk.StringVar(value="USD")
        currency_frame = ttk.Frame(self.rates_frame)
        currency_frame.grid(row=8, column=0, columnspan=2, pady=5)

        ttk.Radiobutton(
            currency_frame, text="USD → RUB", variable=self.currency_var, value="USD"
        ).grid(row=0, column=0, padx=5)

        ttk.Radiobutton(
            currency_frame, text="EUR → RUB", variable=self.currency_var, value="EUR"
        ).grid(row=0, column=1, padx=5)

        # Кнопка конвертации
        ttk.Button(
            self.rates_frame, text="Конвертировать", command=self.convert_currency
        ).grid(row=9, column=0, columnspan=2, pady=5)

        # Результат конвертации
        self.result_label = ttk.Label(self.rates_frame, text="", style="Rate.TLabel")
        self.result_label.grid(row=10, column=0, columnspan=2, pady=5)

        # Настройка grid
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Сохраняем курсы
        self.rates = {"USD": 0, "EUR": 0}

        # Запускаем первое обновление
        self.update_rates()

        # Запускаем автоматическое обновление каждый час
        self.start_auto_update()

    def get_currency_rates(self, date=None):
        try:
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
            if date:
                url += f"?date_req={date.strftime('%d/%m/%Y')}"

            response = requests.get(url)
            data = xmltodict.parse(response.content)

            for valute in data["ValCurs"]["Valute"]:
                if valute["CharCode"] == "USD":
                    self.rates["USD"] = float(valute["Value"].replace(",", "."))
                elif valute["CharCode"] == "EUR":
                    self.rates["EUR"] = float(valute["Value"].replace(",", "."))

            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить курсы валют: {str(e)}")
            return False

    def update_rates(self, days_ago=0):
        self.update_button.configure(state="disabled")
        date = datetime.now() - timedelta(days=days_ago) if days_ago > 0 else None

        if self.get_currency_rates(date):
            self.usd_rate.configure(text=f"{self.rates['USD']:.2f} ₽")
            self.eur_rate.configure(text=f"{self.rates['EUR']:.2f} ₽")
            current_time = datetime.now().strftime("%H:%M:%S")
            self.update_time.configure(text=f"Последнее обновление: {current_time}")

            if days_ago == 0:
                date_text = "сегодня"
            elif days_ago == 1:
                date_text = "вчера"
            elif days_ago == 7:
                date_text = "неделю назад"
            else:
                date_text = (datetime.now() - timedelta(days=days_ago)).strftime(
                    "%d.%m.%Y"
                )

            self.rate_date.configure(text=f"Дата курса: {date_text}")

        self.update_button.configure(state="normal")

    def convert_currency(self):
        try:
            amount = float(self.amount_var.get())
            currency = self.currency_var.get()
            result = amount * self.rates[currency]
            self.result_label.configure(
                text=f"{amount:.2f} {currency} = {result:.2f} ₽"
            )
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")

    def start_auto_update(self):
        def auto_update():
            while True:
                time.sleep(3600)  # Обновление каждый час
                self.root.after(0, lambda: self.update_rates(days_ago=0))

        thread = threading.Thread(target=auto_update, daemon=True)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.geometry("")
    root.mainloop()
