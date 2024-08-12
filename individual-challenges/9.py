import matplotlib.pyplot as plt
import math

g = 10
h=2

def bounceVerlet(theta, u, N, c, k):
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
    positions=[[x[i],y[i]] for i in range(n+1)]
    plt.plot([i[0] for i in positions],[i[1] for i in positions])
            
u=10
theta=math.radians(30)
bounceVerlet(90-theta,u,2,0.8,0)
bounceVerlet(90-theta,u,2,0.8,0.1)
plt.show()