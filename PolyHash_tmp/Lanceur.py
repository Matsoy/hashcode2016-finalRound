from Temps import Tempsfrom Collection import Collectionfrom Satellite import Satelliteimport copyimport mathimport timeclass Lanceur:    """    Cette classe s'occupe de gerer les entrees sorties et de lancer la simulation    """    def __init__(self,fichier):        """        Constructeur de Lanceur        :param fichier: Le chemin du fichier contenant les donnees d'entree en caracteres ASCII        :type fichier: string        """        self.listeSatellite = []        self.listeCollection = []        self.listeCollectionValidee = []        self.listePhotosPossibles = []        # la liste de toutes les coordonnees de toutes les collections triees (par latitude croissante, si meme latitude par longitude decroissante)        self.listeCoordonneesTriees = []        self.score = 0        self.temps = None        # intervallesValues[i] est un dictionnaire de la forme {i: [[from1, to1], [from2, to2]]}        # Ce dictionnaire correspondra aux intervalles demandes pour le point de coordonnees coordKey[i] (parmi les coordonnees sur une trajectoire de satellite)        self.coordKey = []        self.intervallesValues = {}        # tours est un dictionnaire. Par exemple, tours[i] correspondra aux tours durant lequels les satellites passent sur le point coordKey[i]        self.tours = {}        # Et tours est un dictionnaire. Par exemple, tours[i] correspondra aux scores des collections possedant le point coordKey[i]        self.scores = {}        # La liste des coordonnees prises lors de la simulation        self.coordonneesPrises = []        self.nomFichier = fichier        self.lectureFichier()        self.lancerSimulation()    def lectureFichier(self):        """        Lit le fichier et en extrait:        le temps de la simulation        le nombre de satellites        les parametres initiaux des satellites:            latitude de depart            longitude de depart            vitesse de depart            changement d'orientation max d'un tour a l'autre            orientation max        le nombre d'images dans la collection        les points d'interet:            score rapporte pour la prise d'un point d'interet            latitude            longitude            intervals de prise de vue requis        """        with open(self.nomFichier,'r') as f:            #Premiere ligne pour le temps            self.temps = Temps(int(f.readline()))            #On creer les satellites            for i in range(0, int(f.readline())):                coord = f.readline().split(" ")                self.listeSatellite.append(Satellite(int(coord[0]),int(coord[1]),float(coord[2]),int(coord[3]),int(coord[4]),i))            #Ajout des collections d images            for i in range(0, int(f.readline())):                #line contient 1) Points 2) Nombre d images 3) Nombre d intervalles de temps                line = f.readline().split(" ")                images = []                temps = []                #Ajoute les coordonnees des images                for p in range(0, int(line[1])):                    images.append([int(j) for j in f.readline().strip('\n').split(" ")])                    #Parcours de images pour initialiser listeCoordonneesTriees                    for coord in images:                        #Si la coordonnees n'est pas deja dans listeCoordonneesTriees, alors on l'ajoute                        if(coord not in self.listeCoordonneesTriees):                            self.listeCoordonneesTriees.append(coord)                #Ajoute les intervalles de temps                for p in range(0, int(line[2])):                    temps.append(f.readline().strip('\n').split(" "))                #Ajoute la collection                self.listeCollection.append(Collection(line[0], images, temps))            #Tri par latitude croissante et, si meme latitude par longitude decroissante            self.trierListeCoordonneesTriees()            #Initialise la liste des photos sur la trajectoire des satellites    def fichierSortie(self):        """        Ecrit le fichier de sortie contenant:            le nombre de photos prises            pour chaque photo prise:                latitude du point d'interet                longitude du point d'interet                tour de la prise de vue                numero du satellite ayant pris la prise de vue        """        # Pour eviter les duplications dans le fichier de sortie, dans le cas ou une seule prise de photo a permis d'avancer plusieurs collections        listePointsPris = []        # Parcours de toutes les coordonnees des collections validees        for collect in self.listeCollectionValidee:            for coord in collect.listeCoordonneesReussies:                # Si les coordonnees du point ne sont pas dans listePointsPris, alors on les rajoute a la liste                if not coord in listePointsPris:                    listePointsPris.append(coord)        fichier = open("fichierSortie.out", "w")        # Ecriture du nombre total de coordonnees        fichier.write(str(len(listePointsPris))+"\n")        for coord in listePointsPris:            fichier.write(str(coord[0])+ " " + str(coord[1]) + " " + str(coord[2]) + " " + str(coord[3]) + "\n")        fichier.close()    def trierListeCoordonneesTriees(self):        """        Tri de listeCoordonneesTriees        Les coordonnees sont triees par latitude croissante et, par longitude decroissante pour les coordonnees ayant la meme latitude        """        #Tri par longitude decroissante        self.listeCoordonneesTriees.sort(key=lambda x: x[1], reverse = True)        #Puis tri par latitude croissante        self.listeCoordonneesTriees.sort(key=lambda x:x[0])        #print("listeCoordonneesTriees", self.listeCoordonneesTriees)    """    def initialiserListePhotosPossibles(self):        for satellite in self.listeSatellite:            print(satellite.getPosition())    """    def validationCollection(self, collection):        """        :param collection: La collection validee pour ne plus se preoccuper de cette collection        :type collection: Collection        """        try:            self.listeCollection.remove(collection)            self.listeCollectionValidee.append(collection)        except ValueError:            print("Collection absente de la liste")    def lancerSimulation(self) :        """        Lancement de la simulation        """        tabPolygones = []        for s in self.listeSatellite:            tabPolygones.append(s.getPolygone(self.temps.getTempsTotal()))        # True = Vitesse positive dans le polygone = tri croissant pour ce polygone        # False = Vitesse négative dans le polygone = tri decroissant pour ce polygone        tabTri = []        #Initialise les tableaux de points        #Le tableau est trié par satellite, puis par polygone de ce satellite, pour enfin avoir les points dedans        tabPointsSat = []        for i in range(0, len(self.listeSatellite)):            tabPointsSat.append([])            tabTri.append([])            croissant = True            for a in tabPolygones[i]:                if a[5][0] - a[0][0] > 0:                    croissant = True                else:                    croissant = False                tabPointsSat[i].append([])                tabTri[i].append(croissant)        #Permet de faire un tableau de polygone par "edge" (2 sommets consécutif)        newTabPolygones = []        for p in range(0, len(tabPolygones)):            newTabPolygones.append([])            for m in range(0, len(tabPolygones[p])):                newTabPolygones[p].append([])                for point in range (0, len(tabPolygones[p][m])-1):                    edge = []                    edge.append(tabPolygones[p][m][point])                    edge.append(tabPolygones[p][m][point+1])                    newTabPolygones[p][m].append(edge)                edge = []                edge.append(tabPolygones[p][m][len(tabPolygones[p][m])-1])                edge.append(tabPolygones[p][m][len(tabPolygones[p][m])-1])                newTabPolygones[p][m].append(edge)        listeCoordonnees = []        for collec in self.listeCollection:            for coord in collec.listeCoordonnees:                if coord not in listeCoordonnees:                    listeCoordonnees.append(coord)        cmpt = 0        #Regarde si un point peut être pris dans un polygone        for coord in listeCoordonnees:            for p in range(0, len(newTabPolygones)):                for m in range(0, len(newTabPolygones[p])):                        inside = self.pointDansPolygone(coord[0], coord[1], tabPolygones[p][m])                        if inside:                            cmpt += 1                            tabPointsSat[p][m].append(coord)        #Tri les points (par polygone)        for p in range(0, len(tabPointsSat)):            for l in range(0, len(tabPointsSat[p])):                if tabTri[p][l] == True:                    tabPointsSat[p][l].sort(key=lambda x:x[0])                else:                    tabPointsSat[p][l].sort(key=lambda x:x[0], reverse = True)        #Créer un tableau de point normal avec les points dans l'ordre pour chaque satellite        #Créer un tableau de point normal avec temps, il est vide        tabPointsNormal = []        tabPointsNormalTemps = []        for p in range(0, len(tabPointsSat)):            tabPointsNormal.append([])            tabPointsNormalTemps.append([])            for l in range(0, len(tabPointsSat[p])):                for point in tabPointsSat[p][l]:                    tabPointsNormal[p].append(point)        #Rempli le tableau pointNormalTemps comme le point point normal, mais avec le temps        #ex : tabPointsNormalTemps[a][p] renvoi ((1000, 2000), 250) avec a le numéro du satellite et p le point        for s in range(0, len(tabPointsNormal)):            while self.temps.getTempsActuel() < self.temps.getTempsTotal():                if len(tabPointsNormal[s]) > 0 and self.listeSatellite[s].photoPossible(tabPointsNormal[s][0]):                    tab = []                    tab.append(tabPointsNormal[s][0])                    tab.append(self.temps.getTempsActuel())                    tab2 = []                    disLat = tabPointsNormal[s][0][0] - self.listeSatellite[s].latitude                    disLong = tabPointsNormal[s][0][1] - self.listeSatellite[s].longitude                    tab2.append(disLat)                    tab2.append(disLong)                    tab.append(tab2)                    tabPointsNormalTemps[s].append(tab)                    del tabPointsNormal[s][0]                latH = self.listeSatellite[s].latitude + self.listeSatellite[s].orientationMax                latB = self.listeSatellite[s].latitude - self.listeSatellite[s].orientationMax                self.listeSatellite[s].calculePosition()                self.temps.incrementer()            self.temps.resetTemps()        #Reset la vitesse de chaque satellite pour recommencer une simulation        for a in self.listeSatellite:            a.resetVitesse()            a.resetPos()        # Suppression des collections impossibles, si des points sont en dehors de trajectoires de satellites        self.supprimerCollectionsImpossibles(tabPointsNormalTemps)        # initialisation et remplissage de self.coordIntervalles, la liste des coordonnees et de leurs intervalles de prise de photo requis par les collections        self.initDictionnaires(tabPointsNormalTemps)        # Suppression des collections dont les points ne sont pas atteignablent dans les intervalles requis        self.supprimerCollectionsImpossibles2(tabPointsNormalTemps)        # tri des satellites pour simuler d'abord les satellites passant par le moins de points        tabPointsNormalTemps = self.trierTrajectoire(tabPointsNormalTemps)        possible = False        print()        print("__ lancement de la simulation __")        for s in range(0, len(tabPointsNormalTemps)):            while self.temps.getTempsActuel() < self.temps.getTempsTotal():                #Plus de points à test                if len(tabPointsNormalTemps[s]) == 0:                    break                if possible is False and self.listeSatellite[s].rotMaxLat == 0:                    possible = self.listeSatellite[s].peutPrendrePoint(tabPointsNormalTemps[s][0][2], tabPointsNormalTemps[s][0][0], self.temps.getTempsActuel(), tabPointsNormalTemps[s][0][1])                # Test si le satellite peut prendre le point                if possible:                    if self.listeSatellite[s].prendrePhotoPossible(tabPointsNormalTemps[s][0][0]):                        self.coordonneesPrises.append(tabPointsNormalTemps[s][0][0])                        #print(tabPointsNormalTemps[s][0][0], "" , tabPointsNormalTemps[s][0][1] , "" , s)                        # boolPasDansIntervalle : Booleen || des return de prisePhoto de Collection                            # si boolPasDansIntervalle = False (i.e bon intervalle pour les collections possedant ce point), alors on supprime ce point pour tous les satellites passant par ce point dans tabPointsNormalTemps car nous n'avons plus besoin de repasser par ce point                            # si boolPasDansIntervalle = True (i.e mauvais intervalle pour au moins une collection possedant ce point), alors on ne supprime pas ce point de tabPointsNormalTemps car on devra repasser dessus pour, cette fois-ci le prendre un intervalle correspondant aux collections concernees                        boolPasDansIntervalle = False                            # On parcours les collections non finies                        for col in self.listeCollection:                            # Test de compatibilite du pt pouvant etre pris avec la collection col                            # Test prise de la photo en renseignant les coordonnees du point, le tour courant et le numero du satellite concerne                            boolPasDansIntervalle = boolPasDansIntervalle or col.prisePhoto(tabPointsNormalTemps[s][0][0], s, self.temps.getTempsActuel())                        # Validation des collections avec listeCollection vide                        # Sauvegarde de la taille initiale de listeCollection car nous supprimerons les collections validees de listeCollection en partant de la fin de la liste listeCollection                        tailleListeCollection = len(self.listeCollection)-1                        for colIndex in range (0, len(self.listeCollection)):                            collectionTestee = self.listeCollection[tailleListeCollection - colIndex]                            if collectionTestee.estVide():                                # On valide alors la collection en la supprimer de listeCollection et en la rajoutant dans listeCollectionValidee                                self.validationCollection(collectionTestee)                        # Sauvegarde du point courant avant de le supprimer du chemin du satellite s                        pointCourant = tabPointsNormalTemps[s][0][0]                        # Maintenant que le point est parcouru, on peut le supprimer du satellite correspondant pour passer au prochain au tour suivant                        del tabPointsNormalTemps[s][0]                        # Si le point est valide pour toutes les collections le contenant, alors on supprime ce point de tous les chemins des satellites                        if(boolPasDansIntervalle == False):                            tailleTabPointsNormalTemps = len(tabPointsNormalTemps)-1                            for satId in range(0, len(tabPointsNormalTemps)):                                cheminTeste = tabPointsNormalTemps[tailleTabPointsNormalTemps - satId]                                tailleCheminTeste = len(cheminTeste)-1                                for coordIndex in range (0, len(cheminTeste)):                                    coordTestee = cheminTeste[tailleCheminTeste - coordIndex]                                    if(coordTestee[0] == pointCourant):                                        del tabPointsNormalTemps[tailleTabPointsNormalTemps - satId][tailleCheminTeste - coordIndex]                        # Suppression des collections, si certaines deviennent impossibles après suppression de ce point de la trajectoire du satellite courant                        self.majCollections(tabPointsNormalTemps, pointCourant)                        self.listeSatellite[s].rotMaxLat = 0                        self.listeSatellite[s].rotMaxLong = 0                        possible = False                    else:                        self.listeSatellite[s].changerOrientationLatitude()                        self.listeSatellite[s].changerOrientationLongitude()                else:                    pointCourant = tabPointsNormalTemps[s][0][0]                    del tabPointsNormalTemps[s][0]                    # Suppression des collections, si certaines deviennent impossibles après suppression de ce point de la trajectoire du satellite courant                    self.majCollections(tabPointsNormalTemps, pointCourant)                self.listeSatellite[s].calculePosition()                self.temps.incrementer()            self.temps.resetTemps()        if((len(self.listeCollection) + len(self.listeCollectionValidee)) != 0):            print(len(self.listeCollectionValidee), "collections validees", len(self.listeCollection) + len(self.listeCollectionValidee), "=>", (len(self.listeCollectionValidee)/(len(self.listeCollection) + len(self.listeCollectionValidee)))*100,"%")        else:            print(len(self.listeCollectionValidee), "collections validees")        score = 0        for colV in self.listeCollectionValidee:            score += int(colV.getvaleur())        print("Score ==> ", score)        print()        print(len(self.coordonneesPrises), "coordonnees prises :")        print(self.coordonneesPrises)        print()        # Ecriture du fichier de sortie        self.fichierSortie()    def pointDansPolygone(self,coord_x,coord_y,poly):        taillePoly = len(poly)        # booleen si le point est dans le polygone        dedans = False        point1_x = poly[0][0]        point1_y = poly[0][1]        for cpt in range(0, taillePoly+1):            point2_x = poly[cpt % taillePoly][0]
            point2_y = poly[cpt % taillePoly][1]            if(coord_y > min(point1_y, point2_y)):                if(coord_y <= max(point1_y,point2_y)):                    if(coord_x <= max(point1_x,point2_x)):                        if(not point1_y == point2_y):                            intersectionEnX = (coord_y - point1_y) * (point2_x - point1_x) / (point2_y - point1_y) + point1_x                        if(point1_x == point2_x or coord_x <= intersectionEnX):                            dedans = not dedans            point1_x = point2_x            point1_y = point2_y        return dedans    def supprimerCollectionsImpossibles(self, listeTrajectoires):        # liste des points differents dans une trajectoire        listePtsDansTrajectoire = []        for satId in range(0, len(listeTrajectoires)):            for coordId in range(0, len(listeTrajectoires[satId])):                coord = listeTrajectoires[satId][coordId][0]                if(coord not in listePtsDansTrajectoire):                    listePtsDansTrajectoire.append(coord)        print()        print("Points (differents) dans une trajectoire :", len(listePtsDansTrajectoire))        print("Points totaux dans le fichier d'entree :", len(self.listeCoordonneesTriees))        colIdImpossibles = []        for colId in range(0, len(self.listeCollection)):            for coord in self.listeCollection[colId].listeCoordonnees:                # si le point de la collection n'est pas dans la liste des points sur une trajectoire de satellite et que l'index de la collection n'est pas deja dans colIdImpossibles                if((coord not in listePtsDansTrajectoire) and (colId not in colIdImpossibles)):                    colIdImpossibles.append(colId)        # Tri par id decroissant des collections        colIdImpossibles.reverse()        # Suppression des collections si elles contiennent un point non present dans la trajectoire d'un satellite        for colId in colIdImpossibles:            del self.listeCollection[colId]        print("Collections apres suppression des collections inutiles :", len(self.listeCollection))    def supprimerCollectionsImpossibles2(self, listeTrajectoires):        # liste des points differents dans une trajectoire        colIdImpossibles = []        for colId in range(0, len(self.listeCollection)):            for coord in self.listeCollection[colId].listeCoordonnees:                i = self.coordKey.index(coord)                intervalles = self.intervallesValues[i]                toursCourant = self.tours[i]                impossible = True                for t in toursCourant:                    for inter in intervalles:                        if(t>=int(inter[0]) and t<=int(inter[1])):                            impossible = False                if(impossible and (colId not in colIdImpossibles)):                    colIdImpossibles.append(colId)        # Tri par id decroissant des collections        colIdImpossibles.reverse()        # Suppression des collections        for colId in colIdImpossibles:            del self.listeCollection[colId]        print("Collections apres suppression des collections inutiles dans supprimerCollectionsImpossibles2:", len(self.listeCollection))    def majCollections(self, listeTrajectoires, coordSupprimee):        boolDansTrajectoire = False        # Regarde si le point supprime est encore dans la trajectoire d'un satellite        for trajectoire in listeTrajectoires:            for coord in trajectoire:                if coord[0] == coordSupprimee:                    boolDansTrajectoire = True        # Si le point supprime n'est dans aucune trajectoire de satellite        if boolDansTrajectoire == False:            colIdImpossibles = []            for colId in range(0, len(self.listeCollection)):                for coord in self.listeCollection[colId].listeCoordonnees:                    # si le point supprime est dans la collection et que l'index de la collection n'est pas deja dans colIdImpossibles                    if((coord == coordSupprimee) and (colId not in colIdImpossibles)):                        colIdImpossibles.append(colId)            # Tri par id decroissant des collections            colIdImpossibles.reverse()            # Suppression des collections si elles contiennent le point supprime            for colId in colIdImpossibles:                del self.listeCollection[colId]    def initDictionnaires(self, listeTrajectoires):        print("debut initDictionnaires, len(self.listeCollection) = ", len(self.listeCollection))        # remplissage de self.coordKey et de self.tours        for satId in range(0, len(listeTrajectoires)):            for coordId in range(0, len(listeTrajectoires[satId])):                coord = listeTrajectoires[satId][coordId][0]                tourTrouve = listeTrajectoires[satId][coordId][1]                if(coord not in self.coordKey):                    self.coordKey.append(coord)                    i = self.coordKey.index(coord)                    self.tours[i] = [tourTrouve]                else:                    i = self.coordKey.index(coord)                    self.tours[i].append(tourTrouve)        # remplissage de self.intervallesValues et de self.scores        for col in self.listeCollection:            for coord in col.listeCoordonnees:                i = self.coordKey.index(coord)                # Si le dictionnaire intervallesValues n'a pas de cle i                if self.intervallesValues.get(i) == None:                    self.intervallesValues[i] = copy.deepcopy(col.getTemps())                else:                    for intervalle in col.getTemps():                        try:                            print("col.getTemps().index(intervalle)", col.getTemps().index(intervalle), "sur" , len(col.getTemps()))                            self.intervallesValues[i].append(copy.deepcopy(intervalle))                        except MemoryError:                            print("MemoryError pour len(self.intervallesValues[i]) =", len(self.intervallesValues[i]))                # Si le dictionnaire scores n'a pas de cle i                if self.scores.get(i) == None:                    self.scores[i] = [col.getvaleur()]                else:                    self.scores[i].append(col.getvaleur())    def trierTrajectoire(self, tabPointsNormalTemps):        newTab = []        while len(tabPointsNormalTemps)>0:            plusPetiteTrajectoire = tabPointsNormalTemps[0]            for trajectoire in tabPointsNormalTemps:                if len(trajectoire) < len(plusPetiteTrajectoire):                    plusPetiteTrajectoire = trajectoire            newTab.append(plusPetiteTrajectoire)            tabPointsNormalTemps.remove(plusPetiteTrajectoire)        return newTab    def getListeSatellite(self):        """        Accesseur - Renvoie la liste des satellites        :return: la liste des satellites (listeSatellite)        :rtype: [Satellite]        """        return self.listeSatellite    def getListeCollection(self):        """        Accesseur - Renvoie la liste des collections        :return: la liste des collections (listeCollection)        :rtype: [Collection]        """        return self.listeCollection# initialisation d'un objet de type LanceurtpsSimulation = time.time()jeuDeDonnees = "constellation"print("---------------")print(jeuDeDonnees)print("---------------")Lanceur("../final_round_2016.in/"+jeuDeDonnees+".in")tpsSimulation = (time.time() - tpsSimulation)tpsSimulationMin = int(tpsSimulation/60)tpsSimulationSec = int(tpsSimulation-(tpsSimulationMin*60))print("Duree de la simulation :", tpsSimulationMin, "min", tpsSimulationSec, "sec")