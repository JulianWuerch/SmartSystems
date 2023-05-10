import math
import serial

serialConnectionSpeed = 115200
setUpRunning = True
positions = []

def getConnectionToElement(port):
    return serial.Serial("/dev/serial/" + port, serialConnectionSpeed)

def configureElement(connection):
    #connection.write()
    pass

def getDistancesFromElement(connection):
    pass

#Funktion um aus Ankerpositionen und Abständen zu diesen eine neue Position zu berechnen
def calcPositionOfElement(positions, distances):
    #Falls das der erste Anker ist
    if len(positions) == 0:
        return (0, 0)
    
    #Falls nur ein Anker bis jetzt zur Verfügung steht
    if len(positions) == 1:
        return (positions[0] + distances[0], positions[1])

    distanceAncors = math.hypot(positions[0][0] - positions[1][0], positions[0][1] - positions[1][1])
    inLineFromA = (distances[0]**2 + distanceAncors**2 - distances[1]**2) / (2 * distanceAncors)
    perpendicular = math.sqrt(math.fabs(distances[0]**2 - inLineFromA**2))
    XdistanceAncors = positions[1][0] - positions[0][0]
    YdistanceAncors = positions[1][1] - positions[0][1]
    yI = positions[0][1] + (inLineFromA * YdistanceAncors) / distanceAncors + perpendicular * XdistanceAncors / distanceAncors
    xI = positions[0][0] + (inLineFromA * XdistanceAncors) / distanceAncors + perpendicular * YdistanceAncors / distanceAncors
    yII = positions[0][1] + (inLineFromA * YdistanceAncors) / distanceAncors - perpendicular * XdistanceAncors / distanceAncors
    xII = positions[0][0] + (inLineFromA * XdistanceAncors) / distanceAncors - perpendicular * YdistanceAncors / distanceAncors

    #jetz mit dem drittem Anker entscheiden welche Position wir nehmen
    if len(distances) >= 3:
        distI = math.fabs(math.hypot(xI - positions[2][0], yI - positions[2][1]) - distances[2])
        distII = math.fabs(math.hypot(xII - positions[2][0], yII - positions[2][1]) - distances[2])
        distIII = math.fabs(math.hypot(xII - positions[2][0], yI - positions[2][1]) - distances[2])
        distIV = math.fabs(math.hypot(xI - positions[2][0], yII - positions[2][1]) - distances[2])
        if distI < distII and distI < distIII and distI < distIV: 
            return (xI, yI)
        elif distII < distIII and distII < distIV:
            return (xII, yII)
        elif distIII < distIV:
            return (xII, yI)
        else:
            return (xI, yII)
    return (xII, yI)

def setPositionOfElement(connection, position):
    pass

def setUpElement(port):
    pass
    #Hier Serial Verbindung aufbauen
    connection = getConnectionToElement(port)

    #Hier das Element konfigurieren
    configureElement(connection)

    #Hier die Distanzen vom Element abrufen
    distances = getDistancesFromElement(connection)

    #Position finden
    position = calcPositionOfElement(positions, distances)

    #Position setzen
    setPositionOfElement(connection, position)
    positions.append(position)

def tokenSetUpLoop():
    elementIndex = 1
    while(setUpRunning):
        print("Positon Element " + str(elementIndex))
        input()
        print("Connect Element " + str(elementIndex))
        portToConfigure = input("Used Port: ")
        setUpElement(portToConfigure)
        print("Configuration of Element" + str(elementIndex) + " compleate")
        print()
        print()



print("**--------------------------------**")
print("**                                **")
print("**Nomadic Positioning System Setup**")
print("**                                **")
print("**--------------------------------**")
print("")
#print("**                                **")
panId = input("Input Pan-ID: ")
print("")

tokenSetUpLoop()
