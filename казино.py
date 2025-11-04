import tkinter as tk
import random
import time
from threading import Thread

# --- НАСТРОЙКИ СИМВОЛОВ ---
symbols = {
    "🍒": {"value": 15, "weight": 5, "highlight": "white"},
    "🍉": {"value": 5, "weight": 5, "highlight": "white"},
    "🍇": {"value": 10, "weight": 5, "highlight": "white"},
    "🍊": {"value": 10, "weight": 5, "highlight": "white"},
    "7️⃣": {"value": 25, "weight": 4, "highlight": "white"},
    "💎": {"value": 30, "weight": 1, "highlight": "purple"},   # алмаз
    "💚": {"value": 50, "weight": 1.5, "highlight": "gold"},    # изумруд
    "🔴": {"value": 200, "weight": 1, "highlight": "rainbow"}   # рубин
}

base_bet = 50

rainbow_colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]


class SlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Минималистичный слот")
        self.root.configure(bg="black")
        self.root.geometry("900x550")

        self.coins = 100
        self.bet = base_bet
        self.is_spinning = False

        # Заголовок
        tk.Label(root, text="🎰 Минималистичный слот 🎰", font=("Arial", 28, "bold"),
                 fg="gold", bg="black").pack(pady=10)

        # Баланс
        self.balance_label = tk.Label(root, text=f"Монеты: {self.coins}",
                                      font=("Arial", 18, "bold"), fg="white", bg="black")
        self.balance_label.pack(pady=5)

        # Ставка
        self.bet_label = tk.Label(root, text=f"Ставка: {self.bet}",
                                  font=("Arial", 16, "bold"), fg="white", bg="black")
        self.bet_label.pack(pady=5)

        # Экран автомата
        self.reel_frame = tk.Frame(root, bg="gray20", bd=8, relief="ridge")
        self.reel_frame.pack(pady=20)

        self.reels = []
        for i in range(3):
            lbl = tk.Label(self.reel_frame, text=random.choice(list(symbols.keys())),
                           font=("Arial", 48), width=3, height=1, bg="black", fg="white")
            lbl.grid(row=0, column=i, padx=20)
            self.reels.append(lbl)

        # Кнопки ставок
        button_frame = tk.Frame(root, bg="black")
        button_frame.pack(pady=15)

        self.spin_button = tk.Button(button_frame, text="🎰 Крутить", font=("Arial", 18, "bold"),
                                     bg="green", fg="white", width=12, command=self.spin)
        self.spin_button.grid(row=0, column=0, padx=8)

        self.double_button = tk.Button(button_frame, text="x2 ставка", font=("Arial", 18, "bold"),
                                       bg="orange", fg="white", width=12, command=self.double_bet)
        self.double_button.grid(row=0, column=1, padx=8)

        self.half_button = tk.Button(button_frame, text="½ ставка", font=("Arial", 18, "bold"),
                                     bg="blue", fg="white", width=12, command=self.half_bet)
        self.half_button.grid(row=0, column=2, padx=8)

        self.reset_button = tk.Button(button_frame, text="Сброс ставки", font=("Arial", 18, "bold"),
                                      bg="purple", fg="white", width=12, command=self.reset_bet)
        self.reset_button.grid(row=0, column=3, padx=8)

        # Сообщения
        self.msg_label = tk.Label(root, text="", font=("Arial", 18, "bold"),
                                  fg="gold", bg="black")
        self.msg_label.pack(pady=10)

    def double_bet(self):
        self.bet = base_bet * 2
        self.update_bet_label()
        self.double_button.configure(bg="red")
        self.half_button.configure(bg="blue")
        self.reset_button.configure(bg="purple")

    def half_bet(self):
        self.bet = base_bet // 2
        self.update_bet_label()
        self.half_button.configure(bg="red")
        self.double_button.configure(bg="orange")
        self.reset_button.configure(bg="purple")

    def reset_bet(self):
        self.bet = base_bet
        self.update_bet_label()
        self.reset_button.configure(bg="red")
        self.double_button.configure(bg="orange")
        self.half_button.configure(bg="blue")

    def update_bet_label(self):
        self.bet_label.config(text=f"Ставка: {self.bet}")

    def spin(self):
        if self.is_spinning or self.coins < self.bet:
            return

        self.is_spinning = True
        self.coins -= self.bet
        self.balance_label.config(text=f"Монеты: {self.coins}")
        self.msg_label.config(text="🎲 Крутим барабаны...", fg="white")

        Thread(target=self.animate_spin).start()

    def animate_spin(self):
        all_symbols = list(symbols.keys())
        weights = [symbols[s]["weight"] for s in all_symbols]

        # Анимация кручения
        for _ in range(20):
            for reel in self.reels:
                reel.config(text=random.choices(all_symbols, weights=weights, k=1)[0], fg="white")
            time.sleep(0.1)

        # Итоговые символы
        final = random.choices(all_symbols, weights=weights, k=3)

        for i in range(3):
            symbol = final[i]
            # Если рубин, делаем радужную анимацию
            if symbols[symbol]["highlight"] == "rainbow":
                self.rainbow_flash(self.reels[i])
            else:
                self.reels[i].config(text=symbol, fg=symbols[symbol]["highlight"])

        # Подсчёт выигрыша
        winnings = sum(symbols[s]["value"] for s in final)
        if self.bet == base_bet * 2:
            winnings *= 2
        elif self.bet == base_bet // 2:
            winnings //= 2

        self.coins += winnings
        self.balance_label.config(text=f"Монеты: {self.coins}")

        # Сообщение о выигрыше
        if winnings > 0:
            self.msg_label.config(text=f"🎉 Ты выиграл {winnings} монет! 🎉", fg="lime")
        else:
            self.msg_label.config(text="😢 Не повезло! Попробуй ещё раз!", fg="red")

        if self.coins < base_bet // 2:
            self.msg_label.config(text="💀 Монеты закончились! Игра окончена.")
            self.spin_button.config(state="disabled")

        self.is_spinning = False

    def rainbow_flash(self, label):
        for _ in range(7):
            for color in rainbow_colors:
                label.config(fg=color)
                label.update()
                time.sleep(0.05)


# --- ЗАПУСК ---
root = tk.Tk()
game = SlotMachine(root)
root.mainloop()
