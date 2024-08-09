# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:27:09 2024

@author: JacopoBaldacci
"""
class Contatto:
    def __init__(self, data_inserimento):
        self.nome = ""
        self.cognome = ""
        self.numero_mobile = ""
        self.numero_fisso = ""
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
    
    def set_data(self, campo):
        if hasattr(self, campo):
            while True:
                valore = input(f"inserisci {campo}: ")
                if self._check_dati(campo, valore):
                    setattr(self, campo, valore)
                    return True
                else:
                    print("inserisci un valore valido")
        else:
            print("campo non valido")
            
    def set_data_da_esterno(self, campo, valore):
        if hasattr(self, campo):
            if self._check_dati(campo, valore):
                setattr(self, campo, valore)
                return True
            else:
                return False
        else:
            print("campo non valido")
        
        
    def _check_dati(self, campo, valore):
        check = True
        if campo == "nome":
            if valore == "":
                print("il nome non può essere vuoto!")
                check = False
        elif campo == "numero_mobile":
            if valore != "":
                if valore[0] != "3": 
                    print("il numero di telefono mobile deve iniziare con 3! ")
                    check = False
                if len(valore) != 10:
                    print("il numero di telefono mobile dev avere 10 cifre, di cui 3 per il prefisso! ")
                    check = False
                return check
        elif campo == "numero_fisso":
            if valore != "":
                if valore[0] != "0":
                    print("il numero di telefono fisso deve iniziare con 0! ")
                    check = False
        return check
        
