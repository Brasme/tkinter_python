import tkinter as tk
from tkinter import messagebox
import time, threading 
import math
import copy

class Complex():
    def __init__(self, re, im):
        self.re = re
        self.im = im
    
    @staticmethod
    def from_type(v):
        if isinstance(v, (list, tuple)):
            if len(v)>=2:
                return Complex(v[0],v[1])
            elif len(v)>0:
                return Complex(v[0],0)
            else:
                return Complex(0,0)
        if isinstance(v,Complex):
            return Complex(v.re,v.im)
        return Complex(v,0)        
    
    def __str__(self):
        return "{}+{}i".format(self.re, self.im) 
    
    def __add__(self,value):
        v=Complex.from_type(value)        
        return Complex(self.re+v.re,self.im+v.im)

    def __sub__(self,value):
        v=Complex.from_type(value)        
        return Complex(self.re-v.re,self.im-v.im)

    def __mul__(self,value):
        v=Complex.from_type(value)        
        return Complex(self.re*value.re-self.im*value.im,self.re*value.im+self.im*value.re)        
        
    def __div__(self,value):
        v=Complex.from_type(value)        
        d=(v.re*v.re+v.im+v.im)
        if d==0:
            d=1.0e-255
        return Complex((self.re*v.re+self.im*v.im)/d,(self.im*v.re-self.re*v.im)/d)        
        
    def length(self):
        v=self.re**2 + self.im**2
        if v==0:
            return 0
        return math.sqrt(v)
    
    def distance(self,other):
        return (self-other).length()
    

def clip_to_boundary(point,geometry,old=None):
    p=Complex.from_type(point)
    g=Complex.from_type(geometry)
    if old == None:
        o=Complex(geometry.x/2,geometry.y/2)
    else:
        o=Complex.from_type(old)
        if o.re==0 and o.im==0:
            o=Complex(geometry.x/2,geometry.y/2)
    dp=p-o
    if abs(dp.re)>abs(dp.im):
        if p.re<o.re:
            v = Complex(0,p.im)
        else:
            v = Complex(g.re-1,p.im)
    else:
        if p.im<o.im:
            v = Complex(p.re,0)
        else:
            v = Complex(g.re,g.im-1)
    if v.re<0:
        v.re=0
    if v.re>=g.re:
        v.re=g.re-1
    if v.im<0:
        v.im=0
    if v.im>=g.im:
        v.im=g.im-1
    return v



class Event(object):
    pass

def no_func():
    return
    
class App(object):
    def __init__(self,width=1024,height=768):        
        self.callbacks = []
        self.on_exit = no_func
        self._win=tk.Tk()
        # self._win.geometry('1024x512')
        self._canvas = tk.Canvas(self._win,width=width,height=height)
        self._canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self._win.title("Test Application")
        self._win.configure(bg="gray")
        self._state="out"
        self.mousePos=Complex(0,0)
        self._mousePos=Complex(0,0) # Previous/old point
        self.in_count=0

        self._win.bind('<Motion>',self._on_mouse_motion)
        self._win.bind("<Enter>", self._on_mouse_enter)
        self._win.bind("<Leave>", self._on_mouse_leave)
        self._win.protocol("WM_DELETE_WINDOW", self._on_close)

    def __str__(self):
        p1=Complex.from_type(self._win.winfo_pointerxy()) 
        p2=Complex(self._win.winfo_rootx(),self._win.winfo_rooty())
        return '{0:<3} : {1:<12} : {2:<12} : {3:<12}'.format(self._state,str(self.mousePos),str(p1),str(p2))
    
    def _on_notify(self,info):
        event = Event()
        event.source = self
        event.info = info
        for func in self.callbacks:
            func(event)

    def _on_mouse_motion(self,event):
        self._mousePos = copy.deepcopy(self.mousePos)
        self.mousePos = Complex(event.x, event.y)
        self._on_notify("motion")
        self._draw()
        self.in_count += 1

    def _on_mouse_enter(self,event):
        self._state="in"
        self._on_notify("enter")

    def _on_mouse_leave(self,event):
        p = copy.deepcopy(self.mousePos)
        o = copy.deepcopy(self._mousePos)
        self._mousePos=copy.deepcopy(self.mousePos)
        g = Complex(self._win.winfo_width(),self._win.winfo_height())
        self.mousePos=clip_to_boundary(p,g,o)
        self._state="out" 
        self._on_notify("leave")
        self._draw()
        self.in_count=-1
    
    def _draw(self):
        green = "#476042"
        # d = self.mousePos.distance(self._mousePos)
        # x, y = (self.mousePos.re - 1), (self.mousePos.im - 1)
        # self._canvas.create_oval(x, y, x+2, y+2, fill=green)
        if self.in_count<=0:
            return
        p0=copy.deepcopy(self.mousePos)
        p1=copy.deepcopy(self._mousePos)
        if p1.re<p0.re:
            v=p0.re
            p0.re=p1.re
            p1.re=v
        if p1.im<p0.im:
            v=p0.im
            p0.im=p1.im
            p1.im=v        
        self._canvas.create_oval(p0.re-1, p0.im-1, p1.re+1, p1.im+1, fill=green)

    def _on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.on_exit()
            self._win.destroy()

    def run(self):
        self._win.mainloop()


class Timer(object):
    def __init__(self,period=1.0):
        self.callbacks = []
        self.period=period
        self.time=time.ctime()
        self._timer=threading.Timer(self.period,self._on_timer_event)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.cancel()

    def __str__(self):
        return self.time

    def _on_timer_event(self):
        self.time=time.ctime()
        self._on_notify("timer")
        self._timer=threading.Timer(self.period,self._on_timer_event)
        self._timer.start()
    
    def _on_notify(self,info):
        event = Event()
        event.source = self
        event.info = info
        for func in self.callbacks:
            func(event)


    
class Test(object):
    def __init__(self):
        self._app = App()
        self._t = Timer(1.0)
        self._t.callbacks.append(self._info)
        self._t.start()
        self._app.callbacks.append(self._info)
        self._app.on_exit=self._on_exit
        self._app.run()
    
    def _info(self,event):
        print(f"{self._t}: {event.info:<10} : {self._app}") # event.source is the timer / app so we do not print that

    def _on_exit(self):
        self._t.stop()

        

    

if __name__ == "__main__":
    Test()    