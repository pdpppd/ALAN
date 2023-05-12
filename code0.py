
from tkinter import *

# Define the canvas
root = Tk()
canvas = Canvas(root, width=500, height=500)
canvas.pack()

# Draw the cat
canvas.create_oval(175, 175, 325, 325, fill="white", outline="black")
canvas.create_oval(200, 220, 240, 260, fill="black")
canvas.create_oval(260, 220, 300, 260, fill="black")
canvas.create_oval(225, 270, 275, 320, fill="black")
canvas.create_oval(225, 280, 230, 285, fill="white")
canvas.create_oval(270, 280, 275, 285, fill="white")
canvas.create_arc(200, 220, 300, 320, start=190, extent=160, fill="white", outline="black", width=3)

# Run the tkinter loop
root.mainloop()
