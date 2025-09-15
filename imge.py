import tkinter as tk
from tkinter import filedialog
import os

# Function to identify clicked image
def identify_image(image_path):
    print("You selected:", image_path)
    # Display the selected image
    selected_img = tk.PhotoImage(file=image_path)
    selected_label.config(image=selected_img)
    selected_label.image = selected_img
    # Check which image was selected and display corresponding text
    filename = os.path.basename(image_path)
    if filename == "rock.png":
        selected_text.set("You selected: Rock")
    elif filename == "paper.png":
        selected_text.set("You selected: Paper")
    elif filename == "scissors.png":
        selected_text.set("You selected: Scissors")

# Function to open file dialog and get the selected image
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        identify_image(file_path)

# Create the main window
root = tk.Tk()
root.title("Image Identification")

# Add some styling
root.configure(bg="#f0f0f0")  # Set background color

# Add a heading
heading_label = tk.Label(root, text="Image Identification", bg="#f0f0f0", font=("Helvetica", 16, "bold"))
heading_label.pack(pady=10)

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image, bg="#008CBA", fg="white", font=("Helvetica", 12))
select_button.pack(pady=10)

# Create a label to display the selected image
selected_label = tk.Label(root)
selected_label.pack()

# Variable to hold the selected text
selected_text = tk.StringVar()

# Label to display the selected text
selected_text_label = tk.Label(root, textvariable=selected_text, bg="#f0f0f0", font=("Helvetica", 12))
selected_text_label.pack()

# Run the main event loop
root.mainloop()
