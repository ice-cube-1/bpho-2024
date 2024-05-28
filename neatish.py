import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

g = 10
t = 45
lines = [{'g': g, 't': t}]

def yfromx(theta,g,x,h,u):
    return round(x*math.tan(theta)-(g*x**2)/(2*u**2*math.cos(theta)**2)+h,5)

def thetaFromU(u,X,Y,h):
    a=g*X**2/(2*u**2)
    b=-X
    c=Y-h+((g*X**2)/(2*u**2))
    return (math.atan((-b+math.sqrt(b**2-4*a*c))/(2*a)),
            math.atan((-b-math.sqrt(b**2-4*a*c))/(2*a)))

def minU(g,X,Y):
    return math.sqrt(g)*math.sqrt(Y+math.sqrt(X**2+Y**2))

def maxRange(g,h,u):
    return math.asin(1/(math.sqrt(2+((2*g*h)/u**2))))

def z_func(z):
    return 0.5*math.log(abs(math.sqrt(1+z**2)+z))+0.5*z*math.sqrt(1+z**2)

def distance(theta, u, g, r):
    a = (u**2)/(g*(1+(math.tan(theta))**2))
    b = math.tan(theta)
    c = math.tan(theta)-g*r*(1+(math.tan(theta))**2)/(u**2)
    return a*( z_func(b)-z_func(c))

def bounceVerlet(theta, u, N, c, k, h):
    n,nbounce,dt = 0,0,0.02
    x,y,vx,vy=[0],[h],[u*math.sin(theta)],[u*math.cos(theta)]
    while nbounce <= N:
        v = math.sqrt(vx[n]**2+vy[n]**2)
        ax = -(vx[n]/v)*k*v**2
        ay = -g-(vx[n]/v)*k*v**2
        x.append(x[n] + vx[n]*dt + 0.5*ax*dt**2)
        y.append(y[n] + vy[n]*dt + 0.5*ay*dt**2)
        aax = -(vx[n]/v)*k*v**2
        aay = -g-(vy[n]/v)*k*v**2
        vx.append(vx[n] + 0.5*(ax + aax)*dt)
        vy.append(vy[n] + 0.5*(ay + aay)*dt)
        if y[n+1] < 0:
            y[n+1] = 0
            vy[n+1] = -c*vy[n+1]
            nbounce+=1
        n+=1
    return [[x[i],y[i]] for i in range(n+1)]            

def line(theta,u, rng,h):
    data=[]
    y=h
    x=0
    while y >= 0:
        x+=(rng/100)
        y = yfromx(theta,g,x,h,u)
        data.append((x,y))
    return data

def plot(g, h=0, u=None, thetas=None, showMinMax=False, X=None, Y=None, bounce=0, k=0, bounceConstant=0):
    if thetas == None:
        if u == None:
            u = minU(g,X,Y)
            thetas = thetaFromU(u,X,Y,h)
        else:
            if X == None: thetas = (maxRange(g,h,u),)
            else: thetas = thetaFromU(u,X,Y,h)
    else: thetas=tuple([math.radians(i) for i in thetas])
    for theta in thetas:
        rng = ((u*math.sin(theta)+math.sqrt(2*h*g+(u*math.sin(theta))**2))/g)*u*math.cos(theta)
        outval={"Theta (rad)":theta,
                "Theta (deg)":math.degrees(theta),
                "U":u,
                "VX":math.cos(theta)*u,
                "VY":math.sin(theta)*u, 
                "ToF": rng/(u*math.cos(theta)),
                "Range": rng,
                "Distance": distance(theta,u,g,rng)}
        if bounce==False and k == 0: data = line(theta,u,rng,h)
        else: data = bounceVerlet(theta, u, bounce, bounceConstant, k, h)
        plt.plot([i[0] for i in data],[i[1] for i in data])
        [print(i,round(outval[i],3)) for i in outval]
        if theta >= math.asin(2*math.sqrt(2)/3) and showMinMax == True:
            times=(((3*u)/(2*g))*(math.sin(theta)+math.sqrt(math.sin(theta)**2-(8/9))),
                ((3*u)/(2*g))*(math.sin(theta)-math.sqrt(math.sin(theta)**2-(8/9))))
            for t in times:
                print(t)
                x=u*t*math.cos(theta)
                y=yfromx(theta,g,x,h)
                plt.plot(x,y,marker="x")
                print("Turning point t/rng:",x,y)
            
def bound(u,h):
    y=h
    x=0
    data=[]
    while y>=0:
        x+=0.02
        y=(u**2/(2*g))-((g*x**2)/(2*u**2))+h
        data.append((x,y))
    plt.plot([i[0] for i in data],[i[1] for i in data])

def update_plot():
    print(lines,'pre-change')
    lines[-1]['g'] = float(g_entry.get())
    lines[-1]['t'] = float(t_entry.get())
    print(lines)
    plt.clf()  # Clear the existing plot
    for i in lines:
        plot(i['g'], thetas=(i['t'],), u=2, h=0)
    canvas.draw()

def save_line():
    print(lines, 'saved')
    lines.append({'g':lines[-1]['g'], 't': lines[-1]['t']})

# Create a Tkinter window
root = tk.Tk()
root.title("Projectile Motion Plot")

# Create a FigureCanvasTkAgg widget
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Call your plot function with initial parameters
plot(g, thetas=(t,), u=2, h=0)

g_label = tk.Label(root, text="Acceleration due to gravity (g):")
g_label.pack()
g_entry = tk.Entry(root)
g_entry.insert(0, str(g))
g_entry.pack()
t_label = tk.Label(root, text="Theta:")
t_label.pack()
t_entry = tk.Entry(root)
t_entry.insert(0, str(t))
t_entry.pack()
update_button = tk.Button(root, text="Update Plot", command=update_plot)
update_button.pack()
save_button = tk.Button(root, text="Save Line", command=save_line)
save_button.pack()
root.mainloop()
