import tkinter as tk
import itertools
from enum import Enum

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
        
        # Used mainly for giving params to canvas
        # TODO: Remove if not needed and just do math in getParamsForCanvas()
        self.endX = self.x + self.width
        self.endY = self.y + self.height
    
    # Return bounding box coordinates for canvas 
    def getParamsForCanvas(self):
        return self.x, self.y, self.endX, self.endY

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
    room1 = Room(20, 20, 300, 120)
    room2 = Room(380, 440, 40, 80)
    room3 = Room(60, 280, 40, 20)

    rooms.append(room1)
    rooms.append(room2)
    rooms.append(room3)
    
    # Initialize window for display
    m = tk.Tk()
    m.resizable(False, False)
    canvas = tk.Canvas(m, width=MAPWIDTH, height=MAPHEIGHT)

    addGrid(canvas)

    # Add rooms to canvas
    for r in rooms:
        canvas.create_rectangle(r.getParamsForCanvas())
        canvas.pack()

    # Display rooms
    m.mainloop()

if __name__ == "__main__":
    main()