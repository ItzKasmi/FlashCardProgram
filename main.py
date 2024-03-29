from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

# ----------------------- CSV Functionality ------------------------ #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
    french_to_english = data.to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    french_to_english = data.to_dict(orient="records")

# --- Save Cards Left to CSV File --- #
def save_cards():
    new_data = pandas.DataFrame(french_to_english)
    new_data.to_csv("data/words_to_learn.csv", index=False)

# ----------------------- Button Functionality -------------- #
def right_pressed():
    french_to_english.remove(current_card)
    save_cards()
    next_card()

# ----------------------- Card Functionality ---------------- #
def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=f"{current_card["English"]}", fill="white")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_to_english)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=f"{current_card["French"]}", fill="black")
    flip_timer = window.after(3500, flip_card)


# ----------------------- UI Setup -------------------------- #
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3500, flip_card)

# --- Card --- #
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

# --- Text --- #
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

# --- Buttons --- #
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

right_button = Button(image=right, highlightthickness=0, command=right_pressed)
right_button.grid(column=1, row=1)

wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

# --- Starting Card --- #
next_card()

window.mainloop()
