import subprocess
from tkinter import *

# Function to execute the other Python program
def run_other_program():
    subprocess.Popen(["python", "project.py"])

# Create the main window
root = Tk()
root.title("Rock Paper Scissors: Computer vs Human")
root.configure(background="pink")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center coordinates
center_x = screen_width // 2
center_y = screen_height // 2

# Function to execute the other Python program
def run_other_program():
    subprocess.Popen(["python", "Visuala.py"])

# Create a custom font for headings
heading_font = ('Helvetica', 24, 'bold')
subheading_font = ('Helvetica', 18, 'bold')

# Create a label for the heading
heading_label = Label(root, text="Rock Paper Scissors Game", font=heading_font, fg="blue")
heading_label.place(relx=0.5, rely=0.4, anchor=CENTER)

# Create a label for the subheading
subheading_label = Label(root, text="Computer vs Human", font=subheading_font, fg="green")
subheading_label.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create a button to run the other program
play_button = Button(root, text="Let us play", command=run_other_program, font=subheading_font, fg="red")
play_button.place(relx=0.5, rely=0.6, anchor=CENTER)

# Start the Tkinter event loop
root.mainloop()
