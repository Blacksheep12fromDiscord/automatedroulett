import tkinter as tk
import random

class RouletteGame:
    def __init__(self, root, table_number):
        self.table_number = table_number
        self.money = 10000  # Starting money
        self.history = []  # To keep track of betting history
        self.current_bet = 5  # Initial bet amount
        self.running = False  # To control game running state
        self.rounds = 0  # To keep track of rounds to play
        self.infinite_mode = False  # To check if game is in infinite mode

        # Set up the frame for this table
        self.frame = tk.Frame(root, borderwidth=2, relief="groove")
        self.frame.grid(row=(table_number - 1) // 6, column=(table_number - 1) % 6, padx=5, pady=5)

        # Display current money
        self.money_label = tk.Label(self.frame, text=f"Table {self.table_number} - Money: ${self.money}", font=("Helvetica", 12))
        self.money_label.pack()

        # Display history
        self.history_label = tk.Label(self.frame, text="History:", font=("Helvetica", 10))
        self.history_label.pack()
        self.history_listbox = tk.Listbox(self.frame, width=40, height=6)
        self.history_listbox.pack()

        # Input field for custom rounds
        self.rounds_entry_label = tk.Label(self.frame, text="Rounds (0 for infinite):")
        self.rounds_entry_label.pack()
        self.rounds_entry = tk.Entry(self.frame)
        self.rounds_entry.pack()

        # Input field for custom bet amount
        self.bet_entry_label = tk.Label(self.frame, text="Bet amount:")
        self.bet_entry_label.pack()
        self.bet_entry = tk.Entry(self.frame)
        self.bet_entry.insert(tk.END, str(self.current_bet))  # Set initial bet amount
        self.bet_entry.pack()

        # Start button
        self.start_button = tk.Button(self.frame, text="Start", command=self.start_game)
        self.start_button.pack()

        # Stop button
        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop_game, state=tk.DISABLED)
        self.stop_button.pack()

    def start_game(self):
        try:
            self.rounds = int(self.rounds_entry.get())  # Fetch rounds from the entry widget
            self.current_bet = int(self.bet_entry.get())
        except ValueError:
            self.history.append("Error: Invalid number of rounds or bet amount.")
            self.update_history()
            return
        
        if self.rounds < 0 or self.current_bet <= 0:
            self.history.append("Error: Number of rounds cannot be negative and bet amount must be positive.")
            self.update_history()
            return
        
        self.infinite_mode = (self.rounds == 0)
        self.running = True
        self.stop_button.config(state=tk.NORMAL if self.infinite_mode else tk.DISABLED)  # Enable Stop button only for infinite mode

        if self.infinite_mode:
            self.run_rounds_with_delay()  # Run with delay
        else:
            self.run_rounds_without_delay()  # Run without delay

    def stop_game(self):
        self.running = False
        self.stop_button.config(state=tk.DISABLED)  # Disable Stop button when game is stopped

    def run_rounds_with_delay(self):
        if not self.running:
            return

        if self.money <= 0:
            self.history.append("Game Over: You're out of money.")
            self.update_history()
            self.running = False
            self.stop_button.config(state=tk.DISABLED)  # Disable Stop button when game is over
            return

        if self.current_bet > self.money:
            self.history.append("Error: Bet amount exceeds available money.")
            self.update_history()
            self.running = False
            self.stop_button.config(state=tk.DISABLED)  # Disable Stop button when game is over
            return

        bet = self.current_bet
        choice = 'black'

        # Spin the wheel
        result = random.randint(0, 36)
        color = "red" if result % 2 == 1 else "black"
        if result == 0:
            color = "green"

        outcome = f"{result} {color}"
        self.history.append(f"Bet: ${bet}, Choice: {choice}, Result: {outcome}")

        if color == choice:
            self.money += bet
            self.current_bet = int(self.bet_entry.get())  # Update bet to latest input
        else:
            self.money -= bet
            self.current_bet *= 2  # Double the bet after a loss

        self.money_label.config(text=f"Table {self.table_number} - Money: ${self.money}")

        self.update_history()

        if self.running:
            self.frame.after(100, self.run_rounds_with_delay)  # Call run_rounds_with_delay after 0.1 seconds

    def run_rounds_without_delay(self):
        if not self.running:
            return

        if self.rounds == 0 and not self.infinite_mode:
            return
        
        if self.money <= 0:
            self.history.append("Game Over: You're out of money.")
            self.update_history()
            self.running = False
            self.stop_button.config(state=tk.DISABLED)  # Disable Stop button when game is over
            return

        if self.current_bet > self.money:
            self.history.append("Error: Bet amount exceeds available money.")
            self.update_history()
            self.running = False
            self.stop_button.config(state=tk.DISABLED)  # Disable Stop button when game is over
            return

        bet = self.current_bet
        choice = 'black'

        # Spin the wheel
        result = random.randint(0, 36)
        color = "red" if result % 2 == 1 else "black"
        if result == 0:
            color = "green"

        outcome = f"{result} {color}"
        self.history.append(f"Bet: ${bet}, Choice: {choice}, Result: {outcome}")

        if color == choice:
            self.money += bet
            self.current_bet = int(self.bet_entry.get())  # Update bet to latest input
        else:
            self.money -= bet
            self.current_bet *= 2  # Double the bet after a loss

        self.money_label.config(text=f"Table {self.table_number} - Money: ${self.money}")

        self.update_history()

        if self.rounds > 0:
            self.rounds -= 1
            self.frame.after(0, self.run_rounds_without_delay)  # Call run_rounds_without_delay immediately

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)
        # Auto-scroll to the bottom
        self.history_listbox.yview(tk.END)


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roulette Game - Multiple Tables")

        # Create a frame to hold the tables
        self.tables_frame = tk.Frame(root)
        self.tables_frame.pack(fill=tk.BOTH, expand=True)

        # Create 12 roulette tables (6 per row)
        self.tables = []
        for i in range(12):
            table = RouletteGame(self.tables_frame, i + 1)
            self.tables.append(table)

        # Create rows of tables
        for i in range(2):  # 2 rows
            for j in range(6):  # 6 columns
                self.tables[i * 6 + j].frame.grid(row=i, column=j, padx=5, pady=5)

        # Frame for controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10, fill=tk.X)

        # Input field for bet amount for all tables
        self.all_bet_entry_label = tk.Label(self.controls_frame, text="Bet amount for all tables:")
        self.all_bet_entry_label.grid(row=0, column=0, padx=5)
        self.all_bet_entry = tk.Entry(self.controls_frame)
        self.all_bet_entry.grid(row=1, column=0, padx=5)

        # Input field for rounds for all tables
        self.all_rounds_entry_label = tk.Label(self.controls_frame, text="Rounds (0 for infinite) for all tables:")
        self.all_rounds_entry_label.grid(row=0, column=1, padx=5)
        self.all_rounds_entry = tk.Entry(self.controls_frame)
        self.all_rounds_entry.grid(row=1, column=1, padx=5)

        # Centered buttons frame
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=20)

        # Set bet button
        self.set_bet_button = tk.Button(self.buttons_frame, text="Set Bet for All Tables", command=self.set_bet_for_all)
        self.set_bet_button.grid(row=0, column=0, padx=5)

        # Set rounds button
        self.set_rounds_button = tk.Button(self.buttons_frame, text="Set Rounds for All Tables", command=self.set_rounds_for_all)
        self.set_rounds_button.grid(row=0, column=1, padx=5)

        # Start all tables button
        self.start_all_button = tk.Button(self.buttons_frame, text="Start All Tables", command=self.start_all_tables)
        self.start_all_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Stop all tables button
        self.stop_all_button = tk.Button(self.buttons_frame, text="Stop All Tables", command=self.stop_all_tables)
        self.stop_all_button.grid(row=2, column=0, columnspan=2, pady=5)

    def set_bet_for_all(self):
        try:
            bet_amount = int(self.all_bet_entry.get())
            if bet_amount <= 0:
                raise ValueError("Bet amount must be positive.")
        except ValueError:
            print("Error: Invalid bet amount.")  # Debug print
            return
        
        for table in self.tables:
            table.current_bet = bet_amount
            table.bet_entry.delete(0, tk.END)
            table.bet_entry.insert(tk.END, str(bet_amount))

    def set_rounds_for_all(self):
        try:
            rounds_amount = int(self.all_rounds_entry.get())
        except ValueError:
            print("Error: Invalid rounds amount.")  # Debug print
            return
        
        for table in self.tables:
            table.rounds = rounds_amount
            table.rounds_entry.delete(0, tk.END)
            table.rounds_entry.insert(tk.END, str(rounds_amount))  # Update the rounds entry widget

    def start_all_tables(self):
        for table in self.tables:
            table.start_game()

    def stop_all_tables(self):
        for table in self.tables:
            table.stop_game()


# Create the main window
root = tk.Tk()
app = MainApp(root)
root.mainloop()
