from asyncio.windows_events import NULL
from tkinter import * 
import random

from joueur import Joueur
from jeu import Jeu

players = []
game = Jeu(players)
width = 300
height = 300

def createGame():
    row = []
    for i in range(len(players[0].strategies)):
        for j in range(len(players[1].strategies)):
            couple = [ game.joueurs[0].strategies[i], game.joueurs[1].strategies[j] ]
            row.append(couple)
        game.matrix.append(row)

    displayMatrix()


def createPlayer():
    player = Joueur(name.get(), [0 for j in range(nb_strategies.get())])
    players.append(player)
    print("Player", name.get(), "created with", nb_strategies.get(), "strategies.")

box = []


def displayMatrix():
    nb_lines = len(players[0].strategies)
    nb_columns = len(players[1].strategies)
    # print(nb_lines, nb_columns)
    # print(game.matrix)
    for i in range(nb_lines):
        box.append([])
        for j in range(nb_columns):
            box[i].append(StringVar())
            e = Entry(frame, textvariable=box[i][j], width = 5)
            e.grid(row=i, column=j)
            content = str(game.matrix[i][j][0]) + ", " + str(game.matrix[i][j][1])
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
    print("USER INPUT:", matrix)
    return matrix
    

def zeroSum():
    game.matrix = readMatrix()
    print("Zero-sum game:", game.estSommeNul1())
    return game.estSommeNul1()


def nash(players):
    game.matrix = readMatrix()
    result = game.equilibreDeNash(players[0], players[1])
    print("Nash:", result)
    return result
    


def reset():
    lst = []
    game = Jeu(lst)




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

_ = Button(window, text="RESET", command=reset)
_.pack()


window.mainloop()