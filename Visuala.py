from tkinter import *
from PIL import Image, ImageTk
from random import randint
import matplotlib.pyplot as plt
import numpy as np

# Main window
root = Tk()
root.title("Rock Scissor Paper")
root.configure(background="blue")

# Picture
rock_img = ImageTk.PhotoImage(Image.open("1.png"))
paper_img = ImageTk.PhotoImage(Image.open("2.png"))
scissor_img = ImageTk.PhotoImage(Image.open("3.png"))
rock_img_comp = ImageTk.PhotoImage(Image.open("4.png"))
paper_img_comp = ImageTk.PhotoImage(Image.open("5.png"))
scissor_img_comp = ImageTk.PhotoImage(Image.open("6.png"))

# Insert picture
user_label = Label(root, image=scissor_img)
comp_label = Label(root, image=scissor_img)
comp_label.grid(row=1, column=0)
user_label.grid(row=1, column=4)

# Scores
playerscore = Label(root, text=0, font=100, bg="green", fg="white")
computerscore = Label(root, text=0, font=100, bg="green", fg="white")
computerscore.grid(row=1, column=1)
playerscore.grid(row=1, column=3)

# Indicator
user_indi = Label(root, font=50, text="USER", bg="green", fg="white")
comp_indi = Label(root, font=50, text="COMPUTER", bg="green", fg="white")
user_indi.grid(row=0, column=3)
comp_indi.grid(row=0, column=1)

# Message
msg = Label(root, font=50, bg="green", fg="white")
msg.grid(row=3, column=2)

# Update message
def updateMessage(x):
    msg["text"] = x

# Update user score
def updateuserscore():
    score = int(playerscore['text'])
    score += 1
    playerscore['text'] = str(score)

# Update computer score
def updatecompscore():
    score = int(computerscore['text'])
    score += 1
    computerscore['text'] = str(score)

# Check winner
def checkwin(player, computer):
    if player == computer:
        updateMessage("It is a tie")
    elif player == "rock":
        if computer == "paper":
            updateMessage("You lose")
            updatecompscore()
        else:
            updateMessage("You win")
            updateuserscore()
    elif player == "paper":
        if computer == "scissor":
            updateMessage("You lose")
            updatecompscore()
        else:
            updateMessage("You win")
            updateuserscore()
    elif player == "scissor":
        if computer == "rock":
            updateMessage("You lose")
            updatecompscore()
        else:
            updateMessage("You win")
            updateuserscore()
    else:
        pass

# Update choices
choice = ["rock", "paper", "scissor"]
def updatechoices(x):
    # For computer
    compchoice = choice[randint(0, 2)]
    if compchoice == "rock":
        comp_label.configure(image=rock_img_comp)
    elif compchoice == "paper":
        comp_label.configure(image=paper_img_comp)
    else:
        comp_label.configure(image=scissor_img_comp)

    # For user
    if x == "rock":
        user_label.configure(image=rock_img)
    elif x == "paper":
        user_label.configure(image=paper_img)
    else:
        user_label.configure(image=scissor_img)
    checkwin(x, compchoice)

# Reset function
def reset_game():
    playerscore['text'] = "0"
    computerscore['text'] = "0"
    updateMessage("")
    user_label.configure(image=scissor_img)
    comp_label.configure(image=scissor_img)

# Buttons
rock = Button(root, width=20, height=2, text="ROCK", bg="brown", fg="white", command=lambda: updatechoices("rock")).grid(row=2, column=1)
paper = Button(root, width=20, height=2, text="PAPER", bg="red", fg="white", command=lambda: updatechoices("paper")).grid(row=2, column=2)
scissor = Button(root, width=20, height=2, text="SCISSOR", bg="pink", fg="white", command=lambda: updatechoices("scissor")).grid(row=2, column=3)

# Reset button
reset_button = Button(root, text="RESET", bg="yellow", fg="black", command=reset_game)
reset_button.grid(row=4, column=2)

# Data Visualization
def visualize_data():
    data = np.random.normal(0, 1, 1000)
    
    plt.figure(figsize=(12, 8))

    # Histogram
    plt.subplot(2, 3, 1)
    plt.hist(data, bins=30, color='purple', alpha=0.7)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')

    # Heatmap
    matrix_data = np.random.rand(10, 10)
    plt.subplot(2, 3, 2)
    plt.imshow(matrix_data, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Heatmap')

    # Scatter Plot
    x = np.random.rand(50)
    y = np.random.rand(50)
    sizes = np.random.rand(50) * 100
    colors = np.random.rand(50)
    plt.subplot(2, 3, 3)
    plt.scatter(x, y, s=sizes, c=colors, alpha=0.5)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scatter Plot')

    # Pie Chart
    labels = ['Rock', 'Paper', 'Scissors']
    counts = [int(playerscore['text']), int(computerscore['text']), 10 - int(playerscore['text']) - int(computerscore['text'])]
    plt.subplot(2, 3, 4)
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=['red', 'green', 'blue'])
    plt.title('Pie Chart')

    # Bar Plot
    plt.subplot(2, 3, 5)
    x = np.arange(len(labels))
    plt.bar(x, counts, color=['red', 'green', 'blue'])
    plt.xlabel('Selection')
    plt.ylabel('Count')
    plt.title('Bar Plot')
    plt.xticks(x, labels)

    # Line Plot
    plt.subplot(2, 3, 6)
    plt.plot(labels, counts, marker='o', linestyle='-', color='orange')
    plt.xlabel('Selection')
    plt.ylabel('Count')
    plt.title('Line Plot')

    plt.tight_layout()
    plt.show()

# Button for Data Visualization
visualize_button = Button(root, text="Visualize Data", bg="orange", fg="black", command=visualize_data)
visualize_button.grid(row=5, column=2)

root.mainloop()
