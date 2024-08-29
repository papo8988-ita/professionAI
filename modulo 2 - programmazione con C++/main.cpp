#include <iostream>
#include "StrutturaDati.h"

void mostraAiuto() {
	std::cout << "Inserisci nuovo cliente: Permette di aggiungere un nuovo cliente al sistema inserendo nome, cognome "
	          "e codice cliente.\n\n";
	std::cout << "inserisci nuovo venditore: Permette di aggiungere un nuovo venditore al sistema inserendo nome, cognome"
	          " e numero di matricola.\n\n";
	std::cout << "Inserisci nuovo appuntamento: Permette di aggiungere un nuovo appuntamento al sistema; "
	          "dobbiamo selezionare un cliente e un venditore presenti nel nostro sistema e inserire i dati "
	          "dell'appuntamento: data, luogo e stato (annulato, previsto, avvenuto). Ogni appuntamento è "
	          "codificato da un codice che deve essere univoco.\n\n";
	std::cout << "Inserisci nuovo contratto: Permette di aggiungere un nuovo contratto al sistema; "
	          "dobbiamo selezionare un cliente e un venditore presenti nel nostro sistema e inserire i dati "
	          "del contratto: tipo (moto, macchina, ecc), valore (in euro), data di inizio, durata (in mesi) "
	          "e stato (valido, scaduto, sospeso). Ogni contratto è codificato da un codice "
	          "che deve essere univoco\n\n";
	std::cout << "Cerca venditore: Consente di cercare un venditore esistente nel sistema e visualizzare"
	          "i suoi dati, i suoi appuntamenti e i contratti stipulati.\n\n";
	std::cout << "Cerca cliente: Consente di cercare un cliente esistente nel sistema e visualizzare "
	          " i suoi dati, i suoi appuntamenti e i contratti che ha stipulato.\n\n";
	std::cout << "Modifica venditore: Permette di modificare i dati di un venditore esistente e di aggiornare "
	          "lo stato di uno dei suoi contratti o di uno dei suoi appuntamenti.\n\n";
	std::cout << "Modifica cliente: Permette di modificare i dati di un cliente esistente e di aggiornare "
	          "lo stato di uno dei suoi contratti o di uno dei suoi appuntamenti.\n\n";
	std::cout << "Elimina venditore: Consente di eliminare un venditore dal sistema.\n\n";
	std::cout << "Elimina cliente: Consente di eliminare un cliente dal sistema.\n\n";
	std::cout << "Salva ed esci: Salva i dati correnti su file ed esce dal programma.\n\n\n\n";
}

int main() {
	std::cout << "+++++++++ SOFTWARE CRM PER IMPRESA ASSICURAZIONI ++++++++++ \n\n";

	StrutturaDati struttura;

	// Carica i dati dal file all'avvio
	struttura.deserialize("dati.txt");


	int scelta;
	do {
		std::cout << "\n\n1. Inserisci nuovo cliente\n";
		std::cout << "2. Inserisci nuovo venditore\n";
		std::cout << "3. Inserisci nuovo appuntamento\n";
		std::cout << "4. Inserisci nuovo contratto\n";
		std::cout << "5. Cerca venditore\n";
		std::cout << "6. Cerca cliente\n";
		std::cout << "7. Modifica venditore\n";
		std::cout << "8. Modifica cliente\n";
		std::cout << "9. Elimina venditore\n";
		std::cout << "10. Elimina cliente\n";
		std::cout << "11. Salva ed esci\n";
		std::cout << "12. Mostra aiuto\n";
		std::cout << "\nScegli un'opzione: \n";
		std::cin >> scelta;

		// Gestione delle opzioni scelte
		switch (scelta) {
		case 1:
			struttura.inserisciCliente();
			break;
		case 2:
			struttura.inserisciVenditore();
			break;
		case 3:
			struttura.inserisciAppuntamento();
			break;
		case 4:
			struttura.inserisciContratto();
			break;
		case 5:
			struttura.cercaVenditore();
			break;
		case 6:
			struttura.cercaCliente();
			break;
		case 7:
			struttura.modificaVenditore();
			break;
		case 8:
			struttura.modificaCliente();
			break;
		case 9:
			struttura.eliminaVenditore();
			break;
		case 10:
			struttura.eliminaCliente();
			break;
		case 11:
			struttura.serialize("dati.txt");
			break;
		case 12:
			mostraAiuto();
			break;
		default:
			std::cerr << "Opzione non valida.\n";
			break;
		}
	} while (scelta != 11);

	return 0;
}

