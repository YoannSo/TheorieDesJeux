class Joueur:
    def __init__(self,name,strategies):
        self.name=name
        self.strategies=strategies

    def getValue(self,strategies,i,game):
        copStrat = strategies.copy()
        x =copStrat.pop(i)
        listeJoueur = game.joueurs.copy()
        listeJoueur.pop(i)
        y=0
        Pas=1;
        for j in range (len(copStrat)-1,-1,-1):            
           y+= copStrat[j]*Pas
           Pas = Pas * len(listeJoueur[j].strategies)
        return self.strategies[x][y];
    