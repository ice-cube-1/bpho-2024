import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation, PillowWriter
import math

class Line():
    '''from a (partially empty) dataset, creates the points that should be plotted, possibly including
       the bounding parabola and local minmaxes for range/time'''
    def __init__(self, input_str: dict[str, str], minmax: int, bound: int) -> None:
        '''converts to floats, calculating values if required'''        
        self.g: float = float(input_str['g'])
        self.minmax: int = minmax
        self.bound: int = bound          
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
    
    def plot(self) -> list[tuple[float, float]]:
        '''return the path(s) of the lines, calculated either exactly or numerically'''
        paths = []
        for t in self.t:
            if bounce_verlet.get() != 1: 
                data: list[tuple[float, float]] = self.line(t)
            else: 
                data: list[tuple[float, float]] = self.bounceVerlet(t)
            paths.append(data)
            self.getRange(t)
            if self.bound == 1:
                self.boundParabola()
        return paths

    def boundParabola(self) -> None:
        '''plots the bounding parabola'''
        y: float = self.h
        x: float = 0
        data: list[tuple[float, float]] = []
        while y >= 0:
            x += 0.02
            y = (self.u**2/(2*self.g))-((self.g*x**2)/(2*self.u**2))+self.h
            data.append((x, y))
        plt.plot([i[0] for i in data], [i[1] for i in data])

    def print_info(self) -> None:
        '''outputs information about the graph'''
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, f"MinMax: {self.minmax}\n")
        for t in self.t:
            outval: dict[str, float] = {"t (rad)": t, "t (deg)": math.degrees(t), "U": self.u,
                                        "VX": math.cos(t)*self.u, "VY": math.sin(t)*self.u,
                                        "ToF": self.getRange(t)/(self.u*math.cos(t)), "Range": self.getRange(t),
                                        "Distance": self.distance(t), "Apogee xa": (self.u*math.cos(t))*(self.u*math.sin(t))/self.g,
                                        "Apogee ya": self.yfromx(t, (self.u*math.cos(t))*(self.u*math.sin(t))/self.g)}
            for i in outval:
                text_output.insert(tk.END, f"{i}: {round(outval[i], 3)}\n")
            if t >= math.asin(2*math.sqrt(2)/3) and self.minmax == 1:
                times = (((3*self.u)/(2*self.g))*(math.sin(t)+math.sqrt(math.sin(t)**2-(8/9))),
                         ((3*self.u)/(2*self.g))*(math.sin(t)-math.sqrt(math.sin(t)**2-(8/9))))
                for time in times:
                    x = self.u*time*math.cos(t)
                    y = self.yfromx(t, x)
                    plt.plot(x,y,marker="x")
                    text_output.insert(tk.END, f"Turning point t/rng: {x}, {y}\n")

    def line(self, t: float) -> list[tuple[float, float]]:
        '''calculates exact positions of 100 points (evenly spaced across range)'''
        data: list[tuple[float, float]] = []
        y: float = self.h
        x = 0
        for i in range(100):
            x += (self.getRange(t)/100)
            y = self.yfromx(t, x)
            data.append((x, y))
        return data

    def bounceVerlet(self, t: float) -> list[tuple[float,float]]:
        '''uses the verlet method to generate points (takes into account drag coefficient / velocity lost during bounces)'''
        n: int = 0
        nN: int = 0
        dt: float = 0.02
        x: list[float] = [0]
        y: list[float] = [self.h]
        vx: list[float] = [self.u*math.sin(t)]
        vy: list[float] = [self.u*math.cos(t)]
        while nN <= self.N:
            v = math.sqrt(vx[n]**2+vy[n]**2)
            ax = -(vx[n]/v)*self.k*v**2
            ay = -self.g-(vx[n]/v)*self.k*v**2
            x.append(x[n] + vx[n]*dt + 0.5*ax*dt**2)
            y.append(y[n] + vy[n]*dt + 0.5*ay*dt**2)
            aax = -(vx[n]/v)*self.k*v**2
            aay = -self.g-(vy[n]/v)*self.k*v**2
            vx.append(vx[n] + 0.5*(ax + aax)*dt)
            vy.append(vy[n] + 0.5*(ay + aay)*dt)
            if y[n+1] < 0: 
                y[n+1] = 0
                vy[n+1] = -self.c*vy[n+1]
                nN += 1
            n += 1
        return [(x[i], y[i]) for i in range(n+1)]
    
    def distance(self, t: float) -> float:
        '''calculates distance travelled by the projectile'''
        a: float = (self.u**2)/(self.g*(1+(math.tan(t))**2))
        b: float = math.tan(t)
        c: float = math.tan(t)-self.g*self.getRange(t)*(1+(math.tan(t))**2)/(self.u**2)
        return a*(self.z_func(b)-self.z_func(c))
    
    def tFromU(self, X: float, Y: float) -> tuple[float, float]:
        '''calculates the angle for a given speed to pass through X/Y'''
        a: float = self.g*X**2/(2*self.u**2)
        b: float = -X
        c: float = Y-self.h+((self.g*X**2)/(2*self.u**2))
        return (math.atan((-b+math.sqrt(b**2-4*a*c))/(2*a)), math.atan((-b-math.sqrt(b**2-4*a*c))/(2*a)))

    def getRange(self, t: float) -> float: 
        '''calculates range of projectile'''
        return ((self.u*math.sin(t)+math.sqrt(2*self.h*self.g+(self.u*math.sin(t))**2))/self.g)*self.u*math.cos(t)
    
    def yfromx(self, t: float, x: float) -> float: 
        '''calculates the y coordinate for a given x coordinate'''
        return round(x*math.tan(t)-(self.g*x**2)/(2*self.u**2*math.cos(t)**2)+self.h, 5)
    
    def minU(self, X: float, Y: float): 
        '''calculates the minimum speed to pass through X/Y'''
        return math.sqrt(self.g)*math.sqrt(Y+math.sqrt(X**2+Y**2))
    
    def maxRange(self): 
        '''calculates maximum range of projectile'''
        return math.asin(1/(math.sqrt(2+((2*self.g*self.h)/self.u**2))))
    
    def z_func(self, z: float) -> float: 
        '''util function for calculating distance'''
        return 0.5*math.log(abs(math.sqrt(1+z**2)+z))+0.5*z*math.sqrt(1+z**2)


def save_line(): 
    '''saves the line, now modifying a new one'''
    lines.append(Line(input_str, minmax.get(), bound_value.get()))

def reset_lines(): 
    '''removes all but the current (modifiable) line'''
    [lines.remove(lines[0]) for i in lines[:-1]]


def update_plot():
    '''either plays an animation or draws the line'''
    global ani
    for i in input_str: 
        input_str[i] = entry_labels[i][1].get()
    lines[-1] = Line(input_str, minmax.get(), bound_value.get())
    plt.clf()
    for line in lines:
        line.print_info()
        paths = line.plot()
        if animate_value.get() == 0:
            for path in paths:
                plt.plot([i[0] for i in path], [i[1] for i in path])
        else:
            frames = max(len(line.plot()) for line in lines)
            ani = FuncAnimation(fig, animate, frames=frames, interval=10, repeat=False)
    canvas.draw()

def animate(frame):
    '''animates the graph'''
    plt.clf()
    for line in lines:
        paths = line.plot()
        if paths:
            num_points = len(paths)
            if frame < num_points:
                xdata, ydata = [i[0] for i in paths[:frame+1]], [i[1] for i in paths[:frame+1]]
                plt.plot(xdata, ydata)
                plt.scatter(xdata[-1], ydata[-1], c='r')

def save():
    '''saves animation / png depending whether they last viewed an animation or still graph'''
    global ani
    if animate_value.get() == 1:
        ani.save("anim.gif", writer=PillowWriter(fps=20))
    plt.savefig("plot.png")

def toggle_inputs():
    '''hides any inputs that are not required for the radio the user selected'''
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
        pack(['X','Y','u'])
    if bounce_verlet.get() == 1:
        pack(['N','k','c'])
def pack(topack: list[str]):
    for i in topack:
        entry_labels[i][0].pack(padx=10)
        entry_labels[i][1].pack(padx=10)

input_str: dict[str, str] = {'g': '10', 't': '45', 'u': '2', 'h': '0', 'X': '', 'Y': '', 'N': '', 'k': '', 'c': ''}
ani = None # animation
# for the labels in the gui
input_info: dict[str, str] = {'g': 'Gravity (g)', 't': 'theta (t, deg)', 'u': 'initial velocity (u)', 'h': 'initial height', 'X': 'X intersect', 
                              'Y': 'Y intersect', 'N': 'number of bounces', 'k': 'air resistance', 'c': 'velocity loss / bounce'}
root = tk.Tk()
root.title("Projectile Motion Plot")
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# gui frames / buttons etc
frame_left = tk.Frame(root)
frame_center = tk.Frame(root)
frame_right = tk.Frame(root)
mainButtons = tk.Frame(frame_left)
radio = tk.Frame(frame_left, bd=2, relief=tk.RAISED)
checkboxes = tk.Frame(frame_left, bd=2, relief=tk.RAISED)
inputs = tk.Frame(frame_center, bd=2, relief=tk.RAISED)
info = tk.Frame(frame_right, bd=2, relief=tk.RAISED)
frame_left.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")
frame_center.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")
frame_right.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")
mainButtons.pack(side=tk.TOP, pady=10, anchor="n")
radio.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
checkboxes.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
inputs.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
info.pack(side=tk.TOP, padx=10, pady=10)

options = tk.IntVar(value=1)
lines: list[Line] = [Line(input_str, 0, 0)]
entry_labels: dict[str, list] = {}
label = tk.Label(radio, text=f'Inputs for graph:', justify=tk.LEFT, font=("TkDefaultFont",12)).pack(anchor="w", padx=10, pady=5)
r1 = tk.Radiobutton(radio, text="Path with angle / velocity", value=1, variable=options, command=toggle_inputs).pack(anchor="w")
r2 = tk.Radiobutton(radio, text="Minimum velocity to pass through XY", value=2, variable=options, command=toggle_inputs).pack(anchor="w")
r3 = tk.Radiobutton(radio, text="Maximum range for a given speed", value=3, variable=options, command=toggle_inputs).pack(anchor="w")
r4 = tk.Radiobutton(radio, text="Angle to pass through XY at a given speed", value=4, variable=options, command=toggle_inputs).pack(anchor="w")

label = tk.Label(checkboxes, text=f'Extra features:', justify=tk.LEFT, font=("TkDefaultFont",12)).pack(anchor="w", padx=10, pady=5)
minmax = tk.IntVar()
checkbutton = tk.Checkbutton(checkboxes, text="Show local minmax (if applicable)", variable=minmax, onvalue=1, offvalue=0, bg=root.cget("bg")).pack(anchor="w")
bounce_verlet = tk.IntVar()
bounce_verlet_checkbox = tk.Checkbutton(checkboxes, text="Bounce Verlet", variable=bounce_verlet, onvalue=1, offvalue=0, command=toggle_inputs, bg=root.cget("bg")).pack(anchor="w")
bound_value = tk.IntVar()
bound_checkbox = tk.Checkbutton(checkboxes, text="Show bounding parabola", variable=bound_value, onvalue=1, offvalue=0, bg=root.cget("bg")).pack(anchor="w")
animate_value = tk.IntVar()
anim_checkbox = tk.Checkbutton(checkboxes, text="Show animation", variable=animate_value, onvalue=1, offvalue=0, bg=root.cget("bg")).pack(anchor="w")

update_button = tk.Button(mainButtons, text="Update Plot", command=update_plot, bg=root.cget("bg"), justify=tk.CENTER, width=35).pack(anchor="center", padx=10, pady=5)
save_button = tk.Button(mainButtons, text="Save Line", command=save_line, bg=root.cget("bg"), justify=tk.CENTER, width=35).pack(anchor="center", padx=10, pady=5)
reset_button = tk.Button(mainButtons, text="Reset Lines", command=reset_lines, bg=root.cget("bg"), justify=tk.CENTER,width=35).pack(anchor="center", padx=10, pady=5)
save_file = tk.Button(mainButtons, text="Save as PNG / GIF", command=save, bg=root.cget("bg"), justify=tk.CENTER, width=35).pack(anchor="center", padx=10, pady=5)

label = tk.Label(inputs, text=f'Inputs:', justify=tk.LEFT, font=("TkDefaultFont",12)).pack(anchor="w", padx=10, pady=5)
for i in input_str:
    label = tk.Label(inputs, text=f'{input_info[i]}:', justify=tk.LEFT)
    label.pack(anchor="w", padx=10)
    entry = tk.Entry(inputs, bg=root.cget("bg"))
    entry.insert(0, str(input_str[i]))
    entry.pack(anchor="w", padx=10)
    entry_labels[i] = [label, entry]
bottom_padding = tk.Label(inputs, text="", height=1)
bottom_padding.pack(side=tk.BOTTOM, fill=tk.X)
label = tk.Label(info, text=f'Graph info:', justify=tk.LEFT, font=("TkDefaultFont",12)).pack(anchor="w", padx=10, pady=5)
text_output = tk.Text(info, bg=root.cget("bg"), font=("TkDefaultFont",10), width=20, height=25)
text_output.pack(padx=10,pady=5)


root.mainloop()
