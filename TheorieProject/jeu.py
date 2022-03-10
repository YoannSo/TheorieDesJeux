class Jeu:
    def __init__(self,joueurs):
        self.joueurs=joueurs
        self.matrix = []

    def get_matrix(self):
        return self.matrix
    
    def estSommeNul(self):
        matrice= [[[-2,2],[-3,3],[-2,2]],[[-2,2],[-5,5],[-2,2]],[[-4,4],[-7,7],[0,0]]]
        for i in range(0, len(matrice)):
            for j in range(0, len(matrice[i])):
                somme=0
                for strategie in range (0,len(matrice[i][j])):
                    somme+=matrice[i][j][strategie]
                if(somme!=0):
                    return False
        return True

    def estSommeNul1(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                somme = 0
                for strategie in range (len(self.matrix[i][j])):
                    somme+=self.matrix[i][j][strategie]
                if(somme!=0):
                    return False
        return True