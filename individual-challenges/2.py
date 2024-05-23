import matplotlib.pyplot as plt
import math
theta = math.radians(42)

def yfromx(theta,g,x,h):
    return round(x*math.tan(theta)-(g*x**2)/(2*u**2*math.cos(theta)**2)+h,5)
u = 10
g = 9.81
h=1
fractions=100

data=[]
y=h
x=0
rng = ((u*math.sin(theta)+math.sqrt(2*h*g+(u*math.sin(theta))**2))/g)*u*math.cos(theta)
apogx = (u*math.cos(theta))*(u*math.sin(theta))/g
apog=[round(apogx,5),yfromx(theta,g,apogx,h)]
while y >= 0:
    x+=(rng/fractions)
    y = yfromx(theta,g,x,h)
    data.append((x,y))
outval={"Theta":theta,
        "VX":math.cos(theta)*u,
        "VY":math.sin(theta)*u, 
        "ToF": rng/(u*math.cos(theta)),
        "Range": rng}
[print(i,round(outval[i],3)) for i in outval]
print(apog)
plt.plot([i[0] for i in data],[i[1] for i in data])
plt.plot(apog[0],apog[1], marker="x")
plt.show()