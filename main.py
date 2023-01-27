import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helper import make_fuc,StdoutRedirector
import sys

        
        
root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

def draw_grid(rows, columns):
    for i in range(rows+1):
        canvas.create_line(0, i*50, columns*50, i*50)
    for i in range(columns+1):
        canvas.create_line(i*50, 0, i*50, rows*50)




rows, columns = 12,16
draw_grid(12, 16)

coordinates = []

def on_move(event):
    x, y = event.x, event.y
    if coordinates:
        canvas.create_line(coordinates[-1][0], coordinates[-1][1], x, y,width=2)
    coordinates.append((x, y))


def set_degree(degree):
    global upper_degree
    upper_degree = int(degree)
    print(f'Upper degree set to {upper_degree}')

def increment_degree():
    global upper_degree
    if upper_degree < 20:
        upper_degree += 1

    degree_slider.set(upper_degree)

def decrement_degree():
    global upper_degree
    if upper_degree > 1:
        upper_degree -= 1

    degree_slider.set(upper_degree)

    
def get_coordinates():
    global upper_degree
    df = pd.DataFrame(coordinates,columns=['x','y'])
    df['x']=(df['x'] - 400)/50
    df['y']=(rows-df['y'] + 300)/50
    

    df.to_csv('coordinates.csv',index=False)
    x = df['x'].to_numpy()

    y = df['y'].to_numpy()


    n = len(x)
    degree_upper = upper_degree
    degree_lower = 0

    X = x**degree_upper

    for i in range(degree_upper-1,degree_lower,-1):
        X = np.vstack((X,(x)**i))
    else:
        X = np.vstack((X,np.ones(n)))
   
    X = X.T
    W = np.linalg.inv(X.T @ X) @ X.T @ y
    my_fuc = make_fuc(W,degree_upper)

    print(f'predict fucntion : {my_fuc}')

    
def draw_graph():
    global upper_degree
    df = pd.DataFrame(coordinates,columns=['x','y'])
    df['x']=(df['x'] - 400)/50
    df['y']=(rows-df['y'] + 300)/50
    

    df.to_csv('coordinates.csv',index=False)
    x = df['x'].to_numpy()

    y = df['y'].to_numpy()

    n = len(x)
    degree_upper = upper_degree
    degree_lower = 0

    plt.plot(x,y,'.r')

    X = x**degree_upper

    for i in range(degree_upper-1,degree_lower,-1):
        X = np.vstack((X,(x)**i))
    else:
        X = np.vstack((X,np.ones(n)))
   
    X = X.T
    W = np.linalg.inv(X.T @ X) @ X.T @ y
    z = X @ W
    plt.scatter(x,z,s=50)
    
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.show()
    

def clear_canvas():
    canvas.delete("all")
    draw_grid(12,16)
    canvas.create_line(0, rows*50/2, columns*50, rows*50/2, width=3) # x-axis
    canvas.create_line(columns*50/2, 0, columns*50/2, rows*50, width=3) # y-axis
    coordinates.clear()


canvas.bind("<B1-Motion>", on_move)
upper_degree = 2
degree_slider = tk.Scale(root, from_=1, to=20, orient="horizontal", label="Degree", command=set_degree)
degree_slider.pack()
#create a horizontal frame to hold the buttons
frame = tk.Frame(root)
frame.pack()

#create the buttons
predict_button = tk.Button(frame, text="Predict", command=get_coordinates)
predict_button.pack(side=tk.LEFT)
draw_button = tk.Button(frame, text="Draw", command=draw_graph)
draw_button.pack(side=tk.LEFT)
clear_button = tk.Button(frame, text="Clear", command=clear_canvas)
clear_button.pack(side=tk.LEFT)

#create a text box to display the output
output_text = tk.Text(root, width=90, height=6, wrap=tk.WORD)
output_text.pack()

#redirect the output to the text box
sys.stdout = StdoutRedirector(output_text)

#create the up and down arrow buttons
down_arrow = tk.Button(frame, text="v", command=decrement_degree)
down_arrow.pack(side=tk.RIGHT)
up_arrow = tk.Button(frame, text="^", command=increment_degree)
up_arrow.pack(side=tk.RIGHT)
degree_slider.set(upper_degree)

canvas.create_line(0, rows*50/2, columns*50, rows*50/2, width=3) # x-axis
canvas.create_line(columns*50/2, 0, columns*50/2, rows*50, width=3) # y-axis


root.mainloop()