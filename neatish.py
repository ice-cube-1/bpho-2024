import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


def yfromx(t: float, g: float, x: float, h: float, u: float) -> float: return round(x*math.tan(t)-(g*x**2)/(2*u**2*math.cos(t)**2)+h, 5)


def tFromU(u: float, X: float, Y: float, h: float, g: float) -> tuple[float, float]:
    a: float = g*X**2/(2*u**2)
    b: float = -X
    c: float = Y-h+((g*X**2)/(2*u**2))
    return (math.atan((-b+math.sqrt(b**2-4*a*c))/(2*a)),
            math.atan((-b-math.sqrt(b**2-4*a*c))/(2*a)))


def minU(g, X, Y): return math.sqrt(g)*math.sqrt(Y+math.sqrt(X**2+Y**2))


def maxRange(g, h, u): return math.asin(1/(math.sqrt(2+((2*g*h)/u**2))))


def z_func(z: float) -> float: return 0.5*math.log(abs(math.sqrt(1+z**2)+z))+0.5*z*math.sqrt(1+z**2)


def distance(t: float, u: float, g: float, r: float) -> float:
    a: float = (u**2)/(g*(1+(math.tan(t))**2))
    b: float = math.tan(t)
    c: float = math.tan(t)-g*r*(1+(math.tan(t))**2)/(u**2)
    return a*(z_func(b)-z_func(c))


def bounceVerlet(t: float, u: float, N: float, c: float, k: float, h: float, g: float) -> list[tuple[float, float]]:
    n: int = 0; nN: int = 0; dt: float = 0.02
    x: list[float] = [0]; y: list[float] = [h]
    vx: list[float] = [u*math.sin(t)]; vy: list[float] = [u*math.cos(t)]
    while nN <= N:
        v = math.sqrt(vx[n]**2+vy[n]**2)
        ax = -(vx[n]/v)*k*v**2; ay = -g-(vx[n]/v)*k*v**2
        x.append(x[n] + vx[n]*dt + 0.5*ax*dt**2)
        y.append(y[n] + vy[n]*dt + 0.5*ay*dt**2)
        aax = -(vx[n]/v)*k*v**2; aay = -g-(vy[n]/v)*k*v**2
        vx.append(vx[n] + 0.5*(ax + aax)*dt)
        vy.append(vy[n] + 0.5*(ay + aay)*dt)
        if y[n+1] < 0:
            y[n+1] = 0
            vy[n+1] = -c*vy[n+1]
            nN += 1
        n += 1
    return [(x[i], y[i]) for i in range(n+1)]


def line(t: float, u: float, rng: float, h: float, g: float) -> list[tuple[float, float]]:
    data = []
    y = h
    x = 0
    while y >= 0:
        x += (rng/100)
        y = yfromx(t, g, x, h, u)
        data.append((x, y))
    return data


class Line():
    def __init__(self, input_str: dict[str, str]) -> None:
        self.g: float = float(input_str['g'])
        self.k: float = 0 if input_str['k'] == '' else float(input_str['k'])
        self.N: float = 0 if input_str['N'] == '' else float(input_str['N'])
        self.c: float = 0 if input_str['c'] == '' else float(input_str['c'])
        self.h: float = 0 if input_str['h'] == '' else float(input_str['h'])
        if input_str['t'] == '':
            if input_str['u'] == '':
                self.u: float = minU(self.g, float(input_str['X']), float(input_str['Y']))
                self.t: tuple = tFromU(self.u, float(input_str['X']), float(input_str['Y']), self.h, self.g)
            else:
                self.u: float = float(input_str['u'])
                if input_str['X'] == '': self.t: tuple = (maxRange(self.g, self.h, self.u),)
                else: self.t: tuple = tFromU(self.u, float(input_str['X']), float(input_str['Y']), self.h, self.g)
        else: 
            self.t: tuple = (float(input_str['t']),)
            self.u: float = float(input_str['u'])

    def plot(self) -> None:
        for t in self.t:
            rng: float = ((self.u*math.sin(t)+math.sqrt(2*self.h*self.g + (self.u*math.sin(t))**2))/self.g)*self.u*math.cos(t)
            if self.N == 0 and self.k == 0: data: list[tuple[float, float]] = line(t, self.u, rng, self.h, self.g)
            else: data: list[tuple[float, float]] = bounceVerlet(t, self.u, self.N, self.c, self.k, self.h, self.g)
            plt.plot([i[0] for i in data], [i[1] for i in data])

    def bound(self) -> None:
        y: float = self.h
        x: float = 0
        data: list[tuple[float, float]] = []
        while y >= 0:
            x += 0.02
            y = (self.u**2/(2*self.g))-((self.g*x**2)/(2*self.u**2))+self.h
            data.append((x, y))
        plt.plot([i[0] for i in data], [i[1] for i in data])

    def print_info(self, showMinMax=False) -> None:
        for t in self.t:
            rng: float = ((self.u*math.sin(t)+math.sqrt(2*self.h*self.g + (self.u*math.sin(t))**2))/self.g)*self.u*math.cos(t)
            outval: dict[str, float] = {"t (rad)": t,
                                        "t (deg)": math.degrees(t),
                                        "U": self.u,
                                        "VX": math.cos(t)*self.u,
                                        "VY": math.sin(t)*self.u,
                                        "ToF": rng/(self.u*math.cos(t)),
                                        "Range": rng,
                                        "Distance": distance(t, self.u, self.g, rng)}
            [print(i, round(outval[i], 3)) for i in outval]
            if t >= math.asin(2*math.sqrt(2)/3) and showMinMax == True:
                times = (((3*self.u)/(2*self.g))*(math.sin(t)+math.sqrt(math.sin(t)**2-(8/9))),
                         ((3*self.u)/(2*self.g))*(math.sin(t)-math.sqrt(math.sin(t)**2-(8/9))))
                for t in times:
                    print(t)
                    x = self.u*t*math.cos(t)
                    y = yfromx(t, self.g, x, self.h, self.u)
                    plt.plot(x, y, marker="x")
                    print("Turning point t/rng:", x, y)


def update_plot():
    for i in input_str: input_str[i] = entry_labels[i][1].get()
    lines[-1] = Line(input_str)
    plt.clf()
    for i in lines: i.plot()
    canvas.draw()


def save_line(): lines.append(Line(input_str))


def reset_lines(): [lines.remove(lines[0]) for i in lines[:-1]]


input_str: dict[str, str] = {'g': '10', 't': '45', 'u': '2', 'h': '0', 'X': '', 'Y': '', 'N': '', 'k': '', 'c': ''}
lines: list[Line] = [Line(input_str)]
entry_labels: dict[str, list] = {}

root = tk.Tk()
root.title("Projectile Motion Plot")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

for i in input_str:
    entry_labels[i] = [tk.Label(root, text=f'{i}:').pack(), tk.Entry(root)]
    entry_labels[i][1].insert(0, str(input_str[i]))
    entry_labels[i][1].pack()

update_button = tk.Button(root, text="Update Plot", command=update_plot).pack()
save_button = tk.Button(root, text="Save Line", command=save_line).pack()
reset_button = tk.Button(root, text="Reset Lines", command=reset_lines).pack()
root.mainloop()
