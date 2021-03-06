from functools import total_ordering
class Temps:
    """
    Cette classe s occupe de gerer le temps (les tours) lors de la simulation
    """

    def __init__(self, tempsTotal):
        """
        Constructeur de Temps

        :param tempsTotal: Le temps total
        :type tempsTotal: int
        """

        # initialisation du temps a 0
        self.temps = 0
        self.tempsTotal = tempsTotal

    def incrementer(self):
        """
        Incrementation du temps
        """

        self.temps += 1

    def tempsEcoule(self):
        """
        Verifie si le temps est superieur (ou egal) au temps temps total

        :return: True si temps >= tempsTotal
                False sinon
        :rtype: boolean
        """

        ret = False
        if (self.temps >= self.tempsTotal):
            ret = True
        return ret

    def resetTemps(self):
        """
        Reinitialise le temps a 0
        """

        self.temps = 0

    def getTempsActuel(self):
        """
        Retourne le temps actuel

        :return: le temps actuel
        :rtype: int
        """

        return self.temps

    def getTempsTotal(self):
        """
        Retourne le temps total

        :return: le temps total
        :rtype: int
        """

        return self.tempsTotal
