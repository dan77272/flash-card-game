from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# data = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

current_card = {}


def random_french():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(front_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(front_image, image=card_back_image)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def is_known():
    data_dict.remove(current_card)
    data_to_learn = pandas.DataFrame(data_dict)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    random_french()


window = Tk()

window.title("Flash Card Game")
window.configure(background=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
front_image = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(column=0, row=0, columnspan=2)

language = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

my_right_image = PhotoImage(file="images/right.png")
right_button = Button(image=my_right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

my_wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=my_wrong_image, highlightthickness=0, command=random_french)
wrong_button.grid(column=0, row=1)

random_french()

window.mainloop()
