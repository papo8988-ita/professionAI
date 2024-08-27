#include <iostream>
#include "StrutturaDati.h"

int main() {
    StrutturaDati struttura;

    // Carica i dati dal file all'avvio
    struttura.deserialize("dati.txt");

    int scelta;
    do {
        std::cout << "1. Inserisci nuovo cliente\n";
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
        std::cout << "Scegli un'opzione: ";
        std::cin >> scelta;

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
            default:
                std::cerr << "Opzione non valida.\n";
                break;
        }
    } while (scelta != 11);

    return 0;
}

