import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class Line():
    def __init__(self, input_str: dict[str, str]) -> None:
        print(input_str)
        self.g: float = float(input_str['g'])
        self.k: float = 0 if input_str['k'] == '' else float(input_str['k'])
        self.N: float = 0 if input_str['N'] == '' else float(input_str['N'])
        self.c: float = 0 if input_str['c'] == '' else float(input_str['c'])
        self.h: float = 0 if input_str['h'] == '' else float(input_str['h'])
        if input_str['t'] == '':
            if input_str['u'] == '':
                self.u: float = self.minU(float(input_str['X']), float(input_str['Y']))
                self.t: tuple = self.tFromU(float(input_str['X']), float(input_str['Y']))
            else:
                self.u: float = float(input_str['u'])
                if input_str['X'] == '': self.t: tuple = (self.maxRange(),)
                else: self.t: tuple = self.tFromU(float(input_str['X']), float(input_str['Y']))
        else: self.t: tuple = (math.radians(float(input_str['t'])),); self.u: float = float(input_str['u'])

    def plot(self) -> None:
        for t in self.t:
            if self.N == 0 and self.k == 0: data: list[tuple[float, float]] = self.line(t)
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

    def print_info(self, showMinMax=False) -> None:
        for t in self.t:
            outval: dict[str, float] = {"t (rad)": t, "t (deg)": math.degrees(t), "U": self.u,
                                        "VX": math.cos(t)*self.u, "VY": math.sin(t)*self.u,
                                        "ToF": self.getRange(t)/(self.u*math.cos(t)), "Range": self.getRange(t),
                                        "Distance": self.distance(t)}
            [print(i, round(outval[i], 3)) for i in outval]
            if t >= math.asin(2*math.sqrt(2)/3) and showMinMax == True:
                times = (((3*self.u)/(2*self.g))*(math.sin(t)+math.sqrt(math.sin(t)**2-(8/9))),
                         ((3*self.u)/(2*self.g))*(math.sin(t)-math.sqrt(math.sin(t)**2-(8/9))))
                for t in times:
                    x = self.u*t*math.cos(t); y = self.yfromx(t, x)
                    plt.plot(x, y, marker="x"); print("Turning point t/rng:", x, y)

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
            x.append(x[n] + vx[n]*dt + 0.5*ax*dt**2)
            y.append(y[n] + vy[n]*dt + 0.5*ay*dt**2)
            aax = -(vx[n]/v)*self.k*v**2; aay = -self.g-(vy[n]/v)*self.k*v**2
            vx.append(vx[n] + 0.5*(ax + aax)*dt)
            vy.append(vy[n] + 0.5*(ay + aay)*dt)
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

def save_line(): lines.append(Line(input_str))
def reset_lines(): [lines.remove(lines[0]) for i in lines[:-1]]
def update_plot():
    for i in input_str: input_str[i] = entry_labels[i][1].get()
    lines[-1] = Line(input_str)
    plt.clf()
    for i in lines: i.plot()
    canvas.draw()


input_str: dict[str, str] = {'g': '10', 't': '45', 'u': '2', 'h': '0', 'X': '', 'Y': '', 'N': '', 'k': '', 'c': ''}
lines: list[Line] = [Line(input_str)]; entry_labels: dict[str, list] = {}
root = tk.Tk()
root.title("Projectile Motion Plot")
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
for i in input_str:
    entry_labels[i] = [tk.Label(root, text=f'{i}:').pack(), tk.Entry(root)]
    entry_labels[i][1].insert(0, str(input_str[i])); entry_labels[i][1].pack()
update_button = tk.Button(root, text="Update Plot", command=update_plot).pack()
save_button = tk.Button(root, text="Save Line", command=save_line).pack()
reset_button = tk.Button(root, text="Reset Lines", command=reset_lines).pack()
root.mainloop()
