class Joueur:
    def __init__(self,name,strategies):
        self.name=name
        self.strategies=strategies

    def getValue(self,strategies,i,game):
        x = strategies[i]
        print(self.strategies[i])
        y=0
        for j in range (len(strategies),0):
            if (j==i): continue 
            else:
                y+=strategies[j]*len(game.joueurs[j].strategies)

        return self.strategies[x][y];
    