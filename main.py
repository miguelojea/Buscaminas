from tkinter import *
from tkinter import messagebox
from variables import *
from cellClass import Cell
import mysql.connector as mysql

def createMenus():
    global root, barraMenu, menuJuego, subMenuDif, menuEstadisticas

    barraMenu = Menu(root)  # Añadir primero el menú antes de dar dimensiones a root
    root.config(menu=barraMenu)

    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.resizable(False, False)

    menuJuego = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Juego", menu=menuJuego)

    menuJuego.add_command(label="Nueva partida", command=lambda: newGame(SIZE_X, SIZE_Y, N_Mines))
    menuJuego.add_command(label="Continuar", command=deleteStatsFrame)

    subMenuDif = Menu(menuJuego, tearoff=0)
    menuJuego.add_cascade(label="Dificultad", menu=subMenuDif)
    subMenuDif.add_command(label="Fácil", command=lambda: newGame(10, 10, 10))
    subMenuDif.add_command(label="Intermedio", command=lambda: newGame(15, 15, 30))
    subMenuDif.add_command(label="Difícil", command=lambda: newGame(20, 20, 60))
    subMenuDif.add_command(label="Personalizado", command=newGamePers)

    menuEstadisticas = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Estadísticas", menu=menuEstadisticas)
    menuEstadisticas.add_command(label="Tus estadísticas", command=tusEstadisticas)
    menuEstadisticas.add_command(label="Clasificación", command=createStatsFrame)
    # menu2.add_separator() #Línea continua para separar grupos de opciones

def createInitFrames():
    # topFrame.pack()
    # topFrame.pack_propagate(0)
    global root, topFrame, midFrame, bottomFrame
    topFrame = Frame(root, bg='light green', width=WIDTH, height=0.15 * HEIGHT)
    topFrame.place(x=0, y=0)

    midFrame = Frame(root, bg='light blue', width=WIDTH, height=0.75 * HEIGHT)  # borderwidth=0, highlightthickness=0
    midFrame.place(x=0, y=0.15 * HEIGHT)

    bottomFrame = Frame(root, bg='medium purple', width=WIDTH, height=0.1 * HEIGHT)
    bottomFrame.place(x=0, y=0.9 * HEIGHT)

    global titleLabel, userFrame, gameFrame, countersFrame, gameStateFrame, timerFrame, difficulty, difFrame, difLabel

    titleLabel = Label(topFrame, bg='black', fg='white', text="Buscaminas", font=("Comic sans", "20", "bold"), bd=10,
                       relief="sunken")  # , compound=RIGHT
    titleLabel.place(relx=.5, rely=.5, anchor=CENTER)

    difficulty = "Fácil"
    difFrame = Frame(topFrame, bg='light green', width=0.3 * WIDTH, height=HEIGHT)
    difFrame.place(relx=.15, rely=.5, anchor=CENTER)
    difLabel = Label(difFrame, text=f"Dificultad:\n{difficulty}", font=("Comic sans", "20", "bold"), bg="light green")
    difLabel.pack()

    userFrame = Frame(topFrame, bg='light green', width=0.3 * WIDTH, height=HEIGHT)
    userFrame.place(relx=.85, rely=.5, anchor=CENTER)

    global sesionIniciada, datosUsuario, user, password

    sesionIniciada = False
    datosUsuario = []
    user = StringVar()
    password = StringVar()

    Entry(userFrame, width=12, textvariable=user).grid(row=0, column=1, padx=5, pady=5)
    Entry(userFrame, width=12, textvariable=password, show="*").grid(row=1, column=1, padx=5, pady=5)
    Label(userFrame, text="Usuario:", bg="light green").grid(row=0, column=0, padx=5, pady=5, sticky=E)
    Label(userFrame, text="Contraseña:", bg="light green").grid(row=1, column=0, padx=5, pady=5, sticky=E)
    Button(userFrame, text="Iniciar sesion", command=lambda: login(str(user.get()), str(password.get()))).grid(
        row=2, column=0, padx=5, pady=2)
    Button(userFrame, text="Registrarse", command=lambda: register(str(user.get()), str(password.get()))).grid(
        row=2, column=1, padx=5, pady=2)

    gameFrame = Frame(midFrame, bg='black', borderwidth=2)
    gameFrame.place(relx=.5, rely=.5, anchor=CENTER)

    countersFrame = Frame(bottomFrame, bg='medium purple', width=0.5 * WIDTH, height=0.1 * HEIGHT)
    countersFrame.place(relx=.1, rely=.5, anchor=CENTER)

    gameStateFrame = Frame(bottomFrame, bg='medium purple', width=0.4 * WIDTH, height=0.1 * HEIGHT)
    gameStateFrame.place(relx=.5, rely=.5, anchor=CENTER)

    timerFrame = Frame(bottomFrame, bg='medium purple', width=0.15 * WIDTH, height=0.1 * HEIGHT)
    timerFrame.place(relx=.9, rely=.5, anchor=CENTER)

def createStatsFrame():
    global globalEstadisticasFrame
    globalEstadisticasFrame = Frame(midFrame, bg='white')
    globalEstadisticasFrame.place(relx=.5, rely=.5, anchor=CENTER)

    cnx = mysql.connect(host="localhost", user="root", passwd="siebm", database='buscaminas')
    cursor = cnx.cursor()

    sentencia = "SELECT nombre, recordFacil FROM usuarios WHERE recordFacil IS NOT NULL ORDER BY recordFacil LIMIT 3"
    cursor.execute(sentencia)
    facil = cursor.fetchall()
    sentencia = "SELECT nombre, recordIntermedio FROM usuarios WHERE recordIntermedio IS NOT NULL ORDER BY recordIntermedio LIMIT 3"
    cursor.execute(sentencia)
    medio = cursor.fetchall()
    print(medio)
    sentencia = "SELECT nombre, recordDificil FROM usuarios WHERE recordDificil IS NOT NULL ORDER BY recordDificil LIMIT 3"
    cursor.execute(sentencia)
    dificil = cursor.fetchall()

    px = 5
    py = 2
    pyTit = 5
    font1 = ("Comic sans", "20", "bold")
    font2 = ("Comic sans", "16", "bold")
    font3 = ("Comic sans", "10", "bold")
    Label(globalEstadisticasFrame, text="Clasificación global", font=font1).grid(row=0, column=0, columnspan=3, padx=px,
                                                                                 pady=pyTit)
    Label(globalEstadisticasFrame, text="Fácil", font=font2).grid(row=1, column=0, columnspan=3, padx=px, pady=pyTit)
    Label(globalEstadisticasFrame, text="Posición", font=font3).grid(row=2, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="Nombre", font=font3).grid(row=2, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="Tiempo", font=font3).grid(row=2, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="1º").grid(row=3, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="2º").grid(row=4, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="3º").grid(row=5, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=facil[0][0]).grid(row=3, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=facil[1][0]).grid(row=4, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=facil[2][0]).grid(row=5, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=facil[0][1]).grid(row=3, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=facil[1][1]).grid(row=4, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=facil[2][1]).grid(row=5, column=2, padx=px, pady=py)

    Label(globalEstadisticasFrame, text="Intermedio", font=font2).grid(row=7, column=0, columnspan=3, padx=px,
                                                                       pady=pyTit)
    Label(globalEstadisticasFrame, text="Posición", font=font3).grid(row=8, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="Nombre", font=font3).grid(row=8, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="Tiempo", font=font3).grid(row=8, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="1º").grid(row=9, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="2º").grid(row=10, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="3º").grid(row=11, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=medio[0][0]).grid(row=9, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=medio[1][0]).grid(row=10, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=medio[2][0]).grid(row=11, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=medio[0][1]).grid(row=9, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=medio[1][1]).grid(row=10, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=medio[2][1]).grid(row=11, column=2, padx=px, pady=py)

    Label(globalEstadisticasFrame, text="Difícil", font=font2).grid(row=13, column=0, columnspan=3, padx=px, pady=pyTit)
    Label(globalEstadisticasFrame, text="Posición", font=font3).grid(row=14, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="Nombre", font=font3).grid(row=14, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="Tiempo", font=font3).grid(row=14, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="1º").grid(row=15, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="2º").grid(row=16, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text="3º").grid(row=17, column=0, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=dificil[0][0]).grid(row=15, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=dificil[1][0]).grid(row=16, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=dificil[2][0]).grid(row=17, column=1, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=dificil[0][1]).grid(row=15, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=dificil[1][1]).grid(row=16, column=2, padx=px, pady=py)
    Label(globalEstadisticasFrame, text=dificil[2][1]).grid(row=17, column=2, padx=px, pady=py)

    if sesionIniciada:
        sentencia = "SELECT nombre, recordFacil FROM usuarios WHERE recordFacil IS NOT NULL ORDER BY recordFacil"
        cursor.execute(sentencia)
        resultado = cursor.fetchall()
        contador = 0
        for tupla in resultado:
            contador += 1
            if tupla[0] == datosUsuario[0][1]:
                break
        if contador > 3:
            Label(globalEstadisticasFrame, text=f"{contador}º", fg="green").grid(row=6, column=0, padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][1], fg="green").grid(row=6, column=1, padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][3], fg="green").grid(row=6, column=2, padx=px, pady=py)
        else:
            Label(globalEstadisticasFrame, text=f"{contador}º", fg="green").grid(row=contador + 2, column=0, padx=px,
                                                                                 pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][1], fg="green").grid(row=contador + 2, column=1,
                                                                                     padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][3], fg="green").grid(row=contador + 2, column=2,
                                                                                     padx=px, pady=py)

        sentencia = "SELECT nombre, recordIntermedio FROM usuarios WHERE recordIntermedio IS NOT NULL ORDER BY recordIntermedio"
        cursor.execute(sentencia)
        resultado = cursor.fetchall()
        contador = 0
        for tupla in resultado:
            contador += 1
            if tupla[0] == datosUsuario[0][1]:
                break
        if contador > 3:
            Label(globalEstadisticasFrame, text=f"{contador}º", fg="green").grid(row=12, column=0, padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][1], fg="green").grid(row=12, column=1, padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][4], fg="green").grid(row=12, column=2, padx=px, pady=py)
        else:
            Label(globalEstadisticasFrame, text=f"{contador}º", fg="green").grid(row=contador + 8, column=0, padx=px,
                                                                                 pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][1], fg="green").grid(row=contador + 8, column=1,
                                                                                     padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][4], fg="green").grid(row=contador + 8, column=2,
                                                                                     padx=px, pady=py)

        sentencia = "SELECT nombre, recordDificil FROM usuarios WHERE recordDificil IS NOT NULL ORDER BY recordDificil"
        cursor.execute(sentencia)
        resultado = cursor.fetchall()
        contador = 0
        for tupla in resultado:
            contador += 1
            if tupla[0] == datosUsuario[0][1]:
                break
        if contador > 3:
            Label(globalEstadisticasFrame, text=f"{contador}º", fg="green").grid(row=18, column=0, padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][1], fg="green").grid(row=18, column=1, padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][5], fg="green").grid(row=18, column=2, padx=px, pady=py)
        else:

            Label(globalEstadisticasFrame, text=f"{contador}º", fg="green").grid(row=contador + 14, column=0, padx=px,
                                                                                 pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][1], fg="green").grid(row=contador + 14, column=1,
                                                                                     padx=px, pady=py)
            Label(globalEstadisticasFrame, text=datosUsuario[0][5], fg="green").grid(row=contador + 14, column=2,
                                                                                     padx=px, pady=py)

    cursor.close()
    cnx.close()

def deleteStatsFrame():
    if 'globalEstadisticasFrame' in globals():
        global globalEstadisticasFrame
        for widget in globalEstadisticasFrame.winfo_children():
            widget.destroy()
        globalEstadisticasFrame.place_forget()


def tusEstadisticas():
    pass

def login(user, password):
    global sesionIniciada
    global datosUsuario
    cnx = mysql.connect(host="localhost", user="root", passwd="siebm", database='buscaminas')
    cursor = cnx.cursor()
    sentencia = f"SELECT * FROM usuarios WHERE nombre='{user}'"
    cursor.execute(sentencia)
    datosUsuario = cursor.fetchall()
    if not datosUsuario:
        messagebox.showwarning("Error", "Usuario no registrado.")
        return
    elif password != datosUsuario[0][2]:
        messagebox.showwarning("Error", "Contraseña incorrecta.")
        return
    else:
        sesionIniciada = True
        for widget in userFrame.winfo_children():
            widget.destroy()
        Label(userFrame, text="Usuario:").grid(row=0, column=0, padx=5, pady=2)
        Label(userFrame, text=datosUsuario[0][1]).grid(row=0, column=1, padx=5, pady=2)

    cursor.close()
    cnx.close()

def register(user, password):
    global sesionIniciada
    global datosUsuario
    cnx = mysql.connect(host="localhost", user="root", passwd="siebm", database='buscaminas')
    cursor = cnx.cursor()
    sentencia = f"SELECT * FROM usuarios WHERE nombre='{user}'"
    cursor.execute(sentencia)
    datosUsuario = cursor.fetchall()
    if datosUsuario:
        messagebox.showwarning("Error", "Usuario ya registrado.")
        return
    else:
        sentencia = "INSERT INTO usuarios (nombre, contrasenha) VALUES (%s, %s)"
        valores = (user, password)
        cursor.execute(sentencia, valores)
        cnx.commit()
        sesionIniciada = True
        for widget in userFrame.winfo_children():
            widget.destroy()
        Label(userFrame, text="Usuario:").grid(row=0, column=0, padx=5, pady=2)
        Label(userFrame, text=datosUsuario[0][1]).grid(row=0, column=1, padx=5, pady=2)
    cursor.close()
    cnx.close()

def newGame(x,y,n):

    global difficulty, difLabel
    if x==10 and y==10 and n==10:
        difficulty = "Fácil"
    elif x==15 and y==15 and n==30:
        difficulty = "Intermedio"
    elif x==20 and y==20 and n==60:
        difficulty = "Difícil"
    else:
        difficulty = "Personalizado"

    difLabel.config(text=f"Dificultad:\n{difficulty}")

    if x<5 or x>25 or y<5 or y>25 or x<1 or n>99:
        messagebox.showwarning("Error", "Valores fuera de rango.")
        return

    Cell.all = [[0] * Cell.sizeX for i in range(Cell.sizeY)]
    Cell.cellCounter = 0
    Cell.flagCounter = 0
    Cell.labelCellCounter = None
    Cell.labelFlagCounter = None
    Cell.labelGameState = None
    Cell.iniciado = False
    Cell.time0 = 0
    Cell.time = 0

    for widget in gameFrame.winfo_children():
        widget.destroy()
    for widget in countersFrame.winfo_children():
        widget.destroy()
    for widget in gameStateFrame.winfo_children():
        widget.destroy()
    for widget in timerFrame.winfo_children():
        widget.destroy()

    Cell.defDimensionsGame(x,y,n)

    for i in range(Cell.sizeY):
        for j in range(Cell.sizeX):
            Cell(i, j, gameFrame).createButton(gameFrame)

    Cell.createCounters(countersFrame)
    Cell.createTimerLabel(timerFrame)
    Cell.updateClock(timerFrame)
    Cell.createGameStateLabel(gameStateFrame)

    gameFrame.config(bg='black', borderwidth=2, relief = FLAT)

def newGamePers():

    # gameFrame.config()
    # gameFrame.place(relx=.5, rely=.5, anchor=CENTER)

    gameFrame.config(bg='yellow', borderwidth=10, relief = RIDGE)
    # gameFrame.place(relx=.5, rely=.3, anchor=CENTER)
    # gameFrame.pack_propagate(0)

    for widget in gameFrame.winfo_children():
        widget.destroy()

    # frameGamePers = Frame(gameFrame, bg='red', borderwidth=2)
    # frameGamePers.pack()
    px = 10
    py = 10

    Label(gameFrame, text="Dificultad personalizada").grid(row=0,column=0, columnspan=3, padx=px, pady=py)

    persX = StringVar()
    persY = StringVar()
    persN = StringVar()

    Entry(gameFrame, width=5, textvariable=persX).grid(row=1, column=1, padx=px, pady=py)
    Entry(gameFrame, width=5, textvariable=persY).grid(row=2, column=1, padx=px, pady=py)
    Entry(gameFrame, width=5, textvariable=persN).grid(row=3, column=1, padx=px, pady=py)
    Label(gameFrame, text="Tamaño horizontal:").grid(row=1,column=0, padx=px, pady=py, sticky=E)
    Label(gameFrame, text="Tamaño vertical:").grid(row=2,column=0, padx=px, pady=py, sticky=E)
    Label(gameFrame, text="Número de minas:").grid(row=3,column=0, padx=px, pady=py, sticky=E)
    Label(gameFrame, text="celdas (5-25)").grid(row=1,column=2, padx=px, pady=py, sticky=W)
    Label(gameFrame, text="celdas (5-25)").grid(row=2, column=2, padx=px, pady=py, sticky=W)
    Label(gameFrame, text="minas (1-99)").grid(row=3, column=2, padx=px, pady=py, sticky=W)
    Button(gameFrame, text="Confirmar", command=lambda:newGame(int(persX.get()), int(persY.get()), int(persN.get()))).grid(row=4,column=0, columnspan=3, pady=py, sticky="")

root = Tk()
root.title("Buscaminas")
root.iconbitmap("images/icon.ico")

createMenus()
createInitFrames()

# Label(midFrame, text="hola", borderwidth=0).grid(row=1,column=1)
# Label(midFrame, text="hola", borderwidth=0).grid(row=1,column=2)

Cell.loadImages()
Cell.defDimensionsGame(SIZE_X, SIZE_Y, N_Mines)

for i in range(Cell.sizeY):
    for j in range(Cell.sizeX):
        Cell(i, j, gameFrame).createButton(gameFrame)

Cell.createCounters(countersFrame)
Cell.createTimerLabel(timerFrame)
Cell.updateClock(timerFrame)
Cell.createGameStateLabel(gameStateFrame)

root.mainloop()