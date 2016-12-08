from Temps import Tempsfrom Collection import Collectionfrom Satellite import Satelliteimport copyimport mathimport timeclass Lanceur:    """    Cette classe s'occupe de gerer les entrees sorties et de lancer la simulation    """    def __init__(self,fichier):        """        Constructeur de Lanceur        :param fichier: Le chemin du fichier contenant les donnees d'entree en caracteres ASCII        :type fichier: string        """        self.listeSatellite = []        self.listeCollection = []        self.listeCollectionValidee = []        self.listePhotosPossibles = []        # la liste de toutes les coordonnees de toutes les collections triees (par latitude croissante, si meme latitude par longitude decroissante)        self.listeCoordonneesTriees = []        self.score = 0        self.temps = None        self.nomFichier = fichier        self.lectureFichier()        self.lancerSimulation()    def lectureFichier(self):        """        Lit le fichier et en extrait:        le temps de la simulation        le nombre de satellites        les parametres initiaux des satellites:            latitude de depart            longitude de depart            vitesse de depart            changement d'orientation max d'un tour a l'autre            orientation max        le nombre d'images dans la collection        les points d'interet:            score rapporte pour la prise d'un point d'interet            latitude            longitude            intervals de prise de vue requis        """        with open(self.nomFichier,'r') as f:            #Premiere ligne pour le temps            self.temps = Temps(int(f.readline()))            #On creer les satellites            for i in range(0, int(f.readline())):                coord = f.readline().split(" ")                self.listeSatellite.append(Satellite(int(coord[0]),int(coord[1]),float(coord[2]),int(coord[3]),int(coord[4]),i))            #Ajout des collections d images            for i in range(0, int(f.readline())):                #line contient 1) Points 2) Nombre d images 3) Nombre d intervalles de temps                line = f.readline().split(" ")                images = []                temps = []                #Ajoute les coordonnees des images                for p in range(0, int(line[1])):                    images.append([int(j) for j in f.readline().strip('\n').split(" ")])                    #Parcours de images pour initialiser listeCoordonneesTriees                    for coord in images:                        #Si la coordonnees n'est pas deja dans listeCoordonneesTriees, alors on l'ajoute                        if(coord not in self.listeCoordonneesTriees):                            self.listeCoordonneesTriees.append(coord)                #Ajoute les intervalles de temps                for p in range(0, int(line[2])):                    temps.append(list(map(int, f.readline().strip('\n').split(" "))))                #Ajoute la collection                self.listeCollection.append(Collection(line[0], images, temps))            #Tri par latitude croissante et, si meme latitude par longitude decroissante            self.trierListeCoordonneesTriees()            #Initialise la liste des photos sur la trajectoire des satellites    def fichierSortie(self):        """        Ecrit le fichier de sortie contenant:            le nombre de photos prises            pour chaque photo prise:                latitude du point d'interet                longitude du point d'interet                tour de la prise de vue                numero du satellite ayant pris la prise de vue        """        # Pour eviter les duplications dans le fichier de sortie, dans le cas ou une seule prise de photo a permis d'avancer plusieurs collections        listePointsPris = []        # Parcours de toutes les coordonnees des collections validees        for collect in self.listeCollectionValidee:            for coord in collect.listeCoordonneesReussies:                # Si les coordonnees du point ne sont pas dans listePointsPris, alors on les rajoute a la liste                if not coord in listePointsPris:                    listePointsPris.append(coord)        fichier = open("fichierSortie.txt", "w")        # Ecriture du nombre total de coordonnees        fichier.write(str(len(listePointsPris))+"\n")        for coord in listePointsPris:            fichier.write(str(coord[0])+ " " + str(coord[1]) + " " + str(coord[2]) + " " + str(coord[3]) + "\n")        fichier.close()    def trierListeCoordonneesTriees(self):        """        Tri de listeCoordonneesTriees        Les coordonnees sont triees par latitude croissante et, par longitude decroissante pour les coordonnees ayant la meme latitude        """        #Tri par longitude decroissante        self.listeCoordonneesTriees.sort(key=lambda x: x[1], reverse = True)        #Puis tri par latitude croissante        self.listeCoordonneesTriees.sort(key=lambda x:x[0])        #print("listeCoordonneesTriees", self.listeCoordonneesTriees)    """    def initialiserListePhotosPossibles(self):        for satellite in self.listeSatellite:            print(satellite.getPosition())    """    def validationCollection(self, collection):        """        :param collection: La collection validee pour ne plus se preoccuper de cette collection        :type collection: Collection        """        try:            self.listeCollection.remove(collection)            self.listeCollectionValidee.append(collection)        except ValueError:            print("Collection absente de la liste")    def lancerSimulation(self) :        """        Lancement de la simulation        """        print()        print(" --- Lancement de la simulation : --- ")        print()        # chaque index de tabPointsSat = le numero du satellite concerne        # et dans chaque tabPointsSat[numSatellite], on a un tableau [[latitude, longitude]] contenant la liste des coordonnees dans l'ordre de rencontre        # Donc tabPointsSat[numSatellite][0] => [latitude, longitude] du prochain point à prendre en photo        tabPointsSatFinal = []        # tabPointsSat et tabPointsSatMid sont 2 tableaux qui servent uniquement a initialiser tabPointsSatFinal, on se servira seulement de tabPointsSatFinal par la suite        tabPointsSat = []        tabPointsSatMid = []        for i in range(0,len(self.listeSatellite)):            tabPointsSat.append([])            tabPointsSatMid.append([])            tabPointsSatFinal.append([])        for coord in self.listeCoordonneesTriees:            possible = False            for sat in self.listeSatellite:                if sat.pointDansTrajectoire(coord[0], coord[1], self.temps.getTempsTotal()):                    tabPointsSat[sat.getNumero()].append(coord)                    possible = True                if possible == False:                    lol = 0        satClone = copy.deepcopy(self.listeSatellite)        while self.temps.getTempsActuel() < self.temps.getTempsTotal():            i = 0            for s in self.listeSatellite:                for coord in tabPointsSat[i]:                    if satClone[i].photoPossible(coord) and coord not in tabPointsSatMid[i]:                        tabPointsSatMid[satClone[i].getNumero()].append(coord)                i += 1            for s in satClone:                s.calculePosition()            self.temps.incrementer()        #Donne des chemins uniques aux satellites        if len(tabPointsSatMid) > 1:            for a in range(0, len(tabPointsSatMid)):                if tabPointsSatMid[a]:                    for b in range(0, len(tabPointsSatMid)):                        if a != b:                            if tabPointsSatMid[a][0] in tabPointsSatMid[b]:                                tabPointsSatMid[b].remove(tabPointsSatMid[a][0])                    tabPointsSatFinal[a].append(tabPointsSatMid[a][0])                    del tabPointsSatMid[a][0]        else:            tabPointsSatFinal = tabPointsSatMid        self.temps.resetTemps()        while self.temps.getTempsActuel() < self.temps.getTempsTotal() and tabPointsSatFinal:            for s in self.listeSatellite:                if tabPointsSatFinal[s.getNumero()]:                    # changement de l'axe de la camera du satellite pour se rapprocher du prochain point                    s.changerOrientation(tabPointsSatFinal[s.getNumero()][0])                    if s.photoPossible(tabPointsSatFinal[s.getNumero()][0]) == True:                        # Prise de la photo: suppression du pt dans listeCoordonnees des collections qui possedent ce point et ajout de ce pt dans listeCoordonneesReussies de ces collections                        # On parcours les collections non finies                        for col in self.listeCollection:                            # Test de compatibilite du pt pouvant etre pris avec la collection col                            # Test prise de la photo  en renseignant les coordonnees du point, le tour courant et le numero du satellite concerne                            col.prisePhoto(tabPointsSatFinal[s.getNumero()][0], self.temps.getTempsActuel(), s.getNumero(), self.temps.getTempsActuel())                        # Sauvegarde de la taille initiale de listeCollection car nous supprimerons les collections validees de listeCollection en partant de la fin de la liste listeCollection                        tailleListeCollection = len(self.listeCollection)-1                        for colIndex in range (0, len(self.listeCollection)):                            collectionTestee = self.listeCollection[tailleListeCollection - colIndex]                            if collectionTestee.estVide():                                # On valide alors la collection en la supprimer de listeCollection et en la rajoutant dans listeCollectionValidee                                self.validationCollection(collectionTestee)                        print("Tour : ", self.temps.getTempsActuel()," Satellite : ",s.getNumero(), " Coordonnees pt d'interet: ",tabPointsSatFinal[s.getNumero()][0])                        # apres prise de la photo, on supprime les coordonnees de ce point dans tabPointsSatFinal, du ou des satellites correspondant                        del tabPointsSatFinal[s.getNumero()][0]                s.calculePosition()            self.temps.incrementer()        print()        print(" --- FIN --- ")        print()        print(len(self.listeCollectionValidee), "collections validees sur", len(self.listeCollection) + len(self.listeCollectionValidee), "=>", (len(self.listeCollectionValidee)/(len(self.listeCollection) + len(self.listeCollectionValidee)))*100,"%")        # Ecriture du fichier de sortie        self.fichierSortie()        """        tabPointsSat = [[]]*len(self.listeSatellite)        tabPointsSatFinal = [[]]*len(self.listeSatellite)        satClone = copy.deepcopy(self.listeSatellite)        #Rempli un tableau avec toutes les coordonnees que les satellites peuvent avoir        while self.temps.getTempsActuel() < self.temps.getTempsTotal():            for coord in self.listeCoordonneesTriees:                for cmpt in range(0, len(self.listeSatellite)):                    if satClone[cmpt].photoPossible(coord) and coord not in tabPointsSat[cmpt]:                        tabPointsSat[satClone[cmpt].getNumero()].append(coord)            for s in satClone:                s.calculePosition()            self.temps.incrementer()        print("Part 1 done")        #Clone les tableaux        for it in range(0, len(tabPointsSat)):            tabPointsSat[0] = copy.copy(tabPointsSat[0])            tabPointsSatFinal[0] = copy.copy(tabPointsSatFinal[0])        print("Part 2 done")        #Donne des chemins uniques aux satellites        if len(tabPointsSat) > 1:            for a in range(0, len(tabPointsSat)):                if tabPointsSat[a]:                    for b in range(0, len(tabPointsSat)):                        if a != b:                            if tabPointsSat[a][0] in tabPointsSat[b]:                                tabPointsSat[b].remove(tabPointsSat[a][0])                    tabPointsSatFinal[a].append(tabPointsSat[a][0])                    del tabPointsSat[a][0]        else:            tabPointsSatFinal = tabPointsSat        print("Part 3 done")        for sat in self.listeSatellite:            lati, longi = sat.getPosition()            trier = False            while not trier:                if len(tabPointsSatFinal[sat.getNumero()]) > 1:                    if tabPointsSatFinal[sat.getNumero()][len(tabPointsSatFinal)][1] >= lati:                        if tabPointsSatFinal[sat.getNumero()][0][0] < lati:                            tabPointsSatFinal[sat.getNumero()].append(tabPointsSatFinal[sat.getNumero()][0])                            del tabPointsSatFinal[sat.getNumero()][0]                        else:                            trier = True                    else:                        trier = True                else:                    trier = True        self.temps.resetTemps()        print("Part 4 done")        print(tabPointsSatFinal)        print("Total avant : ", len(tabPointsSatFinal[0]))        while self.temps.getTempsActuel() < self.temps.getTempsTotal() and tabPointsSatFinal:            for s in self.listeSatellite:                if tabPointsSatFinal[s.getNumero()]:                    s.changerOrientation(tabPointsSatFinal[s.getNumero()][0])                    if s.photoPossible(tabPointsSatFinal[s.getNumero()][0]) == True:                        print("Tour : ", self.temps.getTempsActuel()," Satellite : ",s.getNumero(), " Coordonnees pt d'interet: ",tabPointsSatFinal[s.getNumero()][0])                        del tabPointsSatFinal[s.getNumero()][0]                s.calculePosition()            self.temps.incrementer()        print("Total : ", len(tabPointsSatFinal[0]))            #Test si les photos peuvent etre prises            #Pour chaque collection            for c in self.listeCollection:                #Pour chaque coordonnees non prises en photo                for coord in c.getCoordonnees():                    #Pour chaque satellite                    for s in self.listeSatellite:                        #Si la photo est sur la trajectoire du satellite                        :                            #On supprime les coordonnees de la photo prise de toutes les collections                            for c2 in self.listeCollection:                                c2.suppressionElement(coord)                            print("Tour : ", self.temps.getTempsActuel()," Satellite : ",s.getNumero(), " Coordonnees pt d'interet: ",coord)                            c.suppressionElement(coord)            #MAJ de la position des satellites            for s in self.listeSatellite:                s.calculePosition()            #Passage au tour suivant            self.temps.incrementer()        self.fichierSortie()        """    def getListeSatellite(self):        """        Accesseur - Renvoie la liste des satellites        :return: la liste des satellites (listeSatellite)        :rtype: [Satellite]        """        return self.listeSatellite    def getListeCollection(self):        """        Accesseur - Renvoie la liste des collections        :return: la liste des collections (listeCollection)        :rtype: [Collection]        """        return self.listeCollection# initialisation d'un objet de type LanceurtpsSimulation = time.time()# Lanceur("../final_round_2016.in/forever_alone.in")# Lanceur("../final_round_2016.in/constellation.in")# Lanceur("../final_round_2016.in/overlap.in")# Lanceur("../final_round_2016.in/weekend.in")Lanceur("test.txt")tpsSimulation = (time.time() - tpsSimulation)tpsSimulationMin = int(tpsSimulation/60)tpsSimulationSec = int(tpsSimulation-(tpsSimulationMin*60))print("Duree de la simulation :", tpsSimulationMin, "min", tpsSimulationSec, "sec")