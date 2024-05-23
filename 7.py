import matplotlib.pyplot as plt
import math

g = 10
fractions=100
h=5

def yfromx(theta,g,x,h):
    return round(x*math.tan(theta)-(g*x**2)/(2*u**2*math.cos(theta)**2)+h,5)
def thetaFromU(u,X,Y):
    a=g*X**2/(2*u**2)
    b=-X
    c=Y-h+((g*X**2)/(2*u**2))
    return (math.atan((-b+math.sqrt(b**2-4*a*c))/(2*a)),
            math.atan((-b-math.sqrt(b**2-4*a*c))/(2*a)))

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
            print("Turning point t/rng:",x,y)
def bound(u):
    y=h
    x=0
    data=[]
    while y>=0:
        x+=0.02
        y=(u**2/(2*g))-((g*x**2)/(2*u**2))+h
        data.append((x,y))
    plt.plot([i[0] for i in data],[i[1] for i in data])
X = 2
Y = 2
u=10
theta=math.radians(70.55)
line(theta,u)
theta=math.radians(78)
line(theta,u)
theta=math.radians(85)
line(theta,u)
theta = thetaFromU(u,X,Y)
line(theta[0],u) # high ball
line(theta[1],u) # low ball
theta = math.asin(1/(math.sqrt(2+((2*g*h)/u**2))))
line(theta,u)
bound(u)
u = math.sqrt(g)*math.sqrt(Y+math.sqrt(X**2+Y**2)) # minimum u
theta = thetaFromU(u,X,Y)
line(theta[0],u)
plt.show()