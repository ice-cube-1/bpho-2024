import matplotlib.pyplot as plt
import math

g = 9.81
fractions=100
h=2

def yfromx(theta,g,x,h):
    return round(x*math.tan(theta)-(g*x**2)/(2*u**2*math.cos(theta)**2)+h,5)

def z_func(z):
    return 0.5*math.log(abs(math.sqrt(1+z**2)+z))+0.5*z*math.sqrt(1+z**2)

def distance(theta, u, g, r):
    a = (u**2)/(g*(1+(math.tan(theta))**2))
    b = math.tan(theta)
    c = math.tan(theta)-g*r*(1+(math.tan(theta))**2)/(u**2)
    return a*( z_func(b)-z_func(c))


def line(theta,u):
    data=[]
    y=h
    x=0
    rng = ((u*math.sin(theta)+math.sqrt(2*h*g+(u*math.sin(theta))**2))/g)*u*math.cos(theta)
    while y >= 0:
        x+=(rng/fractions)
        y = yfromx(theta,g,x,h)
        data.append((x,y))
    outval={"Theta (rad)":theta,
            "Theta (deg)":math.degrees(theta),
            "U":u,
            "VX":math.cos(theta)*u,
            "VY":math.sin(theta)*u, 
            "ToF": rng/(u*math.cos(theta)),
            "Range": rng,
            "Distance": distance(theta,u,g,rng)}
    [print(i,round(outval[i],3)) for i in outval]
    plt.plot([i[0] for i in data],[i[1] for i in data])

u=10
theta=math.radians(60)
line(theta,u)
plt.show()