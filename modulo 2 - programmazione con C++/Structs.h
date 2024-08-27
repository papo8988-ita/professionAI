#ifndef STRUCTS_H
#define STRUCTS_H

#include <string>
#include <fstream>

struct Appuntamento {
    std::string codice;
    std::string data;
    std::string luogo;
    std::string cognomeCliente;
    std::string cognomeVenditore;

    void serialize(std::ofstream& out) const {
        out << codice << "\n" << data << "\n" << luogo << "\n" << cognomeCliente << "\n" << cognomeVenditore << "\n";
    }

    void deserialize(std::ifstream& in) {
        std::getline(in, codice);
        std::getline(in, data);
        std::getline(in, luogo);
        std::getline(in, cognomeCliente);
        std::getline(in, cognomeVenditore);
    }
};

struct Contratto {
    std::string codice;
    std::string tipo;
    std::string valore;
    std::string cognomeCliente;
    std::string cognomeVenditore;

    void serialize(std::ofstream& out) const {
        out << codice << "\n" << tipo << "\n" << valore << "\n" << cognomeCliente << "\n" << cognomeVenditore << "\n";
    }

    void deserialize(std::ifstream& in) {
        std::getline(in, codice);
        std::getline(in, tipo);
        std::getline(in, valore);
        std::getline(in, cognomeCliente);
        std::getline(in, cognomeVenditore);
    }
};

#endif // STRUCTS_H

