
from tkinter import * 
import random


from joueur import Joueur
from jeu import Jeu

game = Jeu([])
width = 600
height = 600

def createGame():
    
    print("BEFORE")
    print(game.joueurs[0].strategies)
    print(game.joueurs[1].strategies)

    # fill the sub lists for each game.joueurs strategies
    for sublist in game.joueurs[0].strategies:
        for i in range(len(game.joueurs[1].strategies)):
            sublist.append(random.randint(-5, 5))

    for sublist in game.joueurs[1].strategies:
        for i in range(len(game.joueurs[0].strategies)):
            sublist.append(random.randint(-5, 5))

    

    for i in range(len(game.joueurs[0].strategies)):
        row = []
        for j in range(len(game.joueurs[1].strategies)):
            couple = [ game.joueurs[0].strategies[i][j], game.joueurs[1].strategies[j][i] ]
            row.append(couple)
        game.matrix.append(row)
    displayMatrix()
    frame.pack()


def createPlayer():
    player = Joueur(name.get(), [ [] for i in range(nb_strategies.get()) ])
    print("result", player.strategies)
    game.joueurs.append(player)
    print("Player", name.get(), "created with", nb_strategies.get(), "strategies.")


box = []

def displayMatrix():
    nb_lines = len(game.joueurs[0].strategies)
    nb_columns = len(game.joueurs[1].strategies)
    for i in range(nb_lines):
        box.append([])
        for j in range(nb_columns):
            box[i].append(StringVar())
            e = Entry(frame, textvariable=box[i][j], width = 5)
            e.grid(row=i, column=j)
            content = str(game.matrix[i][j][0]) + ", " + str(game.matrix[i][j][1])
            e.insert(END, content)


def updateGame():
    game.matrix = readMatrix()
    game.updateJoueur()


def clearMatrix():
    nb_lines = len(game.joueurs[0].strategies)
    nb_columns = len(game.joueurs[1].strategies)
    for i in range(nb_lines):
        for j in range(nb_columns):
            e = Entry(frame, textvariable=_, width = 5)
            e.grid(row = i, column = j)
            content = ""
            e.insert(END, content)


# method to read the user input matrix (GUI) and convert to list of lists
def readMatrix():
    matrix = []
    for i in range(len(game.joueurs[0].strategies)):
        matrix.append([])
        for j in range(len(game.joueurs[1].strategies)):
            split = box[i][j].get().split(",")
            content = [int(split[0]), int(split[1])]
            matrix[i].append(content)
    # print("USER INPUT:", matrix)
    return matrix
    


def strategieDomine():
    updateGame()
    game.strategieDomine()
    return 


def zeroSum():
    updateGame()
    print("Zero-sum game:", game.estSommeNul1())
    return game.estSommeNul1()


def nash():
    updateGame()
    result = game.equilibreDeNash(game.joueurs[0], game.joueurs[1])
    print("Nash:", result)
    return result


def mixedNash():
    updateGame()
    game.equilibreDeNashMixte()
    




strategy_box = []

# method to enter mixed strategies for a player (player 0)
def enterMixedStrategies():
    # the number of probabilities to enter is = to the number of strategies
    nb_strategies = len(game.joueurs[0].strategies) # get the number of strategies for player 0
    for i in range(nb_strategies):
        strategy_box.append(StringVar())
        e = Entry(frame1, textvariable=strategy_box[i], width = 5)
        e.grid(row = i)
        content = ""
        e.insert(END, content)


# method to read the probability of each strategy entered by the user
def readMixedStrategies():
    mixed_strategies = []
    nb_strategies = len(game.joueurs[0].strategies) # get the number of strategies for player 0
    for i in range(nb_strategies):
        content = float(strategy_box[i].get())
        mixed_strategies.append(content)
    print(mixed_strategies)
    return mixed_strategies


def simulate():
    mixed_strategies = readMixedStrategies()
    if(sum(mixed_strategies) > 1):
        print("Please change probabilites so the total sum is equal to 1.")
        return
    else:
        print("Simulating game over 100 iterations")
        player1_gain = 0
        player2_gain = 0


    
def reset():
    clearMatrix()
    updateGame()
    frame.pack_forget()
    frame1.pack_forget()
    game.joueurs = []
    game.matrix = []
    print("Players have been reset!")
    
    


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

_ = Button(window, text="Mixed Nash equilibrium", command=mixedNash)
_.pack()

_ = Button(window, text="Mixed strategies", command=enterMixedStrategies)
_.pack()

frame1 = Frame(window)
frame1.pack()

_ = Button(window, text="Simulate", command=simulate)
_.pack()

_ = Button(window, text="RESET", command=reset)
_.pack()


window.mainloop()
