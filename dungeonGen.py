import tkinter as tk
import itertools
from enum import Enum
import random
import simpleTriangulation

"""
Dungeon maker for D&D 5e
Assumes a grid where 1 tile = 5 feet
"""

"""
Next Steps:
    - Add random room creation
    - Make random rooms not overlap/clash
    - Add hallways
"""


MAPWIDTH = 500 
MAPHEIGHT = 500 
GRIDSTEP = 20 

class RoomType(Enum):
    ROOM = 1
    HALLWAY = 2

class Room():
    id_iter = itertools.count()

    def __init__(self, x, y, width, height):
        self.id = next(Room.id_iter)

        # Lock room to grid
        if x % GRIDSTEP != 0:
            x = x - (x%GRIDSTEP)
        if y % GRIDSTEP != 0:
            y = y - (y%GRIDSTEP)

        if width % GRIDSTEP != 0:
            width = width - (width%GRIDSTEP)
        if height % GRIDSTEP != 0:
            height = height - (height%GRIDSTEP)

        # Make sure room is within boundaries
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        if x + width > MAPWIDTH:
            width = MAPWIDTH - x
        if y + height > MAPHEIGHT:
            height = MAPHEIGHT - y

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Used in Delaunay Triangulation
        self.midpoint = (self.x + self.width/2, self.y + self.height/2)
        
        # Used mainly for giving params to canvas
        # TODO: Remove if not needed and just do math in getParamsForCanvas()
        self.endX = self.x + self.width
        self.endY = self.y + self.height
    
    # Return bounding box coordinates for canvas 
    def getParamsForCanvas(self):
        return self.x, self.y, self.endX, self.endY

    ## AABB collision detection with optional padding
    def checkCollision(self, roomToCheck, padding = 0):
        if (self.x - padding * GRIDSTEP < roomToCheck.x + roomToCheck.width and 
            self.x + self.width + padding * GRIDSTEP > roomToCheck.x and 
            self.y - padding * GRIDSTEP < roomToCheck.y + roomToCheck.height 
            and self.y + self.height + padding * GRIDSTEP > roomToCheck.y): 
                return True
        return False

def addGrid(canvas):
    # Horizontal lines
    for x in range(0, MAPHEIGHT, GRIDSTEP):
        canvas.create_line(x, 0, x, MAPWIDTH, dash=(4, 2), fill='slate gray')
        canvas.pack()

    # Vertical lines
    for x in range(0, MAPWIDTH, GRIDSTEP):
        canvas.create_line(0, x, MAPHEIGHT, x, dash=(4,2), fill='slate gray')
        canvas.pack()

def main():

    # Create rooms
    rooms = []
    
    # Room creation variables
    # TODO: make these user input
    targetRoomCount = 10
    roomMinSize = 3
    roomMaxSize = 7

    # Make a set of randomly sized rooms we will try to place
    roomsToPlace = []
    for x in range(targetRoomCount):
        width = random.randint(roomMinSize, roomMaxSize) * GRIDSTEP
        height = random.randint(roomMinSize, roomMaxSize) * GRIDSTEP
        roomsToPlace.append((width, height))
    

    maxTries = 50
    for r in roomsToPlace:
        placed = False
        tries = 0
        while not placed and tries < maxTries:
            # Try to place room at random spot
            valid = True
            xPos = random.randint(0, MAPWIDTH/GRIDSTEP) * GRIDSTEP
            yPos = random.randint(0, MAPHEIGHT/GRIDSTEP) * GRIDSTEP

            # See if room is in bounds
            if xPos + r[0] <= MAPWIDTH and yPos + r[1] <= MAPHEIGHT:
                r1 = Room(xPos, yPos, r[0], r[1])
                # See if room collides
                for room in rooms:
                    if r1.checkCollision(room, 1):
                        valid = False
                        break
            else:
                valid = False
            
            if valid:
                rooms.append(r1)
                placed = True
            else:
                tries += 1
    
    # Initialize window for display
    root = tk.Tk()
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=MAPWIDTH, height=MAPHEIGHT)

    addGrid(canvas)

    # Add rooms to canvas
    for r in rooms:
        canvas.create_rectangle(r.getParamsForCanvas())
        canvas.pack()

    # Display rooms
    root.mainloop()

if __name__ == "__main__":
    main()