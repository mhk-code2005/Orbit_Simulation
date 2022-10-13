from cv2 import Feature2D, add
from matplotlib import pyplot as plt
G = 6.67 * 10**-11

print("WELCOME TO THE GRAVITY SIMULATOR")
print()
print("YOU CAN SIMULATE THE MOVEMENET OF PLANETS IN THIS PROGRAM")
print("IF YOU WANT TO EDIT THE NUMBER OF PLANETS, OR THEIR PROPERTIES, YOU CAN EDIT THE orbit.py FILE")
a = int(input('DO YOU WANT TO GRAPH THE ACCELERATION[1] OR THE VELOCITY[2], OR NONE OF THEM[0]:'))
print("ENJOY!!")

class planet():
    #coord -> (x,y)
    #velocity -> [x,y]

    def __init__(self, mass, velocity, coord, acceleration = 0):
        self.mass = mass
        self.velocity = velocity
        self.coord = coord
        self.acceleration = acceleration


def distance(P1, P2):
    return ( (P1.coord[0]-P2.coord[0])**2 + (P1.coord[1]-P2.coord[1])**2 )**(1/2)

def calculateForceMagnitude(P1, P2):
    F = G * (P1.mass) * (P2.mass) / distance(P1, P2)
    return F

def crash(P1, P2, margin):
    if P2.coord[0]-margin<P1.coord[0]<P2.coord[0]+margin and P2.coord[1]-margin<P1.coord[1]<P2.coord[1]+margin:
        print('BOOOOOOOM! ', bodies[P1][0], 'and', bodies[P2][0], 'crashed!')
        return True
    return False

def forceComponents(P1, P2):
    vector = (P2.coord[0] - P1.coord[0], P2.coord[1] - P1.coord[1])
    Vector_Mag = ( vector[0]**2 + vector[1]**2 )**(.5)
    F = calculateForceMagnitude(P1, P2)
    return ( vector[0] * (F/Vector_Mag), vector[1] * (F/Vector_Mag) )

def calculateAccelerations(P1, F):
    return (F[0]/P1.mass, F[1]/P1.mass)
    
def updateVel(P1, F , timeInterval):
    a1 = calculateAccelerations(P1, F)
    P1.acceleration = a1
    P1.velocity[0] +=  a1[0]*timeInterval
    P1.velocity[1] +=  a1[1]*timeInterval


def updateCoords(P1, timeInterval):
    P1.coord = P1.coord[0]+P1.velocity[0]*timeInterval, P1.coord[1]+P1.velocity[1]*timeInterval




P1 = planet(10000000000, [5,0], [0, 4000])
P2 = planet(1000000000000, [.2, 0], [2000,0])
P3 = planet(10000000000, [-3, 0], [0,-4000])
P4 = planet(100000000000, [0, 0], [0,0])
P5 = planet(1000000000000, [4, -2], [3000,-4000])
P6 = planet(1000000000000, [0, 1], [-3000,0])
P7 = planet(100000000000, [3,4 ], [-4000,4000])


def F_Mag(F):
    return ( F[0]**2 + F[1]**2 ) ** (.5) 

def addForces(initial, new):
    return initial[0]+new[0], initial[1] + new[1]

bodies = {P1:['P1', 'green', P1.coord], 
    P2:['P2', 'gray', P2.coord], 
    P3:['P3','red', P3.coord],
    P4:['P4','blue', P4.coord], 
    P5:['P5','orange', P5.coord], 
    P6:['P5','magenta', P6.coord], 
    P7:['P5','purple', P7.coord]}

bodies1 = {P1:['P1', 'green', P1.coord], P2:['P2', 'red', P2.coord], P3:['P3','gray', P3.coord]}
bodies3 = {P1:['Earth', 'green', P1.coord], P2:['Moon', 'gray', P2.coord], P3:['Sun','red', P3.coord], P4:["Saturn", 'orange',P4.coord]}
bodies4 = {P1:['Earth', 'green', P1.coord], P2:['Sun', 'gray', P2.coord]}

graphPointers = {}
for P in bodies:
    graphPointers.update({P:[[[],[]],[[],[]]]})


time_interval = 5
time = 0






def plotA_Values(graphPointers, val = 0):
    
    if val!=0:

        for planet in graphPointers:
            if val == 1:
                plt.plot(graphPointers[planet][1][1] , color = bodies[planet][1], label = bodies[planet][0]+" Acceleration")
            if val == 2:
                plt.plot(graphPointers[planet][0][1],'--', color = bodies[planet][1], label = bodies[planet][0]+" Velocity" )
        plt.legend()
    plt.draw()
    plt.pause(.0001)
    plt.clf()


past_points = []

i = 0
crashed = []
newlyAdded = []
crashedCouples = []

while True:
    i+=1
    #Updates the coordinates
    for Planet in bodies:
        for oppositePlanet in bodies:
            if Planet!=oppositePlanet and Planet not in crashed and oppositePlanet not in crashed:
                if crash(Planet, oppositePlanet, 200):
                    crashed.append(oppositePlanet)
                    crashedCouples.append((Planet, oppositePlanet))

    for f in crashedCouples:
        Vx = (f[0].velocity[0]*f[0].mass + f[1].velocity[0]*f[1].mass) / (f[0].mass+f[1].mass)
        Vy = (f[0].velocity[1]*f[0].mass + f[1].velocity[1]*f[1].mass) / (f[0].mass+f[1].mass)
        f[0].velocity = [Vx, Vy]
        f[0].mass += f[1].mass
        bodies.pop(f[1])
    crashedCouples = []

    for t in newlyAdded:
        bodies.update({t[0]:t[1]})
    
    for Planet in bodies:
        orig_coord = Planet.coord
        netF = 0,0
        for oppositePlanet in bodies:
            if Planet not in crashed and oppositePlanet not in crashed:
                if Planet != oppositePlanet:
                    F = forceComponents(Planet, oppositePlanet)
                    netF = addForces(netF, F)
                
        updateVel(Planet, netF,time_interval)
        updateCoords(Planet, time_interval)
        bodies[Planet][2] = Planet.coord
        Planet.coord = orig_coord



    for Planet in bodies:
        Planet.coord = bodies[Planet][2]

    #Saves the acceleration and velocity values
    if a != 0:
        for planet in bodies:
            if a == 1:
                graphPointers[planet][1][1].append(F_Mag(planet.acceleration))
            
                graphPointers[planet][0][0].append(time)

            if a == 2:
                graphPointers[planet][0][1].append(F_Mag(planet.velocity))

                graphPointers[planet][1][0].append(time)
        plt.figure(2)
        plotA_Values(graphPointers, a)

    #Plots the coordinates of the bodies
    for k in bodies:
        plt.figure(1)
        plt.xlim((-5* 10**3, 5* 10**3))
        plt.ylim((-5* 10**3, 5* 10**3))
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')

        plt.scatter(k.coord[0], k.coord[1], color = bodies[k][1], label = bodies[k][0])
    
        plt.quiver(k.coord[0], k.coord[1], k.velocity[0], k.velocity[1], label = "V_ "+str(bodies[k][0]), color = bodies[k][1])

        plt.legend()
    

    
    time += time_interval
    

    plt.draw()
    plt.pause(.0001)
    plt.clf()
    

