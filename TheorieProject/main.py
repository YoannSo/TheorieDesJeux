from tkinter import * 
import random


from joueur import Joueur
from jeu import Jeu

game = Jeu([])
width = 600
height = 600

def createGame():

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
    result = game.equilibreDeNash()
    print("Nash:", result)
    return result


def mixedNash():
    updateGame()
    result = game.equilibreDeNashMixte()
    print("Mixed Nash:", result)
    return result


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
    # print(mixed_strategies)
    return mixed_strategies


def simulate():
    mixed_strategies = readMixedStrategies()
    print(sum(mixed_strategies))
    if(sum(mixed_strategies) != 1):
        print("Please change probabilites so the total sum is equal to 1.")
        return

    else:
        print("Simulating game over 100 iterations")
        player1_gains = []
        player2_gains = []
        utilJ1, utilJ2 = game.equilibreDeNashMixte()

        # player 1's probabilites for both his strategies
        p0_J1, p1_J1 = mixed_strategies[0], mixed_strategies[1]

        # player 2's probabilites for both his strategies 
        # TODO doesn't always return values between 0 and 1 !!!!
        p0_J2, p1_J2 = utilJ2[1]/utilJ2[0], 1-utilJ2[1]/utilJ2[0]
        
        print("J1", p0_J1, p1_J1)
        print("J2", p0_J2, p1_J2)

        mixedJ2 = [p0_J2, p1_J2]
        for i in range(100): # 100 iterations
            rand = random.uniform(0, 1) # generate a random to chose what strategy to chose for each player
            
            if(rand > p0_J1): # then chose p1_J1
                if(rand > p0_J2): # then chose p1_J2
                    index = 1, 1 # <=> line 1, column 1
                else: 
                    index = 1, 0 # maybe the other way around (0, 1)?
            else:
                if(rand > p0_J2):
                    index = 0, 1
                else:
                    index = 0, 0

            player1_gains.append(game.matrix[index[0]][index[1]][0])
            player2_gains.append(game.matrix[index[0]][index[1]][1])

        # print("box chosen is", index)
        # print(game.matrix[index[0]][index[1]])
        
        print("Player 1 gains:", sum(player1_gains), ", average per turn:", sum(player1_gains)/100)
        print("Player 2 gains:", sum(player2_gains), ", average per turn:", sum(player2_gains)/100)
    

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
