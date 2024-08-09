from sys import argv
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class Line():
    def __init__(self, input_str: dict[str, str], minmax: int) -> None:
        self.g: float = float(input_str['g']); self.minmax: int = minmax            
        self.k: float = 0 if input_str['k'] == '' else float(input_str['k'])
        self.N: float = 0 if input_str['N'] == '' else float(input_str['N'])
        self.c: float = 0 if input_str['c'] == '' else float(input_str['c'])
        self.h: float = 0 if input_str['h'] == '' else float(input_str['h'])
        if options.get() == 1: 
            self.t: tuple = (math.radians(float(input_str['t'])),)
            self.u: float = float(input_str['u'])
        elif options.get() == 2: 
            self.u = self.minU(float(input_str['X']), float(input_str['Y']))
            self.t: tuple = self.tFromU(float(input_str['X']), float(input_str['Y']))
        elif options.get() == 3: 
            self.u = float(input_str['u'])
            self.t: tuple = (self.maxRange(),)
        else: 
            self.u = float(input_str['u'])
            self.t: tuple = self.tFromU(float(input_str['X']), float(input_str['Y']))

    def plot(self) -> None:
        for t in self.t:
            if bounce_verlet.get() != 1: data: list[tuple[float, float]] = self.line(t)
            else: data: list[tuple[float, float]] = self.bounceVerlet(t)
            self.getRange(t)
            plt.plot([i[0] for i in data], [i[1] for i in data])

    def bound(self) -> None:
        y: float = self.h; x: float = 0
        data: list[tuple[float, float]] = []
        while y >= 0:
            x += 0.02
            y = (self.u**2/(2*self.g))-((self.g*x**2)/(2*self.u**2))+self.h
            data.append((x, y))
        plt.plot([i[0] for i in data], [i[1] for i in data])

    def print_info(self) -> None:
        print(self.minmax)
        for t in self.t:
            outval: dict[str, float] = {"t (rad)": t, "t (deg)": math.degrees(t), "U": self.u,
                                        "VX": math.cos(t)*self.u, "VY": math.sin(t)*self.u,
                                        "ToF": self.getRange(t)/(self.u*math.cos(t)), "Range": self.getRange(t),
                                        "Distance": self.distance(t)}
            [print(i, round(outval[i], 3)) for i in outval]
            if t >= math.asin(2*math.sqrt(2)/3) and self.minmax == 1:
                times = (((3*self.u)/(2*self.g))*(math.sin(t)+math.sqrt(math.sin(t)**2-(8/9))),
                         ((3*self.u)/(2*self.g))*(math.sin(t)-math.sqrt(math.sin(t)**2-(8/9))))
                for time in times:
                    x = self.u*time*math.cos(t); y = self.yfromx(t, x)
                    plt.plot(x,y,marker="x"); print("Turning point t/rng:", x, y)

    def line(self, t: float) -> list[tuple[float, float]]:
        data: list[tuple[float, float]] = []
        y: float = self.h; x = 0
        for i in range(100):
            x += (self.getRange(t)/100)
            y = self.yfromx(t, x)
            data.append((x, y))
        return data

    def bounceVerlet(self, t: float) -> list[tuple[float,float]]:
        n: int = 0; nN: int = 0; dt: float = 0.02
        x: list[float] = [0]; y: list[float] = [self.h]
        vx: list[float] = [self.u*math.sin(t)]; vy: list[float] = [self.u*math.cos(t)]
        while nN <= self.N:
            v = math.sqrt(vx[n]**2+vy[n]**2)
            ax = -(vx[n]/v)*self.k*v**2; ay = -self.g-(vx[n]/v)*self.k*v**2
            x.append(x[n] + vx[n]*dt + 0.5*ax*dt**2); y.append(y[n] + vy[n]*dt + 0.5*ay*dt**2)
            aax = -(vx[n]/v)*self.k*v**2; aay = -self.g-(vy[n]/v)*self.k*v**2
            vx.append(vx[n] + 0.5*(ax + aax)*dt); vy.append(vy[n] + 0.5*(ay + aay)*dt)
            if y[n+1] < 0: y[n+1] = 0; vy[n+1] = -self.c*vy[n+1]; nN += 1
            n += 1
        return [(x[i], y[i]) for i in range(n+1)]
 
    def distance(self, t: float) -> float:
        a: float = (self.u**2)/(self.g*(1+(math.tan(t))**2))
        b: float = math.tan(t)
        c: float = math.tan(t)-self.g*self.getRange(t)*(1+(math.tan(t))**2)/(self.u**2)
        return a*(self.z_func(b)-self.z_func(c))
    
    def tFromU(self, X: float, Y: float) -> tuple[float, float]:
        a: float = self.g*X**2/(2*self.u**2)
        b: float = -X
        c: float = Y-self.h+((self.g*X**2)/(2*self.u**2))
        return (math.atan((-b+math.sqrt(b**2-4*a*c))/(2*a)), math.atan((-b-math.sqrt(b**2-4*a*c))/(2*a)))

    def getRange(self, t: float) -> float: return ((self.u*math.sin(t)+math.sqrt(2*self.h*self.g+(self.u*math.sin(t))**2))/self.g)*self.u*math.cos(t)
    def yfromx(self, t: float, x: float) -> float: return round(x*math.tan(t)-(self.g*x**2)/(2*self.u**2*math.cos(t)**2)+self.h, 5)
    def minU(self, X: float, Y: float): return math.sqrt(self.g)*math.sqrt(Y+math.sqrt(X**2+Y**2))
    def maxRange(self): return math.asin(1/(math.sqrt(2+((2*self.g*self.h)/self.u**2))))
    def z_func(self, z: float) -> float: return 0.5*math.log(abs(math.sqrt(1+z**2)+z))+0.5*z*math.sqrt(1+z**2)

def save_line(): lines.append(Line(input_str, minmax.get()))
def reset_lines(): [lines.remove(lines[0]) for i in lines[:-1]]
def update_plot():
    for i in input_str: input_str[i] = entry_labels[i][1].get()
    lines[-1] = Line(input_str, minmax.get())
    plt.clf()
    for i in lines: i.plot(); i.print_info()
    canvas.draw()

def toggle_inputs(*args):
    # First, hide all widgets
    for key in input_str.keys():
        entry_labels[key][0].pack_forget()
        entry_labels[key][1].pack_forget()
    pack(['g','h'])
    if options.get() == 1:
        pack(['t','u'])
    elif options.get() == 2:
        pack(['X','Y'])
    elif options.get() == 3:
        pack(['u'])
    elif options.get() == 4:
        pack(['X','Y','t','u'])
    if bounce_verlet.get() == 1:
        pack(['N','k','c'])
def pack(topack: list[str]):
    for i in topack:
        entry_labels[i][0].pack()
        entry_labels[i][1].pack()
        
input_str: dict[str, str] = {'g': '10', 't': '45', 'u': '2', 'h': '0', 'X': '', 'Y': '', 'N': '', 'k': '', 'c': ''}
root = tk.Tk()
root.title("Projectile Motion Plot")
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
options = tk.IntVar(value=1)
lines: list[Line] = [Line(input_str, 0)]; entry_labels: dict[str, list] = {}
r1 = tk.Radiobutton(root, text="Path with angle / velocity", value=1, variable=options, command=lambda: toggle_inputs(options.get())).pack()
r2 = tk.Radiobutton(root, text="Minimum velocity to pass through XY", value=2, variable=options, command=lambda: toggle_inputs(options.get())).pack()
r3 = tk.Radiobutton(root, text="Maximum range for a given speed", value=3, variable=options, command=lambda: toggle_inputs(options.get())).pack()
r4 = tk.Radiobutton(root, text="Angle to pass through XY at a given speed", value=4, variable=options, command=lambda: toggle_inputs(options.get())).pack()

for i in input_str:
    label = tk.Label(root, text=f'{i}:')
    label.pack()
    entry = tk.Entry(root)
    entry.insert(0, str(input_str[i]))
    entry.pack()
    entry_labels[i] = [label, entry]

minmax = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Show local minmax (if applicable)", variable=minmax, onvalue=1, offvalue=0).pack()
update_button = tk.Button(root, text="Update Plot", command=update_plot).pack()
save_button = tk.Button(root, text="Save Line", command=save_line).pack()
reset_button = tk.Button(root, text="Reset Lines", command=reset_lines).pack()
bounce_verlet = tk.IntVar()
bounce_verlet_checkbox = tk.Checkbutton(root, text="Bounce Verlet", variable=bounce_verlet, onvalue=1, offvalue=0, command=toggle_inputs)
bounce_verlet_checkbox.pack()

root.mainloop()
