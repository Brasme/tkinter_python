import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import threading

class MyWindow:
    def __init__(self,period_ms=20):
        self.canvas=None
        self.period_ms = period_ms 
        self.do_run = False
        self.window = tk.Tk()
        self.window.title("Graph Display")
        # self.event = threading.Event()

        # Create a button to plot the graph
        self.plot_button1 = tk.Button(self.window, text="Plot Graph", command=self.plot_graph)
        self.plot_button2 = tk.Button(self.window, text="Start update", command=self.start_timer)
        self.plot_button3 = tk.Button(self.window, text="Stop update", command=self.stop_timer)
        self.value_entry = tk.Entry(self.window)
        self.value_entry.insert(0,str(self.period_ms))
        self.value_entry.bind("<KeyRelease>", self.on_entry_change)
        self.plot_button1.grid(row=0, column=0)
        self.plot_button2.grid(row=0, column=1)
        self.plot_button3.grid(row=0, column=2)
        self.value_entry.grid(row=0, column=3)
        # self.plot_button1.pack(side=tk.LEFT)
        # self.plot_button2.pack(side=tk.LEFT)
        # self.plot_button3.pack(side=tk.LEFT)
        
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(1, 1, 1)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=4)
        # self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


        self.event_count=0

    def on_entry_change(self,event):
        value = self.value_entry.get()
        print("Value changed to:", value)        
        try:
            ms=int(value)
        except:
            ms=self.period_ms    
        self.period_ms = ms

    # Define the function to plot
    def plot_graph(self):
        i = self.event_count/(4*np.pi)
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(i+x)
        self.plot.cla()
        self.plot.plot(x, y)
        self.canvas.draw()
                
    def start_timer(self):
        if self.do_run:
            print("Already running!")
        self.do_run = True
        print("Starting!")
        self.window.after(self.period_ms, self.do_timer)        
        
    def stop_timer(self):
        if not self.do_run:
            print("Not running!")
        print("Stopping!")
        self.do_run = False
        
    def do_timer(self):
        if not self.do_run:
            print("Timer stopped!")
            return
        self.event_count +=1
        self.plot_graph()
        # print(f"Timer called {self.event_count}!")
        self.window.after(self.period_ms, self.do_timer)
        
    def run(self):
        self.window.mainloop()

MyWindow().run()
