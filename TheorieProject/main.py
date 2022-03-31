#from asyncio.windows_events import NULL
from tkinter import * 
import random

from joueur import Joueur
from jeu import Jeu

players = []
game = Jeu(players)
width = 600
height = 600

def createGame():

    # print("BEFORE")
    # print(players[0].strategies)
    # print(players[1].strategies)

    # fill the sub lists for each players strategies
    for sublist in players[0].strategies:
        for i in range(len(players[1].strategies)):
            sublist.append(random.randint(-5, 5))

    for sublist in players[1].strategies:
        for i in range(len(players[0].strategies)):
            sublist.append(random.randint(-5, 5))

    

    for i in range(len(players[0].strategies)):
        row = []
        for j in range(len(players[1].strategies)):
            couple = [ game.joueurs[0].strategies[i][j], game.joueurs[1].strategies[j][i] ]
            row.append(couple)
        game.matrix.append(row)

    displayMatrix()


def createPlayer():
    player = Joueur(name.get(), [ [] for i in range(nb_strategies.get()) ])
    print("result", player.strategies)
    players.append(player)
    print("Player", name.get(), "created with", nb_strategies.get(), "strategies.")


box = []

def displayMatrix():
    nb_lines = len(players[0].strategies)
    nb_columns = len(players[1].strategies)
    for i in range(nb_lines):
        box.append([])
        for j in range(nb_columns):
            box[i].append(StringVar())
            e = Entry(frame, textvariable=box[i][j], width = 5)
            e.grid(row=i, column=j)
            content = str(game.matrix[i][j][0]) + ", " + str(game.matrix[i][j][1])
            e.insert(END, content)

def updateGame():
    print(game.joueurs[0].strategies) 
    print(game.joueurs[1].strategies) 
    game.matrix = readMatrix()
    game.updateJoueur()
    print(game.joueurs[0].strategies) 
    print(game.joueurs[1].strategies) 

def clearMatrix():
    nb_lines = len(players[0].strategies)
    nb_columns = len(players[1].strategies)
    for i in range(nb_lines):
        for j in range(nb_columns):
            e = Entry(frame, textvariable=_, width = 5)
            e.grid(row = i, column = j)
            content = ""
            e.insert(END, content)

# method to read the user input matrix (GUI) and convert to list of lists
def readMatrix():
    matrix = []
    for i in range(len(players[0].strategies)):
        matrix.append([])
        for j in range(len(players[1].strategies)):
            split = box[i][j].get().split(",")
            content = [int(split[0]), int(split[1])]
            matrix[i].append(content)
    # print("USER INPUT:", matrix)
    return matrix
    


def strategieDomine():
    updateGame()
    game.strategieDomine()
    return 0

def zeroSum():
    game.matrix = readMatrix()
    print("Zero-sum game:", game.estSommeNul1())
    return game.estSommeNul1()


def nash():
    game.matrix = readMatrix()
    result = game.equilibreDeNash(players[0], players[1])
    print("Nash:", result)
    return result
    
    


def reset():
    clearMatrix()
    players = []
    game.joueurs = []
    game.matrix = []
    print("Players have been reset!")
    # displayMatrix()
    


window = Tk()
window.geometry(str(width)+"x"+str(height))
window.title("Game Theory")



_ = Label(window, text="Player name:")
_.pack()

name = StringVar(window)
name.set("Benjyoatt")

_ = Entry(window, textvariable=name)
_.pack()

_ = Label(window, text="Number of strategies:")
_.pack()

nb_strategies = IntVar(window)
nb_strategies.set(2)

_ = Spinbox(window, from_=2, to=10, textvariable=nb_strategies)
_.pack()

_ = Button(window, text="Create player", command=createPlayer)
_.pack()

_ = Button(window, text="Create game", command=createGame)
_.pack()

_ = Label(window, text="Matrix")
_.pack()

frame = Frame(window)
frame.pack()

_ = Button(window, text="Zero-sum game?", command=zeroSum)
_.pack()

_ = Button(window, text="Nash equilibrium", command=nash)
_.pack()

_ = Button(window, text="dominees / dominant", command=strategieDomine)
_.pack()

_ = Button(window, text="RESET", command=reset)
_.pack()


window.mainloop()