from faker import Faker
from random import choice
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

faker = Faker()

words = []
secret_word = ""
hidden_word = ""
incorrect_letters = []
tries = 10

def generate_words(num_words, min_length, max_length):
    return [faker.word().lower() for _ in range(num_words) if min_length <= len(faker.word().lower()) <= max_length]

def choose_secret_word(words):
    return choice(words)

def start_game(difficulty):
    global words, secret_word, hidden_word, incorrect_letters, tries

    # Clear previous widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Set difficulty level and word generation parameters
    if difficulty == "easy":
        num_words = 20
        min_length = 2
        max_length = 4
    elif difficulty == "medium":
        num_words = 30
        min_length = 5
        max_length = 8
    elif difficulty == "hard":
        num_words = 40
        min_length = 8
        max_length = 12
    else:
        messagebox.showerror("Error", "Invalid difficulty level selected.")
        return

    words = generate_words(num_words, min_length, max_length)
    secret_word = choose_secret_word(words)
    hidden_word = "-" * len(secret_word)
    incorrect_letters = []
    tries = 10

    # Clear previous widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Show randomly generated words
    words_label = tk.Label(window, text="Random Words:", font=("Arial", 16))
    words_label.pack()

    for word in words:
        word_label = tk.Label(window, text=word, font=("Arial", 12))
        word_label.pack()

    # Show hidden word
    global hidden_word_label
    hidden_word_label = tk.Label(window, text=hidden_word, font=("Arial", 24))
    hidden_word_label.pack()

    # Show incorrect letters
    global incorrect_letters_label
    incorrect_letters_label = tk.Label(window, text=f"Incorrect Letters: {' '.join(incorrect_letters)}", font=("Arial", 16))
    incorrect_letters_label.pack()

    # Show tries left
    global tries_label
    tries_label = tk.Label(window, text=f"Tries Left: {tries}", font=("Arial", 16))
    tries_label.pack()

    # Create input field and submit button
    input_label = tk.Label(window, text="Enter a letter:", font=("Arial", 16))
    input_label.pack()

    global input_entry
    input_entry = tk.Entry(window, width=5, font=("Arial", 16))
    input_entry.pack()
    input_entry.bind("<Return>", lambda event: check_guess(input_entry.get()))  # Bind Enter key event

    submit_button = ttk.Button(window, text="Submit", command=lambda: check_guess(input_entry.get()))
    submit_button.pack()

    # Create back button
    back_button = ttk.Button(window, text="Back", command=select_difficulty)
    back_button.pack(side=tk.BOTTOM, pady=10, padx=10, anchor=tk.SW)

def check_guess(guess):
    global tries
    if guess.lower() in secret_word:
        update_hidden_word(guess.lower())
    else:
        incorrect_letters.append(guess.lower())
    tries -= 1

    # Clear the input field
    input_entry.delete(0, tk.END)

    # Update UI
    update_ui()

    if hidden_word == secret_word:
        messagebox.showinfo("Congratulations!", "You guessed the secret word!")
        play_again()
    elif tries == 0:
        messagebox.showinfo("Game Over", f"You have run out of tries!\nThe correct word was '{secret_word}'.")
        play_again()

def update_hidden_word(letter):
    global hidden_word
    updated_word = ""
    for i in range(len(secret_word)):
        if secret_word[i] == letter:
            updated_word += letter
        else:
            updated_word += hidden_word[i]
    hidden_word = updated_word

def update_ui():
    hidden_word_label.config(text=hidden_word)
    incorrect_letters_label.config(text=f"Incorrect Letters: {' '.join(incorrect_letters)}")
    tries_label.config(text=f"Tries Left: {tries}")

def reset_game():
    global words, secret_word, hidden_word, incorrect_letters, tries
    words = []
    secret_word = ""
    hidden_word = ""
    incorrect_letters = []
    tries = 10
    start_button.pack(pady=100, ipadx=20, ipady=10)  # Repack the start_button to make it visible again

def play_again():
    # Clear previous widgets
    for widget in window.winfo_children():
        widget.destroy()

    play_again_button = ttk.Button(window, text="Play Again", command=select_difficulty, style="TButton")
    play_again_button.pack(pady=10)

    exit_button = ttk.Button(window, text="Exit", command=exit_game, style="TButton")
    exit_button.pack(pady=10)

    # Center align the buttons
    window.update()
    play_again_button.place(x=(window.winfo_width() - play_again_button.winfo_width()) // 2, y=200)
    exit_button.place(x=(window.winfo_width() - exit_button.winfo_width()) // 2, y=260)

def exit_game():
    window.destroy()

def select_difficulty():
    # Clear previous widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Difficulty level selection
    level_label = tk.Label(window, text="Select Difficulty Level:", font=("Arial", 16))
    level_label.pack()

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14))

    easy_button = ttk.Button(window, text="Easy", command=lambda: start_game("easy"), width=15, style="TButton")
    easy_button.pack()

    medium_button = ttk.Button(window, text="Medium", command=lambda: start_game("medium"), width=15, style="TButton")
    medium_button.pack()

    hard_button = ttk.Button(window, text="Hard", command=lambda: start_game("hard"), width=15, style="TButton")
    hard_button.pack()

    # Sync the appearance of buttons
    style.configure("TButton", font=("Arial", 16))
    style.configure("TStartButton.TButton", font=("Arial", 16), padding=20, width=15)  # Adjust the padding and size of the button

# Create the main window
window = tk.Tk()
window.title("Guess the Word Game")
window.geometry("720x720")

style = ttk.Style()
style.configure("TButton", font=("Arial", 16))

style.configure("TStartButton.TButton", font=("Arial", 16), padding=20)  # Adjust the padding for the START button
style.map("TStartButton.TButton",
          foreground=[('active', 'disabled', 'white')],
          background=[('!active', 'black')])

start_button = ttk.Button(window, text="START", command=lambda: select_difficulty(), style="TStartButton.TButton")
exit_button = ttk.Button(window, text="EXIT", command=exit_game, style="TStartButton.TButton")

start_button.pack(pady=20)
exit_button.pack(pady=20)

# Center align the buttons
window.update()
start_button.place(x=(window.winfo_width() - start_button.winfo_width()) // 2, y=200)
exit_button.place(x=(window.winfo_width() - exit_button.winfo_width()) // 2, y=260)

# Run the GUI main loop
window.mainloop()