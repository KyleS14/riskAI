import tkinter as tk
from PIL import Image, ImageTk
import cv2
#import numpy as np

# Create main window
root = tk.Tk()
root.title("Edge Region Labeler")
root.state("zoomed")

# Canvas to display image
canvas = tk.Label(root)
canvas.pack()

# Label to show number of regions
region_label = tk.Label(root, text="Detected Regions: 0", font=("Arial", 14))
region_label.pack(pady=5)

# Global variables
img_cv = None
regions = []

def open_image():

    global img_cv
    image_path = 'riskboard_resized.jpg'
    img_cv = cv2.imread(image_path)
    display_image(img_cv)
    region_label.config(text="Detected Regions: 0")  # Reset label

def display_image(img_cv):
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    canvas.configure(image=img_tk)
    canvas.image = img_tk  # Keep reference

def detect_edges():
    global regions

    if img_cv is None:
        return

    # Step 1: Convert to grayscale and detect edges
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # Step 2: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours]

    # Step 3: Create a labeled version of the edge image
    labeled_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    for idx, contour in enumerate(regions):
        # Get center point of contour (via moments)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.putText(labeled_img, str(idx + 1), (cx, cy),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        # Optionally draw the contour as well
            if idx==0:
                cv2.drawContours(labeled_img, [contour], -1, (255, 0, 0), 1)
    # Step 4: Display labeled image and update region count
    display_image(labeled_img)
    region_label.config(text=f"Detected Regions: {len(regions)}")

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

open_image()
detect_edges()

#assigned regions to territories

def on_click(event):
    print(f"Mouse clicked at {event.x}, {event.y}")
    for i, region in enumerate(regions):
        if cv2.pointPolygonTest(region, (event.x, event.y), False) >= 0:
            print(f"Clicked inside region {i + 1}")
            break

canvas.bind("<Button-1>", on_click)




root.mainloop()




'''
import tkinter as tk
from PIL import ImageTk,Image

def gamespace():
    # Create the main window
    root = tk.Tk()
    root.state('zoomed')
    root.title("Risk Game")

    #creates risk background
    image_path = "riskmap_resized.jpg"
    original_image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(original_image)
    image_label = tk.Label(root, image=tk_image)
    image_label.image = tk_image
    image_label.pack(padx=5, pady=5)

    # Start the GUI event loop
    root.mainloop()

def on_space(event):
    #closes window and opens a new one
    root1.destroy()
    gamespace()


#opens gui window
root1 = tk.Tk()
root1.geometry("895x473")
root1.title("Risk Game")

#background image
image_path1 = "risk_background.jpg"
original_image1 = Image.open(image_path1)
tk_image1 = ImageTk.PhotoImage(original_image1)
image_label1 = tk.Label(root1, image=tk_image1)
image_label1.image = tk_image1
image_label1.pack(padx=5, pady=5)

#textbox
text_label = tk.Label(root1, text="Press Space to Start Game!", fg = "#f00", bg = "#000",font=("Arial", 16, "bold"))
text_label.place(relx=0.5, rely=0.8, anchor='center') #centers textbox

root1.bind("<space>", on_space)  # bind space key
root1.mainloop()
'''