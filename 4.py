import matplotlib.pyplot as plt
import math

def yfromx(theta,g,x,h):
    return round(x*math.tan(theta)-(g*x**2)/(2*u**2*math.cos(theta)**2)+h,5)
def thetaFromU(u,X,Y):
    a=g*X**2/(2*u**2)
    b=-X
    c=Y-h+((g*X**2)/(2*u**2))
    return (math.atan((-b+math.sqrt(b**2-4*a*c))/(2*a)),
            math.atan((-b-math.sqrt(b**2-4*a*c))/(2*a)))
g = 9.81
fractions=100
h=2

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
    [print(i,round(outval[i],3)) for i in outval]
    plt.plot([i[0] for i in data],[i[1] for i in data])
X = 2
Y = 1
u=10
theta = thetaFromU(u,X,Y)
line(theta[0],u) # high ball
line(theta[1],u) # low ball
theta = math.asin(1/(math.sqrt(2+((2*g*h)/u**2))))
line(theta,u)
u = math.sqrt(g)*math.sqrt(Y+math.sqrt(X**2+Y**2)) # minimum u
theta = thetaFromU(u,X,Y)
line(theta[0],u)

plt.show()