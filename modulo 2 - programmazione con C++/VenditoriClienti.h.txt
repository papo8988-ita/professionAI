#ifndef VENDITORI_CLIENTI_H
#define VENDITORI_CLIENTI_H

#include <string>
#include <vector>
#include <fstream>
#include "Structs.h"

class Venditore {
public:
    std::string nome;
    std::string cognome;
    std::vector<Appuntamento> appuntamenti;
    std::vector<Contratto> contratti;

    void serialize(std::ofstream& out) const {
        out << nome << "\n" << cognome << "\n";
        out << appuntamenti.size() << "\n";
        for (const auto& app : appuntamenti) {
            app.serialize(out);
        }
        out << contratti.size() << "\n";
        for (const auto& con : contratti) {
            con.serialize(out);
        }
    }

    void deserialize(std::ifstream& in) {
        std::getline(in, nome);
        std::getline(in, cognome);
        size_t appuntamentiSize, contrattiSize;
        in >> appuntamentiSize; in.ignore();
        appuntamenti.resize(appuntamentiSize);
        for (auto& app : appuntamenti) {
            app.deserialize(in);
        }
        in >> contrattiSize; in.ignore();
        contratti.resize(contrattiSize);
        for (auto& con : contratti) {
            con.deserialize(in);
        }
    }
};

class Cliente {
public:
    std::string nome;
    std::string cognome;
    std::vector<Appuntamento> appuntamenti;
    std::vector<Contratto> contratti;

    void serialize(std::ofstream& out) const {
        out << nome << "\n" << cognome << "\n";
        out << appuntamenti.size() << "\n";
        for (const auto& app : appuntamenti) {
            app.serialize(out);
        }
        out << contratti.size() << "\n";
        for (const auto& con : contratti) {
            con.serialize(out);
        }
    }

    void deserialize(std::ifstream& in) {
        std::getline(in, nome);
        std::getline(in, cognome);
        size_t appuntamentiSize, contrattiSize;
        in >> appuntamentiSize; in.ignore();
        appuntamenti.resize(appuntamentiSize);
        for (auto& app : appuntamenti) {
            app.deserialize(in);
        }
        in >> contrattiSize; in.ignore();
        contratti.resize(contrattiSize);
        for (auto& con : contratti) {
            con.deserialize(in);
        }
    }
};

#endif // VENDITORI_CLIENTI_H


