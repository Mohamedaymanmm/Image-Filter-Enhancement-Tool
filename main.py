import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

root = tk.Tk()
title_label = tk.Label(root, text="Image Enhancement Tool", font=("Arial", 16))
title_label.pack(pady=10)
root.resizable(False, False)
root.geometry('600x600')

img = None

gray_img = None
blur_img = None
edge_img = None


def select_file():
    filetypes = (
        ('Image files', '*.png *.jpg *.jpeg'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    if not filename:
        return

   
    global img, gray_img, blur_img, edge_img
    img = cv2.imread(filename)
    
    display_img = None
    gray_img = None
    blur_img = None
    edge_img = None

    show_image(img)
    


def show_original():
    global img

    if img is None:
        print("No image loaded")
        return
    
    show_image(img)



def apply_grayscale():
    global img, gray_img

    if img is None:
        print("No image loaded")
        return

    if gray_img is None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    show_image(gray_img)
    


def apply_blur():
    global img, blur_img

    if img is None:
        print("No image loaded")
        return

    if blur_img is None:
        blur_img = cv2.GaussianBlur(img, (5,5), 0)

    show_image(blur_img)


def apply_edge():
    global img, edge_img

    if img is None:
        print("No image loaded")
        return
    
    if edge_img is None:
        edge_img = cv2.Canny(img, 100, 200)

    show_image(edge_img)


def save_image():
    global display_img

    if display_img is None:
        print("No image to save")
        return

    file = fd.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG file", "*.png"),
            ("JPG file", "*.jpg"),
            ("All Files", "*.*")
        ]
    )

    if not file:
        return

    cv2.imwrite(file, display_img)
    print("Image saved successfully")


def show_image(img):
    global display_img

    display_img = img  

    if len(img.shape) == 2:
        img_rgb = img
    else:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(img_rgb)
    pil_img.thumbnail((300, 300))

    tk_img = ImageTk.PhotoImage(pil_img)

    image_label.config(image=tk_img)
    image_label.image = tk_img 

def reset_image():
    global img, gray_img, blur_img, edge_img

    if img is None:
        print("No image loaded")
        return

    gray_img = None
    blur_img = None
    edge_img = None

    show_image(img)


top_frame = tk.Frame(root)
top_frame.pack(pady=10)

button = tk.Button(top_frame, text="Load Image", width=25, command=select_file)
button.pack()

image_label = tk.Label(root)
image_label.pack(pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack()

original_button = tk.Button(buttons_frame, text="Original", width=15, command=show_original)
original_button.grid(row=0, column=0, padx=5, pady=5)

gray_button = tk.Button(buttons_frame, text="Grayscale", width=15, command=apply_grayscale)
gray_button.grid(row=0, column=1, padx=5, pady=5)

blur_button = tk.Button(buttons_frame, text="Blur", width=15, command=apply_blur)
blur_button.grid(row=1, column=0, padx=5, pady=5)

edge_button = tk.Button(buttons_frame, text="Edge", width=15, command=apply_edge)
edge_button.grid(row=1, column=1, padx=5, pady=5)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

save_button = tk.Button(bottom_frame, text="Save", width=15, command=save_image)
save_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(bottom_frame, text="Reset", width=15, command=reset_image)
reset_button.grid(row=0, column=1, padx=5)
   
root.mainloop()