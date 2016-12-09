from Temps import Tempsfrom Collection import Collectionfrom Satellite import Satelliteimport copyimport mathimport timeclass Lanceur:    """    Cette classe s'occupe de gerer les entrees sorties et de lancer la simulation    """    def __init__(self,fichier):        """        Constructeur de Lanceur        :param fichier: Le chemin du fichier contenant les donnees d'entree en caracteres ASCII        :type fichier: string        """        self.listeSatellite = []        self.listeCollection = []        self.listeCollectionValidee = []        self.listePhotosPossibles = []        # la liste de toutes les coordonnees de toutes les collections triees (par latitude croissante, si meme latitude par longitude decroissante)        self.listeCoordonneesTriees = []        self.score = 0        self.temps = None        self.nomFichier = fichier        self.lectureFichier()        self.lancerSimulation()    def lectureFichier(self):        """        Lit le fichier et en extrait:        le temps de la simulation        le nombre de satellites        les parametres initiaux des satellites:            latitude de depart            longitude de depart            vitesse de depart            changement d'orientation max d'un tour a l'autre            orientation max        le nombre d'images dans la collection        les points d'interet:            score rapporte pour la prise d'un point d'interet            latitude            longitude            intervals de prise de vue requis        """        with open(self.nomFichier,'r') as f:            #Premiere ligne pour le temps            self.temps = Temps(int(f.readline()))            #On creer les satellites            for i in range(0, int(f.readline())):                coord = f.readline().split(" ")                self.listeSatellite.append(Satellite(int(coord[0]),int(coord[1]),float(coord[2]),int(coord[3]),int(coord[4]),i))            #Ajout des collections d images            for i in range(0, int(f.readline())):                #line contient 1) Points 2) Nombre d images 3) Nombre d intervalles de temps                line = f.readline().split(" ")                images = []                temps = []                #Ajoute les coordonnees des images                for p in range(0, int(line[1])):                    images.append([int(j) for j in f.readline().strip('\n').split(" ")])                    #Parcours de images pour initialiser listeCoordonneesTriees                    for coord in images:                        #Si la coordonnees n'est pas deja dans listeCoordonneesTriees, alors on l'ajoute                        if(coord not in self.listeCoordonneesTriees):                            self.listeCoordonneesTriees.append(coord)                #Ajoute les intervalles de temps                for p in range(0, int(line[2])):                    temps.append(f.readline().strip('\n').split(" "))                #Ajoute la collection                self.listeCollection.append(Collection(line[0], images, temps))            #Tri par latitude croissante et, si meme latitude par longitude decroissante            self.trierListeCoordonneesTriees()            #Initialise la liste des photos sur la trajectoire des satellites    def fichierSortie(self):        """        Ecrit le fichier de sortie contenant:            le nombre de photos prises            pour chaque photo prise:                latitude du point d'interet                longitude du point d'interet                tour de la prise de vue                numero du satellite ayant pris la prise de vue        """        # Pour eviter les duplications dans le fichier de sortie, dans le cas ou une seule prise de photo a permis d'avancer plusieurs collections        listePointsPris = []        # Parcours de toutes les coordonnees des collections validees        for collect in self.listeCollectionValidee:            for coord in collect.listeCoordonneesReussies:                # Si les coordonnees du point ne sont pas dans listePointsPris, alors on les rajoute a la liste                if not coord in listePointsPris:                    listePointsPris.append(coord)        fichier = open("fichierSortie.txt", "w")        # Ecriture du nombre total de coordonnees        fichier.write(str(len(listePointsPris))+"\n")        for coord in listePointsPris:            fichier.write(str(coord[0])+ " " + str(coord[1]) + " " + str(coord[2]) + " " + str(coord[3]) + "\n")        fichier.close()    def trierListeCoordonneesTriees(self):        """        Tri de listeCoordonneesTriees        Les coordonnees sont triees par latitude croissante et, par longitude decroissante pour les coordonnees ayant la meme latitude        """        #Tri par longitude decroissante        self.listeCoordonneesTriees.sort(key=lambda x: x[1], reverse = True)        #Puis tri par latitude croissante        self.listeCoordonneesTriees.sort(key=lambda x:x[0])        #print("listeCoordonneesTriees", self.listeCoordonneesTriees)    """    def initialiserListePhotosPossibles(self):        for satellite in self.listeSatellite:            print(satellite.getPosition())    """    def validationCollection(self, collection):        """        :param collection: La collection validee pour ne plus se preoccuper de cette collection        :type collection: Collection        """        try:            self.listeCollection.remove(collection)            self.listeCollectionValidee.append(collection)        except ValueError:            print("Collection absente de la liste")    def lancerSimulation(self) :        """        Lancement de la simulation        """        tabPolygones = []        for s in self.listeSatellite:            tabPolygones.append(s.getPolygone(self.temps.getTempsTotal()))        """        #Creer des tableaux pour ranger les polygones        newTabPolygones = []        for e in range(0, len(tabPolygones)):            newTabPolygones.append([])            for s in range(0, len(tabPolygones[e])):                newTabPolygones[e].append([])                for m in range(0, len(tabPolygones[e][s])):                    if (m < len(tabPolygones[e][s])-1):                        newTabPolygones[e][s].append([tabPolygones[e][s][m], tabPolygones[e][s][m+1]])                    else:                        newTabPolygones[e][s].append([tabPolygones[e][s][m], tabPolygones[e][s][0]])        """        #Initialise les tableaux de points        #Le tableau est trié par satellite, puis par polygone de ce satellite, pour enfin avoir les points dedans        tabPointsSat = []        tabPointsSatFinal = []        for i in range(0, len(self.listeSatellite)):            tabPointsSat.append([])            tabPointsSatFinal.append([])            for a in tabPolygones[i]:                tabPointsSat[i].append([])                tabPointsSatFinal[i].append([])        #Permet de faire un tableau de polygone par "edge" (2 sommets consécutif)        newTabPolygones = []        for p in range(0, len(tabPolygones)):            newTabPolygones.append([])            for m in range(0, len(tabPolygones[p])):                newTabPolygones[p].append([])                for point in range (0, len(tabPolygones[p][m])-1):                    edge = []                    edge.append(tabPolygones[p][m][point])                    edge.append(tabPolygones[p][m][point+1])                    newTabPolygones[p][m].append(edge)                edge = []                edge.append(tabPolygones[p][m][len(tabPolygones[p][m])-1])                edge.append(tabPolygones[p][m][len(tabPolygones[p][m])-1])                newTabPolygones[p][m].append(edge)        cmpt = 0        #Regarde si un point peut être pris dans un polygone        for coord in self.listeCoordonneesTriees:            for p in range(0, len(newTabPolygones)):                for m in range(0, len(newTabPolygones[p])):                        inside = self.pointDansPolygone(coord[0], coord[1], tabPolygones[p][m])                        if inside:                            cmpt += 1                            tabPointsSat[p][m].append(coord)                            break        print(cmpt)        #Tri les points (par polygone)        for p in range(0, len(tabPointsSat)):            for l in range(0, len(tabPointsSat[p])):                if len(tabPointsSat[p][l]) > 0 and (l % 2 == 0) and self.listeSatellite[p].getVitesse() > 0:                    tabPointsSat[p][l].sort(key=lambda x:x[0])                elif len(tabPointsSat[p][l]) > 0 and (l % 2 != 0) and self.listeSatellite[p].getVitesse() > 0:                    tabPointsSat[p][l].sort(key=lambda x:x[0], reverse = True)                elif len(tabPointsSat[p][l]) > 0 and l % 2 == 0 and self.listeSatellite[p].getVitesse() < 0:                    tabPointsSat[p][l].sort(key=lambda x:x[0], reverse = True)                elif len(tabPointsSat[p][l]) > 0 and l % 2 != 0 and self.listeSatellite[p].getVitesse() < 0:                    tabPointsSat[p][l].sort(key=lambda x:x[0])        #Créer un tableau de point normal avec les points dans l'ordre pour chaque satellite        #Créer un tableau de point normal avec temps, il est vide        tabPointsNormal = []        tabPointsNormalTemps = []        for p in range(0, len(tabPointsSat)):            tabPointsNormal.append([])            tabPointsNormalTemps.append([])            for l in range(0, len(tabPointsSat[p])):                for point in tabPointsSat[p][l]:                    tabPointsNormal[p].append(point)        #Rempli le tableau pointNormalTemps comme le point point normal, mais avec le temps        #ex : tabPointsNormalTemps[a][p] renvoi ((1000, 2000), 250) avec a le numéro du satellite et p le point        for s in range(0, len(tabPointsNormal)):            while self.temps.getTempsActuel() < self.temps.getTempsTotal():                if tabPointsNormal[s][0] and self.listeSatellite[s].photoPossible(tabPointsNormal[s][0]):                    tab = []                    tab.append(tabPointsNormal[s][0])                    tab.append(self.temps.getTempsActuel())                    tabPointsNormalTemps[s].append(tab)                    del tabPointsNormal[s][0]                self.listeSatellite[s].calculePosition()                self.temps.incrementer()            self.temps.resetTemps()            print("wkfosk")        print(tabPointsNormalTemps)        #Donne un chemin unique        if len(tabPointsSat) > 1:            #Parcours les satellites            for a in range(0, len(tabPointsSat)):                #Parcours les polygones                for p in range(0, len(tabPointsSat[a])):                    #Si polygone non vide                    if len(tabPointsSat[a][p]) > 0:                        for b in range(0, len(tabPointsSat)):                            if a != b:                                for v in range(0, len(tabPointsSat[b])):                                    if tabPointsSat[a][p][0] in tabPointsSat[b][v]:                                        tabPointsSat[b][v].remove(tabPointsSat[a][p][0])                        tabPointsSatFinal[a][p].append(tabPointsSat[a][p][0])                        del tabPointsSat[a][p][0]        else:            tabPointsSatFinal = tabPointsSat        #Reset la vitesse de chaque satellite pour recommencer une simulation        for a in self.listeSatellite:            a.resetVitesse()        #Simulation 2 tour par tour        # print("simulation tour par tour")        # for s in range(0, len(tabPointsNormalTemps)):        #     while self.temps.getTempsActuel() < self.temps.getTempsTotal():        #         if self.listeSatellite[s].peutPrendrePoint(tabPointsNormalTemps[s][0][0], tabPointsNormalTemps[s][0][1], self.temps.getTempsActuel()):        #             # Si le satellite peut prendre le point        #             pass        #         else:        #             del tabPointsNormalTemps[s][0]        #         self.listeSatellite[s].calculePosition()        #         self.temps.incrementer()        #     self.temps.resetTemps()# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        print()        print("__ lancement de la simulation __")        for s in range(0, len(tabPointsNormalTemps)):            while self.temps.getTempsActuel() < self.temps.getTempsTotal():                # Test si le satellite peut prendre le point                if self.listeSatellite[s].peutPrendrePoint(tabPointsNormalTemps[s][0][0], tabPointsNormalTemps[s][0][1], self.temps.getTempsActuel()):                    # boolPasDansIntervalle : Booleen || des return de prisePhoto de Collection                        # si boolPasDansIntervalle = False (i.e bon intervalle pour les collections possedant ce point), alors on supprime ce point pour tous les satellites passant par ce point dans tabPointsNormalTemps car nous n'avons plus besoin de repasser par ce point                        # si boolPasDansIntervalle = True (i.e mauvais intervalle pour au moins une collection possedant ce point), alors on ne supprime pas ce point de tabPointsNormalTemps car on devra repasser dessus pour, cette fois-ci le prendre un intervalle correspondant aux collections concernees                    boolPasDansIntervalle = False                        # On parcours les collections non finies                    for col in self.listeCollection:                        # Test de compatibilite du pt pouvant etre pris avec la collection col                        # Test prise de la photo en renseignant les coordonnees du point, le tour courant et le numero du satellite concerne                        ret = ret or col.prisePhoto(tabPointsSatFinal[s.getNumero()][0], self.temps.getTempsActuel(), s.getNumero())                    # Validation des collections avec listeCollection vide                    # Sauvegarde de la taille initiale de listeCollection car nous supprimerons les collections validees de listeCollection en partant de la fin de la liste listeCollection                    tailleListeCollection = len(self.listeCollection)-1                    for colIndex in range (0, len(self.listeCollection)):                        collectionTestee = self.listeCollection[tailleListeCollection - colIndex]                        if collectionTestee.estVide():                            # On valide alors la collection en la supprimer de listeCollection et en la rajoutant dans listeCollectionValidee                            self.validationCollection(collectionTestee)                    # Sauvegarde du point courant avant de le supprimer du chemin du satellite s                    pointCourant = tabPointsNormalTemps[s][0][0]                    # Maintenant que le point est parcouru, on peut le supprimer du satellite correspondant pour passer au prochain au tour suivant                    del tabPointsNormalTemps[s][0]                    # Si le point est valide pour toutes les collections le contenant, alors on supprime ce point de tous les chemins des satellites                    if(boolPasDansIntervalle == False):                        for satId in range(0, len(tabPointsNormalTemps)):                            cheminTeste = tabPointsNormalTemps[satId]                            nbPoints = len(cheminTeste)-1                            for coordIndex in range (0, len(cheminTeste)):                                coordTestee = cheminTeste[nbPoints - coordIndex]                                if(coordTestee[0] == pointCourant):                    # del tabPointsSatFinal[s.getNumero()][0]                self.listeSatellite[s].calculePosition()                self.temps.incrementer()            self.temps.resetTemps()        print()        print(" --- FIN --- ")        print()        print(len(self.listeCollectionValidee), "collections validees sur", len(self.listeCollection) + len(self.listeCollectionValidee), "=>", (len(self.listeCollectionValidee)/(len(self.listeCollection) + len(self.listeCollectionValidee)))*100,"%")        # Ecriture du fichier de sortie        # self.fichierSortie()    def pointDansPolygone(self,x,y,poly):        n = len(poly)        dedans = False        p1x,p1y = poly[0]        for i in range(n+1):            p2x,p2y = poly[i % n]            if y > min(p1y,p2y):                if y <= max(p1y,p2y):                    if x <= max(p1x,p2x):                        if p1y != p2y:                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x                        if p1x == p2x or x <= xinters:                            dedans = not dedans            p1x,p1y = p2x,p2y        return dedans    def getListeSatellite(self):        """        Accesseur - Renvoie la liste des satellites        :return: la liste des satellites (listeSatellite)        :rtype: [Satellite]        """        return self.listeSatellite    def getListeCollection(self):        """        Accesseur - Renvoie la liste des collections        :return: la liste des collections (listeCollection)        :rtype: [Collection]        """        return self.listeCollection# initialisation d'un objet de type LanceurtpsSimulation = time.time()Lanceur("test.txt")tpsSimulation = (time.time() - tpsSimulation)tpsSimulationMin = int(tpsSimulation/60)tpsSimulationSec = int(tpsSimulation-(tpsSimulationMin*60))print()print("Duree de la simulation :", tpsSimulationMin, "min", tpsSimulationSec, "sec")