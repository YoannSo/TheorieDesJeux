from tkinter import * 
import random

from joueur import Joueur
from jeu import Jeu

players = []
game = Jeu(players)
width = 500
height = 500

def createGame():   
    
    print(game.joueurs)
    for i in range(len(players[0].strategies)):
        for j in range(len(players[1].strategies)):
            box = [ game.joueurs[0].strategies[i], game.joueurs[1].strategies[j] ] 
            game.matrix.append(box)
    game.display()
    displayMatrix()



def createPlayer():
    player = Joueur(name.get(), [j for j in range(nb_strategies.get())])
    players.append(player)
    print(name.get(), "created with", nb_strategies.get(), "strategies")


window = Tk()
window.geometry(str(width)+"x"+str(height))
window.title("Game Theory")

label1 = Label(window, text="Name")
label1.pack()

name = StringVar(window)
name.set("Benjyoatt")

name_content = Entry(window, textvariable=name)
name_content.pack()

label2 = Label(window, text="Number of strategies")
label2.pack()

nb_strategies = IntVar(window)
nb_strategies.set(2)

s2 = Spinbox(window, from_=2, to=10, textvariable=nb_strategies)
s2.pack()

button1 = Button(window, text="Create player", command=createPlayer)
button1.pack()

button2 = Button(window, text="Create game", command=createGame)
button2.pack()


label4 = Label(window, text="Matrix")
label4.pack()



def displayMatrix():
    
    entries = [[None for i in range (2)] for j in range (2)]

    nb_lines = len(players[0].strategies)
    nb_columns = len(players[1].strategies)
    
    for i in range(nb_lines):
        for j in range(nb_columns):
            box = Entry(window, textvariable=entries[i][j],width=3)
            box.grid(row=i, column=j)
            entires = box
    
          

window.mainloop()