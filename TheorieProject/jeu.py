class Jeu:
    def __init__(self,joueurs):
        self.joueurs=joueurs
        self.matrix = []

    def get_matrix(self):
        return self.matrix
    
    #Marche uniquement a 2 joueurs
    def updateJoueur(self):
        for i in range(len(self.joueurs[0].strategies)):
            for j in range(len(self.joueurs[0].strategies)):
                print("coucou, ca marche pas ici")
            


    def estSommeNul1(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                somme = 0
                for strategie in range (len(self.matrix[i][j])):
                    somme+=self.matrix[i][j][strategie]
                if(somme!=0):
                    return False
        return True

    def equilibreDeNash(self, j1, j2):
        allEquilibre=[]
        # j1 = Joueur("A",[[0,0,0],[0,5,4],[4,3,2]])
        # j2 = Joueur("A",[[2,3,2],[2,5,2],[2,7,0]])

        # matrice= [[[0,2],[0,3],[0,2]],[[0,2],[5,5],[4,2]],[[4,2],[3,7],[2,0]]]

        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                gainCourant=self.matrix[i][j][1]
                j1Best= True
                j2Best=True
                for k in range(0, len(j2.strategies[i])):
                    #print("Courant:"+str(gainCourant)+" Dans strat:" +str(j2.strategies[i][k]))
                    if(gainCourant<j2.strategies[i][k]):
                        j2Best=False
                        break
                if(j2Best==False):
                    continue

                gainCourant=self.matrix[i][j][0]
                for k in range(0,len(j1.strategies[i])):
                    if(gainCourant<j1.strategies[k][i]):
                        j1Best=False
                        break
                if(j1Best):
                    allEquilibre.append(self.matrix[i][j])
        return allEquilibre 

    def estDominee(semf,x,y):
        for i in range (len(x)):
            if x[i]<=y[i]:
                return False
        return True

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

    
                    