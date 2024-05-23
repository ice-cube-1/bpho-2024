import matplotlib.pyplot as plt
import math
theta = math.radians(45)
speed = 20
g = 9.81
height=2
step=0.02

data=[]
y=height
x=0
while y >= 0:
    x+=step
    y = round(x*math.tan(theta)-(g*x**2)/(2*speed**2*math.cos(theta)**2)+height,5)
    data.append((x,y))

outval={"Theta":theta,"VX":math.cos(theta)*speed,"VY":math.sin(theta)*speed}
[print(i,round(outval[i],3)) for i in outval]
plt.plot([i[0] for i in data],[i[1] for i in data])
plt.show()