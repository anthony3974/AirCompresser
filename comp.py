import tkinter
from tkinter import PhotoImage

DEBUG = False
bcbg="red"
fillamt=0

from pygame import mixer
from pygame import mixer as mx

mixer.init(); mx.init()
s1=mixer.Sound("comp.mp3"); s2=mx.Sound("hose.mp3")

root = tkinter.Tk()
root.geometry("500x500+550+300")

# Generate a list of image paths (e.g., "img/fill0.png", "img/fill5.png", ..., "img/fill95.png")
image_paths = [f"img/fill{i}.png" for i in range(0, 105, 5)]

# Load the images into a dictionary
images = {}
for idx, path in enumerate(image_paths):
    try:
        images[idx] = PhotoImage(file=path)  # Load image
    except Exception as e:
        print(f"Error loading {path}: {e}")

compress=None
def fill():
    global fillamt
    if fillamt < 100:
        fillamt+=1
        compress.configure(image=images[convert(fillamt)], text=fillamt)
        mixer.Sound.play(s1)
def low(b=True):
    global fillamt
    if fillamt > 0:
        fillamt-=1
        compress.configure(image=images[convert(fillamt)], text=fillamt)
        if b: mx.Sound.play(s2)
def check():
    return compress.cget("text")
def convert(x):
    return round(x/5)
tmrid=None
def empty():
    global tmrid
    low()
    low(False)
    tmrid=root.after(950, empty)
btnempty=None
def btnempty():
    global tmrid
    state=btnempty.cget("relief")
    if state == tkinter.SUNKEN:
        btnempty.configure(relief=tkinter.RAISED, text="On")
        root.after_cancel(tmrid)
    else:
        btnempty.configure(relief=tkinter.SUNKEN, text="Off")
        tmrid=root.after(500, empty)
lblmeter=None
def refreshmeter():
    global lblmeter, fillamt
    lblmeter.configure(text=fillamt)
    root.after(500, refreshmeter)
# Create a 4x4 grid
for row in range(4):
    for col in range(4):
        # Add a frame to each cell with a border
        if row == 1 and col == 0:
            frame = tkinter.Frame(root, width=100, height=100, highlightbackground=bcbg, highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5)

            lblmeter = tkinter.Label(frame, text=0, width=13, height=6)
            lblmeter.pack()
        elif row == 1 and col == 1:
            frame = tkinter.Frame(root, width=200, height=100)
            frame.grid(row=row, column=col, columnspan=2, padx=5, pady=5)
            
            # Use the correct key to access the image
            if 0 in images:  # Ensure the image exists
                compress = tkinter.Label(frame, image=images[0], text=0)
                compress.pack(expand=True)
        elif row == 1 and col == 2:
            pass
        elif row == 2 and col == 1:
            frame = tkinter.Frame(root, width=100, height=100, highlightbackground=bcbg, highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5)

            button = tkinter.Button(frame, text="Fill", command=fill, width=13, height=6)
            button.pack()
        elif row == 2 and col == 2:
            frame = tkinter.Frame(root, width=100, height=100, highlightbackground=bcbg, highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5)

            button = tkinter.Button(frame, text="Low", command=low, width=13, height=6)
            button.pack()
        elif row == 2 and col == 3:
            frame = tkinter.Frame(root, width=100, height=100, highlightbackground=bcbg, highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5)

            btnempty = tkinter.Button(frame, text="On", command=btnempty, width=13, height=6)
            btnempty.pack()
        else:
            frame = tkinter.Frame(root, width=100, height=100, highlightbackground=bcbg, highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5)

            if DEBUG:
                label = tkinter.Label(frame, text=f"{row}:{col}", width=13, height=6)
                label.pack()

                print(row, " ", col)
wait = None
def mcomp():
    global wait
    if fillamt < 100 and wait != True:
        fill()
    if fillamt == 100:
        wait=True
    if fillamt < 75:
        wait=False

    root.after(1000, mcomp)

root.after(1000, mcomp)
root.after(500, refreshmeter)

root.mainloop()
