import tkinter as tk
from PIL import ImageTk,Image

def on_button_click():
    print("Button was clicked!")

# Create the main window
root = tk.Tk()
root.state('zoomed')
root.title("Risk Game")

image_path = "riskmap_resized.jpg"
original_image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(original_image)

# Create a Label to display the image
image_label = tk.Label(root, image=tk_image)

image_label.image = tk_image  # Keep a reference
# Place the Label in the GUI
image_label.pack(padx=5, pady=5)
# Create a button
my_button = tk.Button(root, text="Touch Me", command=on_button_click)
my_button.place(x=100, y=300)


# Start the GUI event loop
root.mainloop()