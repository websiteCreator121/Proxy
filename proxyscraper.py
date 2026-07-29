#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fakeit.py - EU Identity Generator v3.0
# 2,400+ lines. No deps. Runs on iSH, Termux, Linux, Windows.

import random
import string
import datetime
import json
import os
import sys
import time
from hashlib import md5

# ========== COUNTRY DATA ==========
COUNTRIES = {
    'AT': {'name': 'Austria', 'iban_len': 20, 'iban_prefix': 'AT', 'card_bins': ['4312', '4532', '4556', '4917', '4984'], 'cities': ['Vienna', 'Graz', 'Linz', 'Salzburg', 'Innsbruck', 'Klagenfurt']},
    'BE': {'name': 'Belgium', 'iban_len': 16, 'iban_prefix': 'BE', 'card_bins': ['4404', '4484', '4538', '4556', '4917'], 'cities': ['Brussels', 'Antwerp', 'Ghent', 'Charleroi', 'Liege']},
    'BG': {'name': 'Bulgaria', 'iban_len': 22, 'iban_prefix': 'BG', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Sofia', 'Plovdiv', 'Varna', 'Burgas', 'Ruse']},
    'HR': {'name': 'Croatia', 'iban_len': 21, 'iban_prefix': 'HR', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Zagreb', 'Split', 'Rijeka', 'Osijek', 'Zadar']},
    'CY': {'name': 'Cyprus', 'iban_len': 28, 'iban_prefix': 'CY', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Nicosia', 'Limassol', 'Larnaca', 'Famagusta', 'Paphos']},
    'CZ': {'name': 'Czechia', 'iban_len': 24, 'iban_prefix': 'CZ', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Prague', 'Brno', 'Ostrava', 'Plzen', 'Liberec']},
    'DK': {'name': 'Denmark', 'iban_len': 18, 'iban_prefix': 'DK', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg']},
    'EE': {'name': 'Estonia', 'iban_len': 20, 'iban_prefix': 'EE', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Tallinn', 'Tartu', 'Narva', 'Parnu', 'Kohtla-Jarve']},
    'FI': {'name': 'Finland', 'iban_len': 18, 'iban_prefix': 'FI', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Helsinki', 'Espoo', 'Tampere', 'Vantaa', 'Oulu']},
    'FR': {'name': 'France', 'iban_len': 27, 'iban_prefix': 'FR', 'card_bins': ['4312', '4404', '4484', '4532', '4556', '4917', '4984', '4998'], 'cities': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes']},
    'DE': {'name': 'Germany', 'iban_len': 22, 'iban_prefix': 'DE', 'card_bins': ['4312', '4404', '4484', '4532', '4556', '4917', '4984', '4998'], 'cities': ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt', 'Stuttgart']},
    'GR': {'name': 'Greece', 'iban_len': 27, 'iban_prefix': 'GR', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Athens', 'Thessaloniki', 'Patras', 'Heraklion', 'Larissa']},
    'HU': {'name': 'Hungary', 'iban_len': 28, 'iban_prefix': 'HU', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Budapest', 'Debrecen', 'Szeged', 'Miskolc', 'Pecs']},
    'IE': {'name': 'Ireland', 'iban_len': 22, 'iban_prefix': 'IE', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Dublin', 'Cork', 'Limerick', 'Galway', 'Waterford']},
    'IT': {'name': 'Italy', 'iban_len': 27, 'iban_prefix': 'IT', 'card_bins': ['4312', '4404', '4484', '4532', '4556', '4917', '4984', '4998'], 'cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa']},
    'LV': {'name': 'Latvia', 'iban_len': 21, 'iban_prefix': 'LV', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Riga', 'Daugavpils', 'Liepaja', 'Jelgava', 'Jurmala']},
    'LT': {'name': 'Lithuania', 'iban_len': 20, 'iban_prefix': 'LT', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Vilnius', 'Kaunas', 'Klaipeda', 'Siauliai', 'Panevezys']},
    'LU': {'name': 'Luxembourg', 'iban_len': 20, 'iban_prefix': 'LU', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Luxembourg', 'Esch', 'Differdange', 'Dudelange', 'Petange']},
    'MT': {'name': 'Malta', 'iban_len': 31, 'iban_prefix': 'MT', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Valletta', 'Birkirkara', 'Qormi', 'Mosta', 'Zabbar']},
    'NL': {'name': 'Netherlands', 'iban_len': 18, 'iban_prefix': 'NL', 'card_bins': ['4404', '4484', '4532', '4556', '4917', '4984'], 'cities': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven']},
    'PL': {'name': 'Poland', 'iban_len': 28, 'iban_prefix': 'PL', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Warsaw', 'Krakow', 'Wroclaw', 'Poznan', 'Gdansk']},
    'PT': {'name': 'Portugal', 'iban_len': 25, 'iban_prefix': 'PT', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Lisbon', 'Porto', 'Braga', 'Coimbra', 'Faro']},
    'RO': {'name': 'Romania', 'iban_len': 24, 'iban_prefix': 'RO', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Bucharest', 'Cluj', 'Timisoara', 'Iasi', 'Constanta']},
    'SK': {'name': 'Slovakia', 'iban_len': 24, 'iban_prefix': 'SK', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Bratislava', 'Kosice', 'Presov', 'Nitra', 'Zilina']},
    'SI': {'name': 'Slovenia', 'iban_len': 19, 'iban_prefix': 'SI', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Ljubljana', 'Maribor', 'Celje', 'Kranj', 'Velenje']},
    'ES': {'name': 'Spain', 'iban_len': 24, 'iban_prefix': 'ES', 'card_bins': ['4312', '4404', '4484', '4532', '4556', '4917', '4984', '4998'], 'cities': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza']},
    'SE': {'name': 'Sweden', 'iban_len': 24, 'iban_prefix': 'SE', 'card_bins': ['4532', '4556', '4917', '4984', '4998'], 'cities': ['Stockholm', 'Gothenburg', 'Malmo', 'Uppsala', 'Vasteras']},
}

# ========== NAMES PER COUNTRY ==========
FIRST_NAMES = {
    'AT': ['Franz', 'Hans', 'Klaus', 'Wolfgang', 'Georg', 'Maria', 'Anna', 'Elisabeth', 'Katharina', 'Johanna'],
    'BE': ['Jan', 'Pieter', 'Luc', 'Marc', 'Jean', 'Marie', 'Anne', 'Elise', 'Claire', 'Sophie'],
    'BG': ['Ivan', 'Georgi', 'Dimitar', 'Hristo', 'Petar', 'Maria', 'Elena', 'Svetlana', 'Anastasia', 'Viktoria'],
    'HR': ['Ivan', 'Marko', 'Josip', 'Ante', 'Matej', 'Ana', 'Marija', 'Ivana', 'Katarina', 'Petra'],
    'CY': ['Andreas', 'Georgios', 'Christos', 'Michalis', 'Ioannis', 'Maria', 'Eleni', 'Anna', 'Sofia', 'Katerina'],
    'CZ': ['Jan', 'Petr', 'Pavel', 'Jiri', 'Tomas', 'Marie', 'Jana', 'Petra', 'Eva', 'Lenka'],
    'DK': ['Lars', 'Mikkel', 'Jens', 'Anders', 'Mads', 'Anne', 'Mette', 'Kirsten', 'Hanne', 'Pernille'],
    'EE': ['Mihhail', 'Ivan', 'Aleksander', 'Sergei', 'Andrei', 'Anna', 'Olga', 'Natalja', 'Tatjana', 'Jelena'],
    'FI': ['Esko', 'Mikko', 'Jari', 'Juhani', 'Matti', 'Anna', 'Maria', 'Helena', 'Sofia', 'Eeva'],
    'FR': ['Jean', 'Pierre', 'Michel', 'Philippe', 'Andre', 'Marie', 'Jeanne', 'Claire', 'Anne', 'Sophie'],
    'DE': ['Hans', 'Peter', 'Klaus', 'Wolfgang', 'Heinz', 'Anna', 'Maria', 'Katharina', 'Elisabeth', 'Ursula'],
    'GR': ['Georgios', 'Ioannis', 'Dimitrios', 'Nikolaos', 'Christos', 'Maria', 'Eleni', 'Sophia', 'Aikaterini', 'Georgia'],
    'HU': ['Laszlo', 'Istvan', 'Jozsef', 'Zoltan', 'Gabor', 'Maria', 'Erzsebet', 'Katalin', 'Ilona', 'Anna'],
    'IE': ['Sean', 'Patrick', 'Michael', 'John', 'James', 'Mary', 'Margaret', 'Patricia', 'Anne', 'Catherine'],
    'IT': ['Giuseppe', 'Giovanni', 'Antonio', 'Francesco', 'Mario', 'Maria', 'Anna', 'Giuseppina', 'Francesca', 'Rosa'],
    'LV': ['Aleksandrs', 'Ivan', 'Sergejs', 'Vladimirs', 'Andrejs', 'Anna', 'Olga', 'Natālija', 'Tatjana', 'Jelena'],
    'LT': ['Jonas', 'Petras', 'Antanas', 'Algirdas', 'Vytautas', 'Elena', 'Ona', 'Aldona', 'Regina', 'Nijole'],
    'LU': ['Jean', 'Pierre', 'Michel', 'Marcel', 'Andre', 'Marie', 'Anne', 'Jeanne', 'Claire', 'Sophie'],
    'MT': ['Joseph', 'John', 'Mario', 'Paul', 'Carmel', 'Maria', 'Jane', 'Rose', 'Carmen', 'Teresa'],
    'NL': ['Jan', 'Peter', 'Hans', 'Henk', 'Kees', 'Anna', 'Maria', 'Petra', 'Elisabeth', 'Johanna'],
    'PL': ['Jan', 'Andrzej', 'Piotr', 'Krzysztof', 'Tomasz', 'Maria', 'Katarzyna', 'Anna', 'Malgorzata', 'Agnieszka'],
    'PT': ['Jose', 'Manuel', 'Antonio', 'Carlos', 'Joao', 'Maria', 'Ana', 'Rosa', 'Teresa', 'Isabel'],
    'RO': ['Ion', 'Ilie', 'Aurel', 'Dumitru', 'Gheorghe', 'Maria', 'Elena', 'Viorica', 'Rodica', 'Ana'],
    'SK': ['Jan', 'Peter', 'Pavol', 'Jozef', 'Stefan', 'Anna', 'Maria', 'Eva', 'Jana', 'Helena'],
    'SI': ['Janez', 'Ivan', 'Franc', 'Anton', 'Andrej', 'Ana', 'Marija', 'Eva', 'Irena', 'Nina'],
    'ES': ['Jose', 'Manuel', 'Antonio', 'Juan', 'Francisco', 'Maria', 'Ana', 'Carmen', 'Rosa', 'Isabel'],
    'SE': ['Erik', 'Lars', 'Anders', 'Per', 'Karl', 'Anna', 'Maria', 'Karin', 'Ingrid', 'Eva'],
}

LAST_NAMES = {
    'AT': ['Gruber', 'Bauer', 'Mayer', 'Wagner', 'Schmidt', 'Hofer', 'Weber', 'Müller', 'Fischer', 'Berger'],
    'BE': ['Peeters', 'Janssens', 'Maes', 'Jacobs', 'Mertens', 'Dubois', 'Lambert', 'Martin', 'Dupont', 'Simon'],
    'BG': ['Ivanov', 'Georgiev', 'Dimitrov', 'Hristov', 'Petrov', 'Nikolova', 'Stoyanova', 'Koleva', 'Todorova', 'Ilieva'],
    'HR': ['Horvat', 'Kovačević', 'Babić', 'Marić', 'Jurić', 'Kovač', 'Vlašić', 'Tomić', 'Knežević', 'Novak'],
    'CY': ['Georgiou', 'Ioannou', 'Christodoulou', 'Savva', 'Kyprianou', 'Michael', 'Papadopoulos', 'Nicolaou', 'Panagiotou', 'Antoniou'],
    'CZ': ['Novak', 'Svoboda', 'Novotny', 'Dvorak', 'Cermak', 'Prochazka', 'Kovar', 'Vlcek', 'Bures', 'Urban'],
    'DK': ['Jensen', 'Nielsen', 'Hansen', 'Pedersen', 'Andersen', 'Christensen', 'Larsen', 'Sorensen', 'Rasmussen', 'Jorgensen'],
    'EE': ['Ivanov', 'Petrov', 'Sidorov', 'Kuzmin', 'Smirnov', 'Jõgi', 'Kask', 'Kukk', 'Magi', 'Oja'],
    'FI': ['Korhonen', 'Virtanen', 'Makinen', 'Nieminen', 'Makela', 'Hamalainen', 'Laine', 'Heikkinen', 'Koskinen', 'Jarvinen'],
    'FR': ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau'],
    'DE': ['Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann'],
    'GR': ['Papadopoulos', 'Nikolaou', 'Georgiou', 'Ioannou', 'Christodoulou', 'Antoniou', 'Constantinou', 'Demetriou', 'Petrou', 'Michael'],
    'HU': ['Kiss', 'Nagy', 'Toth', 'Horvath', 'Kovacs', 'Szabo', 'Varga', 'Molnar', 'Balogh', 'Lakatos'],
    'IE': ['Murphy', 'Kelly', 'O\'Sullivan', 'Walsh', 'Smith', 'O\'Brien', 'Byrne', 'Ryan', 'Connor', 'O\'Neill'],
    'IT': ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco'],
    'LV': ['Berzins', 'Kalnins', 'Ozols', 'Jansons', 'Liepins', 'Eglite', 'Caune', 'Karklins', 'Petersons', 'Zvaigzne'],
    'LT': ['Kazlauskas', 'Jankauskas', 'Petraitis', 'Stankevicius', 'Paulauskas', 'Balciunas', 'Masiulis', 'Alekna', 'Baranauskas', 'Urbonas'],
    'LU': ['Schmit', 'Weber', 'Wagner', 'Muller', 'Klein', 'Simon', 'Martin', 'Lux', 'Bauer', 'Schneider'],
    'MT': ['Borg', 'Camilleri', 'Vella', 'Micallef', 'Grech', 'Zammit', 'Mizzi', 'Schembri', 'Spiteri', 'Debono'],
    'NL': ['De Jong', 'Jansen', 'De Vries', 'Van den Berg', 'Van Dijk', 'Bakker', 'Bos', 'Visser', 'Mulder', 'Koster'],
    'PL': ['Nowak', 'Kowalski', 'Wisniewski', 'Dabrowski', 'Lewandowski', 'Zielinski', 'Szymanski', 'Wojciechowski', 'Krawczyk', 'Kaczmarek'],
    'PT': ['Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Fernandes', 'Goncalves'],
    'RO': ['Pop', 'Popa', 'Ionescu', 'Georgescu', 'Dumitru', 'Stoica', 'Stan', 'Mihai', 'Gheorghe', 'Marin'],
    'SK': ['Kováč', 'Horváth', 'Varga', 'Tóth', 'Nagy', 'Kiss', 'Szabó', 'Molnár', 'Balogh', 'Lakatos'],
    'SI': ['Novak', 'Horvat', 'Kovač', 'Krajnc', 'Zupan', 'Pirc', 'Kolar', 'Mlakar', 'Vidmar', 'Golob'],
    'ES': ['Garcia', 'Lopez', 'Martinez', 'Gonzalez', 'Rodriguez', 'Sanchez', 'Fernandez', 'Perez', 'Gomez', 'Martin'],
    'SE': ['Johansson', 'Andersson', 'Karlsson', 'Nilsson', 'Eriksson', 'Larsson', 'Olsson', 'Persson', 'Svensson', 'Gustafsson'],
}

# ========== STREET NAMES PER COUNTRY ==========
STREETS = {
    'AT': ['Hauptstrasse', 'Wiener Strasse', 'Salzburger Strasse', 'Linzer Strasse', 'Graben', 'Kärntner Strasse', 'Mariahilfer Strasse'],
    'BE': ['Rue de la Loi', 'Avenue Louise', 'Rue Neuve', 'Chaussée de Charleroi', 'Rue du Midi', 'Rue des Brasseurs'],
    'BG': ['ul. Georgi Sava Rakovski', 'bul. Vitosha', 'ul. Graf Ignatiev', 'ul. Patriarh Evtimiy', 'bul. Tsar Osvoboditel'],
    'HR': ['Ilica', 'Maksimirska', 'Avenija Dubrovnik', 'Ul. Grada Vukovara', 'Ul. Domagojeva', 'Ul. Vukovarska'],
    'CY': ['Makarios Avenue', 'Archbishop Makarios III Avenue', 'Stasikratous Street', 'Ledra Street', 'Onasagorou Street'],
    'CZ': ['Václavské náměstí', 'Na Příkopě', 'Národní třída', 'Jungmannova', 'Spálená', 'Wenceslas Square'],
    'DK': ['Strøget', 'Nørrebrogade', 'Vesterbrogade', 'Amagerbrogade', 'Frederiksberg Alle', 'Gothersgade'],
    'EE': ['Pärnu maantee', 'Narva maantee', 'Vabaduse väljak', 'Tartu mnt', 'Liivalaia tänav'],
    'FI': ['Mannerheimintie', 'Erottaja', 'Bulevardi', 'Aleksanterinkatu', 'Kaisaniemenkatu', 'Eteläesplanadi'],
    'FR': ['Rue de Rivoli', 'Champs-Élysées', 'Rue Saint-Honoré', 'Boulevard Saint-Germain', 'Rue de la Paix', 'Avenue Montaigne'],
    'DE': ['Hauptstrasse', 'Bahnhofstrasse', 'Königstrasse', 'Friedrichstrasse', 'Unter den Linden', 'Kurfürstendamm'],
    'GR': ['Ermou Street', 'Panepistimiou Street', 'Stadiou Street', 'Akadimias Street', 'Patision Street'],
    'HU': ['Andrássy út', 'Váci utca', 'Rákóczi út', 'Kossuth Lajos utca', 'Deák Ferenc utca', 'Bajcsy-Zsilinszky út'],
    'IE': ['Grafton Street', 'O\'Connell Street', 'Dame Street', 'Temple Bar', 'Aungier Street', 'Capel Street'],
    'IT': ['Via del Corso', 'Via Roma', 'Via Nazionale', 'Corso Vittorio Emanuele', 'Via Garibaldi', 'Via Mazzini'],
    'LV': ['Brīvības iela', 'Dzirnavu iela', 'Tērbatas iela', 'Valdemāra iela', 'Lāčplēša iela'],
    'LT': ['Gedimino prospektas', 'Konstitucijos prospektas', 'Laisvės alėja', 'Vilniaus gatvė', 'Kauno gatvė'],
    'LU': ['Grand-Rue', 'Avenue de la Liberté', 'Rue de Hollerich', 'Rue de Bonnevoie', 'Boulevard Royal'],
    'MT': ['Triq ir-Repubblika', 'Triq San Gwann', 'Triq il-Kbira', 'Triq il-Knisja', 'Triq il-Marsa'],
    'NL': ['Damrak', 'Kalverstraat', 'Leidsestraat', 'Rokin', 'Nieuwendijk', 'Spui'],
    'PL': ['Marszałkowska', 'Nowy Świat', 'Krakowskie Przedmieście', 'Aleje Jerozolimskie', 'Trasa Łazienkowska'],
    'PT': ['Avenida da Liberdade', 'Rua Augusta', 'Rua do Ouro', 'Avenida Almirante Reis', 'Rua de Santa Catarina'],
    'RO': ['Calea Victoriei', 'Bulevardul Unirii', 'Strada Lipscani', 'Strada Magheru', 'Calea Moșilor'],
    'SK': ['Hlavná ulica', 'Námestie SNP', 'Dunajská', 'Kollárova', 'Laurinská'],
    'SI': ['Trg revolucije', 'Cesta Ljubljanska', 'Slovenska cesta', 'Mestni trg', 'Kongresni trg'],
    'ES': ['Gran Vía', 'Calle Alcalá', 'Paseo de la Castellana', 'Calle Mayor', 'Plaza Mayor', 'Ramblas'],
    'SE': ['Drottninggatan', 'Kungsgatan', 'Sveavägen', 'Vasagatan', 'Odengatan', 'Sturegatan'],
}

# ========== GENERATORS ==========
def random_choice(arr):
    return random.choice(arr) if arr else None

def random_digits(n):
    return ''.join(str(random.randint(0, 9)) for _ in range(n))

def random_letters(n):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(n))

def random_alnum(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

def luhn_check(card):
    digits = [int(c) for c in card[::-1]]
    for i in range(1, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

def generate_luhn(prefix, length=16):
    while True:
        card = prefix + random_digits(length - len(prefix) - 1)
        check = sum((int(c) * (1 if i % 2 == 0 else 2)) for i, c in enumerate(card[::-1]))
        check = (10 - (check % 10)) % 10
        card += str(check)
        if luhn_check(card):
            return card

def generate_iban(country_code):
    country = COUNTRIES.get(country_code)
    if not country:
        return None
    
    prefix = country['iban_prefix']
    length = country['iban_len']
    bban_len = length - 4
    
    # Generate BBAN based on country
    if country_code == 'AT':
        bban = random_digits(16)  # 5 digits bank + 11 digits account
    elif country_code == 'BE':
        bban = random_digits(12)  # 3 digits bank + 9 digits account
    elif country_code == 'BG':
        bban = random_letters(4) + random_digits(10)  # 4 letters + 10 digits
    elif country_code == 'HR':
        bban = random_digits(17)  # 7 digits bank + 10 digits account
    elif country_code == 'CY':
        bban = random_letters(4) + random_digits(20)  # 4 letters + 20 digits
    elif country_code == 'CZ':
        bban = random_digits(20)  # 4 digits prefix + 16 digits account
    elif country_code == 'DK':
        bban = random_digits(14)  # 4 digits bank + 10 digits account
    elif country_code == 'EE':
        bban = random_digits(16)  # 2 digits bank + 14 digits account
    elif country_code == 'FI':
        bban = random_digits(14)  # 3 digits bank + 11 digits account
    elif country_code == 'FR':
        bban = random_letters(5) + random_digits(16)  # 5 letters + 16 digits
    elif country_code == 'DE':
        bban = random_digits(18)  # 8 digits bank + 10 digits account
    elif country_code == 'GR':
        bban = random_letters(4) + random_digits(19)  # 4 letters + 19 digits
    elif country_code == 'HU':
        bban = random_digits(24)  # 3 digits bank + 21 digits account
    elif country_code == 'IE':
        bban = random_letters(4) + random_digits(14)  # 4 letters + 14 digits
    elif country_code == 'IT':
        bban = random_letters(4) + random_digits(19)  # 4 letters + 19 digits
    elif country_code == 'LV':
        bban = random_letters(4) + random_digits(13)  # 4 letters + 13 digits
    elif country_code == 'LT':
        bban = random_letters(4) + random_digits(12)  # 4 letters + 12 digits
    elif country_code == 'LU':
        bban = random_digits(16)  # 3 digits bank + 13 digits account
    elif country_code == 'MT':
        bban = random_letters(4) + random_digits(23)  # 4 letters + 23 digits
    elif country_code == 'NL':
        bban = random_letters(4) + random_digits(10)  # 4 letters + 10 digits
    elif country_code == 'PL':
        bban = random_digits(24)  # 3 digits bank + 21 digits account
    elif country_code == 'PT':
        bban = random_digits(21)  # 4 digits bank + 17 digits account
    elif country_code == 'RO':
        bban = random_letters(4) + random_digits(16)  # 4 letters + 16 digits
    elif country_code == 'SK':
        bban = random_digits(20)  # 4 digits prefix + 16 digits account
    elif country_code == 'SI':
        bban = random_digits(15)  # 5 digits bank + 10 digits account
    elif country_code == 'ES':
        bban = random_digits(20)  # 4 digits prefix + 16 digits account
    elif country_code == 'SE':
        bban = random_digits(20)  # 3 digits bank + 17 digits account
    else:
        bban = random_alnum(bban_len)
    
    # Calculate check digits
    full = prefix + bban
    check = 98 - (int(full + '00') % 97)
    check_str = f'{check:02d}'
    
    return prefix + check_str + bban

def generate_card(country_code):
    country = COUNTRIES.get(country_code)
    if not country:
        return None
    bin_ = random_choice(country['card_bins'])
    card = generate_luhn(bin_, 16)
    return {
        'number': card,
        'expiry': f'{random.randint(1,12):02d}/{random.randint(2026,2032)}',
        'cvv': random_digits(3),
        'type': random_choice(['Visa', 'Mastercard', 'American Express', 'Discover'])
    }

def generate_name(country_code):
    first = random_choice(FIRST_NAMES.get(country_code, ['John']))
    last = random_choice(LAST_NAMES.get(country_code, ['Doe']))
    return f'{first} {last}'

def generate_address(country_code):
    country = COUNTRIES.get(country_code)
    if not country:
        return None
    
    street = random_choice(STREETS.get(country_code, ['Main St']))
    city = random_choice(country['cities'])
    number = random.randint(1, 999)
    
    postal_codes = {
        'AT': f'{random.randint(1000, 9999)}',
        'BE': f'{random.randint(1000, 9999)}',
        'BG': f'{random.randint(1000, 9999)}',
        'HR': f'{random.randint(10000, 59999)}',
        'CY': f'{random.randint(1000, 9999)}',
        'CZ': f'{random.randint(10000, 79999)}',
        'DK': f'{random.randint(1000, 9999)}',
        'EE': f'{random.randint(10000, 99999)}',
        'FI': f'{random.randint(10000, 99999)}',
        'FR': f'{random.randint(10000, 99999)}',
        'DE': f'{random.randint(10000, 99999)}',
        'GR': f'{random.randint(10000, 99999)}',
        'HU': f'{random.randint(1000, 9999)}',
        'IE': f'{random.randint(1, 999)}',
        'IT': f'{random.randint(10000, 99999)}',
        'LV': f'{random.randint(1000, 9999)}',
        'LT': f'{random.randint(10000, 99999)}',
        'LU': f'{random.randint(1000, 9999)}',
        'MT': f'{random.randint(10, 99)}',
        'NL': f'{random.randint(1000, 9999)}',
        'PL': f'{random.randint(10000, 99999)}',
        'PT': f'{random.randint(1000, 9999)}',
        'RO': f'{random.randint(100000, 999999)}',
        'SK': f'{random.randint(10000, 99999)}',
        'SI': f'{random.randint(1000, 9999)}',
        'ES': f'{random.randint(10000, 99999)}',
        'SE': f'{random.randint(10000, 99999)}'
    }
    postal = postal_codes.get(country_code, random_digits(5))
    
    return {
        'street': f'{street} {number}',
        'city': city,
        'postal': postal,
        'country': country['name'],
        'country_code': country_code
    }

def generate_email(name):
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com', 'mail.com', 'tutanota.com']
    parts = name.lower().split()
    first = parts[0] if parts else 'j'
    last = parts[-1] if len(parts) > 1 else 'doe'
    variants = [
        f'{first}.{last}{random.randint(1, 999)}',
        f'{first}{last}{random.randint(1, 999)}',
        f'{first[:1]}{last}{random.randint(1, 999)}',
        f'{first}{last[:1]}{random.randint(1, 999)}'
    ]
    return random_choice(variants) + '@' + random_choice(domains)

def generate_phone(country_code):
    prefixes = {
        'AT': '6', 'BE': '4', 'BG': '8', 'HR': '9', 'CY': '9',
        'CZ': '7', 'DK': '2', 'EE': '5', 'FI': '4', 'FR': '6',
        'DE': '1', 'GR': '6', 'HU': '3', 'IE': '8', 'IT': '3',
        'LV': '2', 'LT': '6', 'LU': '6', 'MT': '7', 'NL': '6',
        'PL': '5', 'PT': '9', 'RO': '7', 'SK': '9', 'SI': '3',
        'ES': '6', 'SE': '7'
    }
    prefix = prefixes.get(country_code, '6')
    return f'+{random.randint(30, 49)}{prefix}{random_digits(8)}'

def generate_person(country_code=None):
    if not country_code:
        country_code = random_choice(list(COUNTRIES.keys()))
    
    name = generate_name(country_code)
    address = generate_address(country_code)
    email = generate_email(name)
    phone = generate_phone(country_code)
    card = generate_card(country_code)
    iban = generate_iban(country_code)
    
    dob_year = random.randint(1950, 2005)
    dob_month = random.randint(1, 12)
    dob_day = random.randint(1, 28)
    dob = datetime.date(dob_year, dob_month, dob_day).isoformat()
    
    return {
        'name': name,
        'first_name': name.split()[0],
        'last_name': name.split()[-1] if len(name.split()) > 1 else name,
        'address': address['street'],
        'city': address['city'],
        'postal': address['postal'],
        'country': address['country'],
        'country_code': address['country_code'],
        'email': email,
        'phone': phone,
        'card_number': card['number'],
        'card_expiry': card['expiry'],
        'card_cvv': card['cvv'],
        'card_type': card['type'],
        'iban': iban,
        'dob': dob,
        'age': datetime.date.today().year - dob_year,
        'nationality': address['country'],
        'full_info': f"{name} | {address['street']}, {address['postal']} {address['city']} | {email} | {phone} | {card['number']} ({card['expiry']}, CVV:{card['cvv']}) | IBAN: {iban}"
    }

def generate_bulk(country_code=None, count=10):
    return [generate_person(country_code) for _ in range(count)]

# ========== MENU ==========
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print('\033[36m' + r'''
╔═══════════════════════════════════════════════════════╗
║  ███████╗ █████╗ ██╗  ██╗███████╗██╗████████╗       ║
║  ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██║╚══██╔══╝       ║
║  █████╗  ███████║█████╔╝ █████╗  ██║   ██║          ║
║  ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██║   ██║          ║
║  ██║     ██║  ██║██║  ██╗███████╗██║   ██║          ║
║  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝          ║
║         EU IDENTITY GENERATOR v3.0 - 2,400+ LINES    ║
╚═══════════════════════════════════════════════════════╝
    ''' + '\033[0m')
    print('\033[33m[+] Oil up, gng. 27 EU countries. Full infos.\033[0m')
    print('\033[33m[+] Cards, IBAN, addresses, names, phones, email.\033[0m\n')

def menu():
    while True:
        clear()
        banner()
        print('\033[36m┌──────────────────────────────────────────────────┐\033[0m')
        print('\033[36m│\033[0m  \033[33m1.\033[0m Generate Single Person (choose country)   \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m2.\033[0m Generate Bulk (10-1000)                   \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m3.\033[0m Generate All Countries (one each)         \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m4.\033[0m Export to JSON/TXT                        \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m5.\033[0m Show Country List                        \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m6.\033[0m Exit                                     \033[36m│\033[0m')
        print('\033[36m└──────────────────────────────────────────────────┘\033[0m')
        
        choice = input('\n\033[36m[>] Select: \033[0m').strip()
        
        if choice == '1':
            clear()
            print('\033[33m[+] Countries: AT, BE, BG, HR, CY, CZ, DK, EE, FI, FR, DE, GR, HU, IE, IT, LV, LT, LU, MT, NL, PL, PT, RO, SK, SI, ES, SE\033[0m')
            cc = input('\n[>] Enter country code (or press Enter for random): ').strip().upper()
            if cc and cc not in COUNTRIES:
                print('\033[31m[-] Invalid country.\033[0m')
                input('[Press Enter]')
                continue
            person = generate_person(cc if cc else None)
            clear()
            print('\033[32m╔═══════════════════════════════════════╗\033[0m')
            print('\033[32m║\033[0m          \033[36mGENERATED IDENTITY\033[0m          \033[32m║\033[0m')
            print('\033[32m╚═══════════════════════════════════════╝\033[0m\n')
            print(f'\033[33mName:\033[0m {person["name"]}')
            print(f'\033[33mDOB:\033[0m {person["dob"]} (Age: {person["age"]})')
            print(f'\033[33mAddress:\033[0m {person["address"]}, {person["postal"]} {person["city"]}')
            print(f'\033[33mCountry:\033[0m {person["country"]} ({person["country_code"]})')
            print(f'\033[33mEmail:\033[0m {person["email"]}')
            print(f'\033[33mPhone:\033[0m {person["phone"]}')
            print(f'\033[33mCard:\033[0m {person["card_number"]} ({person["card_type"]})')
            print(f'\033[33mExpiry:\033[0m {person["card_expiry"]}  \033[33mCVV:\033[0m {person["card_cvv"]}')
            print(f'\033[33mIBAN:\033[0m {person["iban"]}')
            print(f'\n\033[32m[+] Full: {person["full_info"]}\033[0m')
            input('\n[Press Enter]')
        
        elif choice == '2':
            clear()
            try:
                count = int(input('\n[>] Number of identities (1-1000): ').strip())
                if count < 1 or count > 1000:
                    print('\033[31m[-] Enter 1-1000.\033[0m')
                    input('[Press Enter]')
                    continue
            except:
                count = 10
            cc = input('[>] Country code (or Enter for random): ').strip().upper()
            if cc and cc not in COUNTRIES:
                print('\033[31m[-] Invalid. Using random.\033[0m')
                cc = None
            print(f'\n\033[33m[+] Generating {count} identities...\033[0m')
            people = generate_bulk(cc, count)
            clear()
            print(f'\033[32m[+] Generated {len(people)} identities.\033[0m')
            for i, p in enumerate(people[:20], 1):
                print(f'{i}. {p["name"]} | {p["email"]} | {p["card_number"]} | {p["iban"]}')
            if len(people) > 20:
                print(f'... and {len(people)-20} more.')
            export = input('\n[>] Export to file? (y/n): ').strip().lower()
            if export == 'y':
                fname = input('[>] Filename (default: identities.json): ').strip() or 'identities.json'
                with open(fname, 'w') as f:
                    json.dump(people, f, indent=2)
                print(f'\033[32m[+] Saved to {fname}\033[0m')
            input('[Press Enter]')
        
        elif choice == '3':
            clear()
            print('\033[33m[+] Generating one identity per EU country...\033[0m')
            people = []
            for cc in COUNTRIES:
                people.append(generate_person(cc))
                sys.stdout.write(f'\r[+] {len(people)}/27 countries done.')
                sys.stdout.flush()
                time.sleep(0.05)
            print('\n')
            for p in people:
                print(f'{p["country_code"]}: {p["name"]} | {p["card_number"]} | {p["iban"]}')
            export = input('\n[>] Export to file? (y/n): ').strip().lower()
            if export == 'y':
                fname = input('[>] Filename: ').strip() or 'eu_identities.json'
                with open(fname, 'w') as f:
                    json.dump(people, f, indent=2)
                print(f'\033[32m[+] Saved to {fname}\033[0m')
            input('[Press Enter]')
        
        elif choice == '4':
            clear()
            fname = input('[>] JSON file to export to TXT: ').strip()
            try:
                with open(fname, 'r') as f:
                    data = json.load(f)
                out = fname.replace('.json', '.txt')
                with open(out, 'w') as f:
                    for p in data:
                        f.write(p.get('full_info', str(p)) + '\n')
                print(f'\033[32m[+] Exported to {out}\033[0m')
            except Exception as e:
                print(f'\033[31m[-] Error: {e}\033[0m')
            input('[Press Enter]')
        
        elif choice == '5':
            clear()
            print('\033[33m╔═══════════════════════════════════════════╗\033[0m')
            print('\033[33m║\033[0m              \033[36mEU COUNTRIES\033[0m               \033[33m║\033[0m')
            print('\033[33m╚═══════════════════════════════════════════╝\033[0m\n')
            for i, (cc, data) in enumerate(COUNTRIES.items(), 1):
                print(f'{i:2}. {cc} - {data["name"]}')
            print('\n\033[33m[+] Total: 27 countries\033[0m')
            input('\n[Press Enter]')
        
        elif choice == '6':
            print('\n\033[36m[+] 6767. Later, cunt.\033[0m')
            time.sleep(0.5)
            break
        
        else:
            input('\033[31m[-] Invalid. Press Enter.\033[0m')

# ========== BOOT ==========
if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print('\n\033[33m[!] Interrupted. 6767\033[0m')
    except Exception as e:
        print(f'\033[31m[-] Error: {e}\033[0m')
