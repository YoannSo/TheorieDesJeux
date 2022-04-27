from tkinter import * 
import random
import matplotlib.pyplot as plt


from joueur import Joueur
from jeu import Jeu

game = Jeu([])
width = 600
height = 600


def buildMatrix(strategies):
    if (len(strategies)==len(game.joueurs)):
        return game.getResult(strategies)
    else:
        matrix = []
        strat = strategies.copy()
        strat.append(0)
        for i in range(len(game.joueurs[len(strategies)].strategies)):
            matrix.append(buildMatrix(strat))
            strat[len(strategies)]+=1
        return matrix
    

   

def createGame():
   
    # fill the sub lists for each game.joueurs strategies
        
    for i in range (len(game.joueurs)):
        total = 1
            
        for j in range(len(game.joueurs)):
            if (i!=j):
                total*=len(game.joueurs[j].strategies)

        for sublist in game.joueurs[i].strategies:
            for i in range (total):
                sublist.append(random.randint(-5, 5)) 
    if(len(game.joueurs)==2):        
        for i in range(len(game.joueurs[0].strategies)):
            row = []
            for j in range(len(game.joueurs[1].strategies)):
                couple = [ game.joueurs[0].strategies[i][j], game.joueurs[1].strategies[j][i] ]
                row.append(couple)
            game.matrix.append(row)
        displayMatrix()

    
        
    # On build la matrice
    i = 0
    matrix = buildMatrix([])
    for i in range(len(game.joueurs)):
        print("J"+str(i)+":")
        print(game.joueurs[i].strategies)
    print(matrix)    
    game.matrix = matrix
    showOptions()

def createPlayer():
    player = Joueur(name.get(), [ [] for i in range(nb_strategies.get()) ])
    game.joueurs.append(player)
    print("Player", name.get(), "created with", nb_strategies.get(), "strategies.")


def showOptions():
    label_matrix.pack()
    frame.pack()
    label_zero_sum.pack()
    label_nash.pack()
    label_dominated.pack()
    label_mix_nash.pack()
    label_create_mix.pack()

def hideOptions():
    label_matrix.pack_forget()
    frame.pack_forget()
    label_zero_sum.pack_forget()
    label_nash.pack_forget()
    label_dominated.pack_forget()
    label_mix_nash.pack_forget()
    label_create_mix.pack_forget()
    frame1.pack_forget()
    label_simulate.pack_forget()


box = []

def displayMatrix():
    nb_lines = len(game.joueurs[0].strategies)
    nb_columns = len(game.joueurs[1].strategies)
    box.clear()
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

# clear the display matrix
def clearMatrix():
    nb_lines = len(game.joueurs[0].strategies)
    nb_columns = len(game.joueurs[1].strategies)
    for i in range(nb_lines):
        for j in range(nb_columns):
            e = Entry(frame, textvariable=_, width = 5)
            e.grid(row = i, column = j)
            content = ""
            e.insert(END, content)


# clear the mixed strategies
def clearMixedStrategies():
    strategy_box.clear()
    for i in range(2):
        e = Entry(frame1, textvariable=_, width = 5)
        e.grid(row = i)
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
    #updateGame()
    game.strategieDomine()
    return 


def zeroSum():
    updateGame()
    print("Zero-sum game:", game.estSommeNul1())
    return game.estSommeNul1()


def nash():
    #updateGame()
    result = game.equilibreDeNash()
    print("Nash:", result)
    return result


def mixedNash():
    updateGame()
    boolean,nash1,nash2 = game.equilibreDeNashMixte()
    if boolean:
        print("Mixed Nash:", nash1 , nash2)
        return nash1,nash2


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
        frame1.pack()

    # display the simulate label
    label_simulate.pack()


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
    updateGame()
    mixed_strategies = readMixedStrategies()
    if(sum(mixed_strategies) != 1):
        print("Please change probabilites so the total sum is equal to 1.")
        return

    else:
        print("Simulating game over 100 iterations")
        player1_gains = []
        player2_gains = []
        mixteExists, _, utilJ2 = game.equilibreDeNashMixte()

        if(mixteExists):
            # player 1's probabilites for both his strategies
            p0_J1, p1_J1 = mixed_strategies[0], mixed_strategies[1]

            # player 2's probabilites for both his strategies 
            # TODO doesn't always return values between 0 and 1 !!!!
            p0_J2, p1_J2 = utilJ2, 1-utilJ2
            
            print("J1", p0_J1, p1_J1)   
            print("J2", p0_J2, p1_J2)

            mixedJ2 = [p0_J2, p1_J2]
            for i in range(100): # 100 iterations
                rand = random.uniform(0, 1) # generate a random to chose what strategy to chose for each player
                
                if(rand > p0_J1): # then chose p1_J1
                    if(rand > p0_J2): # then chose p1_J2
                        index = 1, 1 # <=> line 1, column 1
                    else: 
                        index = 1, 0
                else:
                    if(rand > p0_J2):
                        index = 0, 1
                    else:
                        index = 0, 0

                player1_gains.append(game.matrix[index[0]][index[1]][0]) # append player 1's gains to his list
                player2_gains.append(game.matrix[index[0]][index[1]][1]) # append player 2's gains to his list
            
            print("Player 1 gains:", sum(player1_gains), ", average per turn:", sum(player1_gains)/100)
            print("Player 2 gains:", sum(player2_gains), ", average per turn:", sum(player2_gains)/100)

            # plot the gain at each iteration with matplotlib for both players
            plt.plot(player1_gains, "ro", label="Player 1")
            plt.plot(player2_gains, "bo", label="Player 2")
            plt.xlabel("Iteration")
            plt.ylabel("Gain")
            plt.legend()
            plt.show()


def reset():
    clearMatrix()
    clearMixedStrategies()
    updateGame()
    hideOptions()
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

label_matrix = Label(window, text="Matrix")
# label_matrix.pack()

frame = Frame(window)
# frame.pack()

label_zero_sum = Button(window, text="Zero-sum game?", command=zeroSum)
# label_zero_sum.pack()

label_nash = Button(window, text="Nash equilibrium", command=nash)
# label_nash.pack()

label_dominated = Button(window, text="Dominant & Dominated Strategies", command=strategieDomine)
# label_dominated.pack()

label_mix_nash = Button(window, text="Mixed Nash equilibrium", command=mixedNash)
# label_mix_nash.pack()

label_create_mix = Button(window, text="Create a mixed strategy", command=enterMixedStrategies)
# label_create_mix.pack()

frame1 = Frame(window)
# frame1.pack()

label_simulate = Button(window, text="Simulate", command=simulate)
# label_simulate.pack()

_ = Button(window, text="RESET", command=reset)
_.pack(side = BOTTOM)


window.mainloop()
