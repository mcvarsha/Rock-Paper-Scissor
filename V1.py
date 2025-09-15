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
    # Labels and scores
    labels = ['User', 'Computer']
    user_score = int(playerscore['text'])
    computer_score = int(computerscore['text'])

    # Data for visualization
    user_data = np.random.normal(0, 1, user_score)
    computer_data = np.random.normal(0, 1, computer_score)

    plt.figure(figsize=(16, 12))

    # Histogram
    plt.subplot(3, 3, 1)
    plt.hist(user_data, bins=30, color='blue', alpha=0.7, label='User')
    plt.hist(computer_data, bins=30, color='red', alpha=0.7, label='Computer')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Scores Histogram')
    plt.legend()

    # Heatmap
    matrix_data = np.random.rand(10, 10)
    plt.subplot(3, 3, 2)
    plt.imshow(matrix_data, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Heatmap')

    # Scatter Plot
    plt.subplot(3, 3, 3)
    x_user = np.random.rand(user_score)
    y_user = np.random.rand(user_score)
    x_computer = np.random.rand(computer_score)
    y_computer = np.random.rand(computer_score)
    plt.scatter(x_user, y_user, color='blue', alpha=0.5, label='User')
    plt.scatter(x_computer, y_computer, color='red', alpha=0.5, label='Computer')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scores Scatter Plot')
    plt.legend()

    # Box Plot
    plt.subplot(3, 3, 4)
    plt.boxplot([user_data, computer_data], labels=['User', 'Computer'])
    plt.xlabel('Player')
    plt.ylabel('Score')
    plt.title('Scores Box Plot')

    # Pie Chart
    plt.subplot(3, 3, 5)
    counts = [user_score, computer_score]
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=['blue', 'red'])
    plt.title('Player Scores Distribution')

    # Bar Plot
    plt.subplot(3, 3, 6)
    plt.bar(labels, counts, color=['blue', 'red'])
    plt.xlabel('Player')
    plt.ylabel('Score')
    plt.title('Player Scores')
    
    # Line Plot
    plt.subplot(3, 3, 7)
    plt.plot(labels, counts, marker='o', linestyle='-', color='green')
    plt.xlabel('Player')
    plt.ylabel('Score')
    plt.title('Player Scores Trend')

    plt.tight_layout()
    plt.show()


# Button for Data Visualization
visualize_button = Button(root, text="Visualize Data", bg="orange", fg="black", command=visualize_data)
visualize_button.grid(row=5, column=2)

root.mainloop()
