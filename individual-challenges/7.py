import matplotlib.pyplot as plt
import math

g = 10
fractions=100
h=5

def yfromx(theta,g,x,h):
    return round(x*math.tan(theta)-(g*x**2)/(2*u**2*math.cos(theta)**2)+h,5)

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
            "Range": rng}
    plt.plot([i[0] for i in data],[i[1] for i in data])
    [print(i,round(outval[i],3)) for i in outval]
    if theta >= math.asin(2*math.sqrt(2)/3):
        times=(((3*u)/(2*g))*(math.sin(theta)+math.sqrt(math.sin(theta)**2-(8/9))),
               ((3*u)/(2*g))*(math.sin(theta)-math.sqrt(math.sin(theta)**2-(8/9))))
        for t in times:
            print(t)
            x=u*t*math.cos(theta)
            y=yfromx(theta,g,x,h)
            plt.plot(x,y,marker="x")
            print("Turning point t/rng:",round(x,3),round(y,3))

u=10
theta=math.radians(70.55)
line(theta,u)
theta=math.radians(78)
line(theta,u)
theta=math.radians(85)
line(theta,u)
plt.show()