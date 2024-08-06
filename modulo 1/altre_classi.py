# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:27:09 2024

@author: JacopoBaldacci
"""
class Contatto:
    def __init__(self, nome, cognome, numero_mobile, numero_fisso, data_inserimento):
        self.nome = nome
        self.cognome = cognome
        self.numero_mobile = self.check_numero_telefono(numero_mobile, "mobile")
        self.numero_fisso = self.check_numero_telefono(numero_fisso, "fisso")
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
        
        
    def check_numero_telefono(self, numero_telefono, tipo):
        """

        Parameters
        ----------
        numero_telefono : TYPE
            DESCRIPTION.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if tipo == "fisso":
            if numero_telefono[0] != "0":
                raise Exception("il numero di telefono fisso deve iniziare con 0! ")
        if tipo == "mobile":
            if numero_telefono[0] != "3": 
                raise Exception("il numero di telefono mobile deve iniziare con 3! ")
            if len(numero_telefono) != 10:
                raise Exception("il numero di telefono mobile avere 10 cifre, di cui 3 per il prefisso! ")
        return numero_telefono
    
    