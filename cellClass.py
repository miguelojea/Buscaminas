from tkinter import *
from variables import *
import random
import time

class Cell:
    sizeX = None
    sizeY = None
    all = []
    nMines = None
    cellCounter = 0
    flagCounter = 0
    labelCellCounter = None
    labelFlagCounter = None
    labelGameState = None
    iniciado = False
    nColors = [None, 'green', 'blue', 'red', 'magenta', 'purple', 'black', 'black', 'black']
    time0 = 0
    time = 0

    imgButton = None
    imgPushing = None
    imgFlag = None
    imgMine = None
    imgVoid = None
    img0 = None



    def __init__(self, row, col, mainFrame):
        self.row = row
        self.col = col
        self.mainFrame = mainFrame
        self.isMine = False

        self.state = "button" #Cell state: "button", "pushing", "clear", "flag"

        self.frame = None
        self.label = None

        Cell.all[row][col] = self

    @staticmethod
    def defDimensionsGame(x,y,n):
        Cell.sizeX = x
        Cell.sizeY = y
        Cell.nMines = n
        Cell.all = [[0] * x for i in range(y)]

    def createButton(self, frame):
        self.frame = Frame(frame, width=25, height=25, bg="white")
        self.frame.grid(row=self.row, column=self.col)
        self.frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it

        self.label = Label(self.frame, image=self.imgButton, compound='center', font = CELL_FONT)
        self.label.pack(expand = True)

        self.label.bind("<ButtonPress>", self.press)
        self.label.bind("<ButtonRelease>", self.release)
        self.label.bind("<Leave>", self.leave)

    @staticmethod
    def loadImages():
        Cell.imgButton = PhotoImage(file="images/button.png")
        Cell.imgPushing = PhotoImage(file="images/PushedButton.png")
        Cell.imgFlag = PhotoImage(file="images/flag.png")
        Cell.imgMine = PhotoImage(file="images/mine.png")
        Cell.imgVoid = PhotoImage(file="images/void.png")
        Cell.img0 = PhotoImage(file="images/0.png")

    @staticmethod
    def createCounters(frame):
        px=0
        py=4
        Cell.labelFlagCounter = Label(frame, bg='medium purple', image=Cell.imgFlag, text=Cell.flagCounter, font=TEXT_FONT, compound=RIGHT)
        Cell.labelFlagCounter.grid(row=0, column=0, padx=px, pady=py)
        Cell.labelBar1 = Label(frame, bg='medium purple', text="/", font=TEXT_FONT)
        Cell.labelBar1.grid(row=0, column=1, padx=px, pady=py)
        Cell.labelMineCounter = Label(frame, bg='medium purple', image=Cell.imgMine, text=Cell.nMines, font=TEXT_FONT, compound=RIGHT)
        Cell.labelMineCounter.grid(row=0, column=2, padx=px, pady=py)

        Cell.labelCellCounter = Label(frame, bg='medium purple', image=Cell.img0, text=Cell.cellCounter, font=TEXT_FONT, compound=RIGHT)
        Cell.labelCellCounter.grid(row=1, column=0, padx=px, pady=py)
        Cell.labelBar2 = Label(frame, bg='medium purple', text="/", font=TEXT_FONT)
        Cell.labelBar2.grid(row=1, column=1, padx=px, pady=py)
        Cell.labelCellNumber = Label(frame, bg='medium purple', image=Cell.imgButton, text=Cell.sizeX * Cell.sizeY - Cell.nMines, font=TEXT_FONT, compound=RIGHT)
        Cell.labelCellNumber.grid(row=1, column=2, padx=px, pady=py)

    @staticmethod
    def createTimerLabel(frame):
        Cell.labelTimer = Label(frame, bg='medium purple', text="00:00",
                                      font=("Comic sans","20","bold"), compound=RIGHT)
        Cell.labelTimer.grid(row=0, column=1)

    @staticmethod
    def createGameStateLabel(frame):
        Cell.labelGameState = Label(frame, bg='light grey', fg='black', bd=5, text=" Sin iniciar ",
                                font=("Comic sans", "20", "bold"),relief="ridge")
        Cell.labelGameState.pack()

        # Cell.labelCellCounter.config(text="Game over", borderwidth=10, bg='red', fg='black', \
        #                              font=('Cambria bold', 30), highlightbackground="black", highlightthickness=5)

    def press(self, event):
        """Acciones de pulsar una celda"""
        if self.state == "button" and event.num == 1:  # Press 1
            event.widget.config(image=Cell.imgPushing)
            self.state = "pushing"
        elif self.state == "button" and (event.num == 2 or event.num == 3):  # Press 2 or 3
            event.widget.config(image=Cell.imgFlag)
            self.state = "flag"
            Cell.flagCounter += 1
            Cell.labelFlagCounter.config(text=Cell.flagCounter)
        elif self.state == "flag" and (event.num == 2 or event.num == 3):  # Press 2 or 3
            event.widget.config(image=Cell.imgButton)
            self.state = "button"
            Cell.flagCounter -= 1
            Cell.labelFlagCounter.config(text=Cell.flagCounter)

    def release(self, event):
        """Acciones de despulsar una celda"""
        if self.state == "pushing" and event.num == 1:
            if Cell.iniciado == False:  # Primera celda pulsada
                Cell.iniciado = True
                self.setMines()
                self.clearCell(self.countSurroundMines())
                Cell.time0 = time.time()
                Cell.labelGameState.config(text=" En progreso ", bg='light blue')
            else:  # No primera celda
                self.clearCell(self.countSurroundMines())
                self.state = "pushed"

    @staticmethod
    def updateClock(frame):
        if not Cell.iniciado:
            Cell.time = 0
        else:
            Cell.time = time.time() - Cell.time0
        Cell.labelTimer.config(text=f"{round(Cell.time//60):02}:{round(Cell.time%60):02}")
        frame.after(1000, lambda:Cell.updateClock(frame))

    def leave(self, event):
        """Acciones de abandonar una celda pulsada"""
        pass

    def clearCell(self, minesSurround):
        """Muestra una celda"""
        if self.state == "flag":
            Cell.flagCounter -= 1
            Cell.labelFlagCounter.config(text=Cell.flagCounter)
        self.state = "clear"
        if self.isMine:
            self.label.config(image=Cell.imgMine, text='', bg="red")
            self.clearAllMines()
            Cell.labelGameState.config(text=" Derrota ", bg='red')

        elif minesSurround != 0:
            self.label.config(text=self.countSurroundMines(), image=Cell.imgVoid, bg='white',
                              fg=Cell.nColors[minesSurround])
            Cell.cellCounter+=1
        else:
            self.label.config(image=Cell.img0, text='')
            Cell.cellCounter+= 1
            self.clearSurroundCells()
        Cell.labelCellCounter.config(text=Cell.cellCounter)
        if Cell.cellCounter == Cell.sizeX*Cell.sizeY-Cell.nMines:
            Cell.labelGameState.config(text=" Victoria ", bg='green')

    def clearAllMines(self):
        """Muestra todas las celdas con mina"""
        for i in range(Cell.sizeY):
            for j in range(Cell.sizeX):
                if Cell.all[i][j].state == "flag":
                    Cell.flagCounter -= 1
                    Cell.labelFlagCounter.config(text=Cell.flagCounter)
                Cell.all[i][j].state = "clear"
                if Cell.all[i][j].isMine and Cell.all[i][j] is not self:
                    Cell.all[i][j].label.config(image=Cell.imgMine, text='', bg="white")


    def clearSurroundCells(self):
        """Muestra en cascada las celdas de alrededor sin mina"""
        stack = self.getSurroundCells()
        while stack:
            minesSurround = stack[0].countSurroundMines()
            if minesSurround != 0:
                stack[0].label.config(text=minesSurround, image=Cell.imgVoid, fg=Cell.nColors[minesSurround])
                Cell.cellCounter+=1
            else:
                stack[0].label.config(image=Cell.img0, text='')
                Cell.cellCounter+= 1
                for cell in stack[0].getSurroundCells():
                    stack.append(cell) if cell not in stack else stack
            if stack[0].state == "flag":
                Cell.flagCounter -= 1
                Cell.labelFlagCounter.config(text=Cell.flagCounter)
            stack[0].state = "clear"
            stack.pop(0)
        Cell.labelCellCounter.config(text=f"Celdas restantes: {Cell.cellCounter}")

    def checkSurroundCells(self,y,x):
        """Devuelve las celdas de alrededor que existen"""
        if Cell.sizeY > y >= 0 and Cell.sizeX > x >= 0:
            return Cell.all[y][x]

    def getSurroundCells(self):
        """Devuelve las celdas de alrededor"""
        cells = [
            self.checkSurroundCells(self.row-1,self.col-1),
            self.checkSurroundCells(self.row-1,self.col),
            self.checkSurroundCells(self.row-1,self.col+1),
            self.checkSurroundCells(self.row,self.col-1),
            self.checkSurroundCells(self.row,self.col+1),
            self.checkSurroundCells(self.row+1,self.col-1),
            self.checkSurroundCells(self.row+1,self.col),
            self.checkSurroundCells(self.row+1,self.col+1),
        ]
        cells = [cell for cell in cells if cell is not None and cell.state != "clear"]
        return cells

    def countSurroundMines(self):
        """Cuenta las minas de alrededor"""
        counter = 0
        for cell in self.getSurroundCells():
            if cell.isMine:
                counter += 1
        return counter

    def setMines(self):
        """Pone aleatoriamente las minas"""
        celdasConMina = random.sample( \
            list(range(self.row * Cell.sizeX + self.col)) + \
            list(range(self.row * Cell.sizeX + self.col + 1, Cell.sizeY * Cell.sizeX)), Cell.nMines)
        for i in celdasConMina:
            Cell.all[i // Cell.sizeX][i % Cell.sizeX].isMine = True

    # def __del__(self):
    #     print("deleted")

