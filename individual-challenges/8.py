import matplotlib.pyplot as plt
import math

g = 10
fractions=100
h=2

def bounceVerlet(theta, u, N, c):
    n,nbounce,dt = 0,0,0.02
    positions=[[0,h]]
    velocities=[[u*math.sin(theta), u*math.cos(theta)]]
    while nbounce <= N:
        positions.append([positions[n][0]+velocities[n][0]*dt,
                          positions[n][1]+velocities[n][1]*dt+0.5*-g*dt**2])
        velocities.append([velocities[n][0],
                           velocities[n][1]+0.5*dt*(-2*g)])
        if positions[n+1][1] < 0:
            positions[n+1][1] = 0
            velocities[n+1][1] = -c*velocities[n+1][1]
            nbounce+=1
        n+=1
    plt.plot([i[0] for i in positions],[i[1] for i in positions])
            
u=10
theta=math.radians(30)
bounceVerlet(90-theta,u,5,0.8)

plt.show()