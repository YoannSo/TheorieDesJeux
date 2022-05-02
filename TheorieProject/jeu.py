# Import the necessary modules
import numpy as np
import matplotlib.pyplot as plt

# Game class
class Jeu:
    def __init__(self,joueurs):
        self.joueurs=joueurs # each game has players
        self.matrix = [] # and a matrix

    def get_matrix(self):
        return self.matrix

    def getResult(self,strategies):
        value = []
        for i in range(len(strategies)):
            value.append(self.joueurs[i].getValue(strategies,i,self));
        return value;

    #Marche uniquement a 2 joueurs
    def updateJoueur(self):
        self.joueurs[0].strategies = []
        for i in range (len(self.matrix)):
            self.joueurs[0].strategies.append([])

        self.joueurs[1].strategies = []
        for i in range (len(self.matrix)):
            self.joueurs[1].strategies.append([])

        """ Pour J1 """
        # x dans la matrice    
        for ligne in range(len(self.joueurs[0].strategies)):
            buf= []
            # y dans la matrice
            for colonne in range(len(self.joueurs[1].strategies)):
                valeur = self.matrix[ligne][colonne][0]
                buf.append(valeur)
            self.joueurs[0].strategies[ligne]=buf
                
        """ Pour J2 """ 
        for colonne in range(len(self.joueurs[1].strategies)):  
            buf = []
            for ligne in range(len(self.joueurs[0].strategies)):
                valeur = self.matrix[ligne][colonne][1]
                buf.append(valeur)
            self.joueurs[1].strategies[colonne]=buf


    # Method that returns if the game is zero-sum or not
    def estSommeNull(self,strategies):
        if (len(strategies)==len(self.joueurs)):
            res = self.getResult(strategies)
            tot = 0
            for i in range(len(res)):
                tot += res[i]
            if (tot==0):
                return True
            else:
                return False
        else:
            strat = strategies.copy()
            strat.append(0)
            for i in range(len(self.joueurs[len(strategies)].strategies)):
                if(self.estSommeNull(strat)==False):
                    return False
                strat[len(strategies)]+=1
            return True


    def listeStrat(self,strategies,liste):
        if (len(strategies)==len(self.joueurs)):
            liste.append(strategies.copy())
            return liste
        else:
            strat = strategies.copy()
            strat.append(0)
            for i in range(len(self.joueurs[len(strategies)].strategies)):
                liste=self.listeStrat(strat,liste)
                strat[len(strategies)]+=1
            return liste


    def checkNash(self,x):
        
        iterateur = 0
        valeurDeBase = self.getResult(x)
        bool = False
        for iterateur in range(len(x)):
            stratTest = x.copy()
            for i in range (len(self.joueurs[iterateur].strategies)):
                stratTest[iterateur]=i
                valeur=self.getResult(stratTest)
                if(valeur[iterateur]>valeurDeBase[iterateur]):
                    bool = True
                    break
            
             # S il y a mieux
            if (bool == True):
                break
        return bool


    # Method that retuns the Nash equlibrium
    def equilibreDeNash(self):
        allEquilibre=[]
        strategies = [0]*(len(self.joueurs)-1)
        listeStrategies = self.listeStrat([],[])
        for x in listeStrategies:
            if(self.checkNash(x)==False):
                allEquilibre.append(self.getResult(x))
        return allEquilibre


    # Method that returns if a strategy is dominated or not
    def estDominee(self,x,y):
        for i in range (len(x)):
            if x[i]<=y[i]:
                return False
        return True


    # Method to find all dominated strategies
    def strategieDomine(self):
        # Pour tous les joueurs, on regarde leur strategie dominee
        check = False
        for x in self.joueurs:
            # On fait deux iterateur qui vont comparer toutes les strategies
            for i in range (0,len(x.strategies)):
                dominant=True
                for j in range (0,len(x.strategies)):
                    if (i==j): continue
                    domine = self.estDominee(x.strategies[i],x.strategies[j])
                    if (domine):
                        check = True
                        print("Pour le joueur ",x.name,", la strategie ",j," est domminee par la strategie ",i,";")
                    else : dominant = False
                if (dominant):
                    print("La strategie ",i," du joueur ",x.name," est dominante.")
        if(not check):
            print("Pas de strategie dominee")

    
    def equilibreDeNashMixte(self):
        allEquilibre=[]
        j1 = self.joueurs[0]
        j2 = self.joueurs[1]
        
        #on va calculer les utilités de chaque strategie de chaque joueurs comme vu en cours avec p et q
        utilitej1s1=[j1.strategies[0][0]-(j1.strategies[0][1]),(j1.strategies[0][1])]
        utilitej1s2=[j1.strategies[1][0]-(j1.strategies[1][1]),(j1.strategies[1][1])]
        
        utilitej2s1=[j2.strategies[0][0]-(j2.strategies[0][1]),(j2.strategies[0][1])]
        utilitej2s2=[j2.strategies[1][0]-(j2.strategies[1][1]),(j2.strategies[1][1])]
        print(utilitej2s1,utilitej2s2)
        utiliteJ1=[utilitej1s1[0]-utilitej1s2[0],utilitej1s1[1]-utilitej1s2[1]]
        utiliteJ2=[utilitej2s1[0]-utilitej2s2[0],utilitej2s1[1]-utilitej2s2[1]]


        utiliteJ1=[utiliteJ1[0],-utiliteJ1[1]]
        utiliteJ2=[utiliteJ2[0],-utiliteJ2[1]]

        #pour eviter la division par 0
        if(utiliteJ1[0]==0 or utiliteJ2[0]==0):
            print("Pas d'equilibre de nash mixte non pur")
            return False,None, None

        #ensuite notre equilibre de nash mixte non pure est un membre sur l'autre, comme vu dans le cours pour l'equation
        nashEquilibreJ1 = float(utiliteJ1[1])/float(utiliteJ1[0])
        nashEquilibreJ2= float(utiliteJ2[1])/float(utiliteJ2[0])
        
        print(utiliteJ1)
        xJ1=np.linspace(0,1,500)
        xJ2=np.linspace(0,1,500)
        yJ1=np.linspace(0,1,500)
        yJ2=np.linspace(0,1,500)
        i=0

     #on va pouvoir ensuite creer deux fonctions entre 0 et 1 ,avant l'equilibre de nash c'est egale a 0 et apres c'est egal a 1. Le croisement entre les deux fonctions est l'equilibre de nash en solution mixtes non pure
        for x in xJ2:
            if x > abs(utiliteJ2[1]/utiliteJ2[0]):
                yJ2[i] = 1
            else:
                yJ2[i] = 0
            i+=1
                
        i=0   
        for x in xJ1:
            if x > abs(utiliteJ1[1]/utiliteJ1[0]):
                xJ1[i] = 1
            else:
                xJ1[i] = 0
            i+=1

        if(nashEquilibreJ1<0 or nashEquilibreJ2<0):
            print("Pas d'equilibre de nash mixte non pur")
            return False,None, None
        if(nashEquilibreJ1<=1 and nashEquilibreJ2<=1 and nashEquilibreJ1>=0 and nashEquilibreJ2>=0):
            stringNashEquilibreJ1=str(utiliteJ1[1])+"/"+str(utiliteJ1[0])
            stringNashEquilibreJ2=str(utiliteJ2[1])+"/"+str(utiliteJ2[0])

            print("Ceci sont les equilibres de nash en strategie mixtes:\n J1:"+stringNashEquilibreJ1+"\n J2:"+stringNashEquilibreJ2)
            plt.plot(xJ1, yJ1,"-")
            plt.plot(xJ2, yJ2,"-")
            xIntersection=nashEquilibreJ1
            yIntersection=nashEquilibreJ2
            plt.plot(yIntersection,xIntersection,'o')
            plt.show()
        else:
            print("Pas d'equilibre de nash mixte non pur")
            return False,None, None
        
        return True,nashEquilibreJ1, nashEquilibreJ2