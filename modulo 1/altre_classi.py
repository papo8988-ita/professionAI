# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:27:09 2024

@author: JacopoBaldacci
"""
class Contatto:
    def __init__(self, nome, cognome, numero_mobile, numero_fisso, data_inserimento):
        self.nome = nome
        self.cognome = cognome
        self.numero_mobile = numero_mobile
        self.numero_fisso = numero_fisso
        self.data_inserimento = data_inserimento
        
    def get_data(self):
        """

        Returns
        -------
        dati : TYPE
            DESCRIPTION.

        """
        dati = {"nome": self.nome,
                "cognome": self.cognome,
                "numero mobile": self.numero_mobile,
                "numero fisso": self.numero_fisso, 
                "data inserimento": self.data_inserimento}
        return dati
        
    
    