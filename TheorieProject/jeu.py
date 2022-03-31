class Jeu:
    def __init__(self,joueurs):
        self.joueurs=joueurs
        self.matrix = []

    def get_matrix(self):
        return self.matrix
    
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
        print(j1.strategies)
        print(j2.strategies)

        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                gainCourant=self.matrix[i][j][1]
                j1Best= True
                j2Best=True
                for k in range(0, len(j2.strategies[i])):
                    #print("Courant:"+str(gainCourant)+" Dans strat:" +str(j2.strategies[i][k]))
                    if(gainCourant<j2.strategies[k][i]):
                        j2Best=False
                        break
                if(j2Best==False):
                    continue

                gainCourant=self.matrix[i][j][0]
                for k in range(0,len(j1.strategies[i])):
                    if(gainCourant<j1.strategies[k][j]):
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

    
    def equilibreDeNashMixte(self):
        allEquilibre=[]
        #j1 = Joueur("A",[[2,1],[0,1]])
        #j2 = Joueur("A",[[1,0],[0,2]])
        j1 = self.joueurs[0]
        j2 = self.joueurs[1]
        # matrice= [[[1,1],[1,1]],[[-1,-1],[2,0]]]
        
        utilitej1s1=[j1.strategies[0][0]-(j1.strategies[0][1]),(j1.strategies[0][1])]
        utilitej1s2=[j1.strategies[1][0]-(j1.strategies[1][1]),(j1.strategies[1][1])]
        
        utilitej2s1=[j2.strategies[0][0]-(j2.strategies[1][0]),(j2.strategies[1][0])]
        utilitej2s2=[j2.strategies[0][1]-(j2.strategies[1][1]),(j2.strategies[1][1])]

        utiliteJ1=[utilitej1s1[0]-utilitej1s2[0],utilitej1s1[1]-utilitej1s2[1]]
        utiliteJ2=[utilitej2s1[0]-utilitej2s2[0],utilitej2s1[1]-utilitej2s2[1]]
        
        xJ1=np.linspace(0,1,500)
        xJ2=np.linspace(0,1,500)
        yJ1=np.linspace(0,1,500)
        yJ2=np.linspace(0,1,500)
        i=0
        for x in xJ2:
            if utiliteJ1[0]*x + utiliteJ1[1] > 0:
                yJ2[i] = 1
            else:
                yJ2[i] = 0
            i+=1
                
        i=0   
        for x in xJ1:
            if utiliteJ2[0]*x + utiliteJ2[1] > 0:
                xJ1[i] = 1
            else:
                xJ1[i] = 0
            i+=1
        utiliteJ1=[abs(utiliteJ1[0]),abs(utiliteJ1[1])]
        utiliteJ2=[abs(utiliteJ2[0]),abs(utiliteJ2[1])]
        nashEquilibreJ1 = float(utiliteJ1[1])/float(utiliteJ1[0])
        nashEquilibreJ2= float(utiliteJ2[1])/float(utiliteJ2[0])
        print(nashEquilibreJ1,nashEquilibreJ2)
        if(nashEquilibreJ1 + nashEquilibreJ2 <=2 and nashEquilibreJ1 + nashEquilibreJ2>=0):
            stringNashEquilibreJ1=str(utiliteJ1[1])+"/"+str(utiliteJ1[0])
            stringNashEquilibreJ2=str(utiliteJ2[1])+"/"+str(utiliteJ2[0])

            print("Ceci sont les equilibres de nash en strategie mixtes:\n J1:"+stringNashEquilibreJ1+"\n J2:"+stringNashEquilibreJ2)
            plt.plot(xJ1, yJ1,"-")
            plt.plot(xJ2, yJ2,"-")
        else:
            print("Aucun equilibre de nash en strategie mixtes")
                    