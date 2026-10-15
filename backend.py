import json
import os

QUIZZES_FILE = "quizuri.json"
LEADERBOARD_FILE = "leaderboard.txt"


# Încarcă quizurile salvate
def load_quizuri():
    if os.path.exists(QUIZZES_FILE):
        with open(QUIZZES_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return create_default_quizzes()
    return create_default_quizzes()


# Creează quizurile implicite
def create_default_quizzes():
    default_quizzes = {
        "filme": [
            {
                "intrebare": "Cine este autorul romanului '1984'?",
                "variante": {
                    "a": "Aldous Huxley",
                    "b": "George Orwell",
                    "c": "Ray Bradbury",
                    "d": "Ernest Hemingway"
                },
                "corect": "b"
            },
            {
                "intrebare": "În ce film apare personajul Jack Sparrow?",
                "variante": {
                    "a": "Star Wars",
                    "b": "Avengers",
                    "c": "Pirates of the Caribbean",
                    "d": "Gladiator"
                },
                "corect": "c"
            },
            {
                "intrebare": "'Hobbitul' este scris de:",
                "variante": {
                    "a": "J.K. Rowling",
                    "b": "J.R.R. Tolkien",
                    "c": "C.S. Lewis",
                    "d": "Stephen King"
                },
                "corect": "b"
            },
            {
                "intrebare": "Cine regizează filmul 'Inception'?",
                "variante": {
                    "a": "James Cameron",
                    "b": "Christopher Nolan",
                    "c": "Steven Spielberg",
                    "d": "Ridley Scott"
                },
                "corect": "b"
            },
            {
                "intrebare": "Care este rasa lui Sherlock Holmes?",
                "variante": {
                    "a": "Vampir",
                    "b": "Vrăjitor",
                    "c": "Om",
                    "d": "Hobbit"
                },
                "corect": "c"
            },
            {
                "intrebare": "În 'Romeo și Julieta', Romeo provine din familia:",
                "variante": {
                    "a": "Capulet",
                    "b": "Montague",
                    "c": "Stark",
                    "d": "Corleone"
                },
                "corect": "b"
            },
            {
                "intrebare": "Cine este personaj principal în 'The Hunger Games'?",
                "variante": {
                    "a": "Bella Swan",
                    "b": "Katniss Everdeen",
                    "c": "Hermione Granger",
                    "d": "Lara Croft"
                },
                "corect": "b"
            },
            {
                "intrebare": "'Mizerabilii' este scris de:",
                "variante": {
                    "a": "Victor Hugo",
                    "b": "F. Dostoevsky",
                    "c": "Charles Dickens",
                    "d": "Thomas Hardy"
                },
                "corect": "a"
            },
            {
                "intrebare": "Care este numele robotului din 'Wall-E'?",
                "variante": {
                    "a": "WALL-D",
                    "b": "WALL-E",
                    "c": "E-100",
                    "d": "EVA"
                },
                "corect": "b"
            },
            {
                "intrebare": "'Harry Potter' a fost scris de:",
                "variante": {
                    "a": "Suzanne Collins",
                    "b": "Agatha Christie",
                    "c": "J.K. Rowling",
                    "d": "Mark Twain"
                },
                "corect": "c"
            }
        ],
        "cultura generala": [
            {
                "intrebare": "Cine a pictat 'Mona Lisa'?",
                "variante": {
                    "a": "Michelangelo",
                    "b": "Leonardo da Vinci",
                    "c": "Donatello",
                    "d": "Rafael"
                },
                "corect": "b"
            },
            {
                "intrebare": "Capitala Canadei este:",
                "variante": {
                    "a": "Toronto",
                    "b": "Ottawa",
                    "c": "Vancouver",
                    "d": "Montreal"
                },
                "corect": "b"
            },
            {
                "intrebare": "Câte corzi are de obicei o chitară clasică?",
                "variante": {
                    "a": "8",
                    "b": "4",
                    "c": "6",
                    "d": "5"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce zeiță era Afrodita în mitologia greacă?",
                "variante": {
                    "a": "Războiului",
                    "b": "Frumuseții și iubirii",
                    "c": "Agriculturii",
                    "d": "Înțelepciunii"
                },
                "corect": "b"
            },
            {
                "intrebare": "Cine a scris 'Divina Comedie'?",
                "variante": {
                    "a": "Boccaccio",
                    "b": "Virgil",
                    "c": "Dante Alighieri",
                    "d": "Shakespeare"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce țară a construit Marele Zid?",
                "variante": {
                    "a": "Japonia",
                    "b": "China",
                    "c": "Coreea",
                    "d": "Mongolia"
                },
                "corect": "b"
            },
            {
                "intrebare": "Anul începerii Primului Război Mondial:",
                "variante": {
                    "a": "1914",
                    "b": "1945",
                    "c": "1866",
                    "d": "1907"
                },
                "corect": "a"
            },
            {
                "intrebare": "În ce an a avut loc Revoluția Franceză?",
                "variante": {
                    "a": "1789",
                    "b": "1776",
                    "c": "1812",
                    "d": "1830"
                },
                "corect": "a"
            },
            {
                "intrebare": "Ce artist renascentist a sculptat statuia lui David?",
                "variante": {
                    "a": "Donatello",
                    "b": "Leonardo da Vinci",
                    "c": "Michelangelo",
                    "d": "Raphael"
                },
                "corect": "c"
            },
            {
                "intrebare": "Care este cel mai înalt vârf montan din lume?",
                "variante": {
                    "a": "Mont Blanc",
                    "b": "Everest",
                    "c": "Kilimanjaro",
                    "d": "Mont McKinley (Denali)"
                },
                "corect": "b"
            },
            {
                "intrebare": "Cine a fost solistul trupei Queen?",
                "variante": {
                    "a": "Freddie Mercury",
                    "b": "Mick Jagger",
                    "c": "Elton John",
                    "d": "David Bowie"
                },
                "corect": "a"
            }
        ],
        "folclor romanesc": [
            {
                "intrebare": "Soacra lui Greuceanu era:",
                "variante": {
                    "a": "Sfânta Vineri",
                    "b": "Zâna Florilor",
                    "c": "Fata Împăratului",
                    "d": "Mama Zmeului"
                },
                "corect": "d"
            },
            {
                "intrebare": "Făt-Frumos călărește adesea:",
                "variante": {
                    "a": "Calul năzdrăvan",
                    "b": "Pegas",
                    "c": "Murgul întunericului",
                    "d": "O sabie zburătoare"
                },
                "corect": "a"
            },
            {
                "intrebare": "În ce poveste apare 'Omul de Fier'?",
                "variante": {
                    "a": "Tinerețe fără bătrânețe",
                    "b": "Prâslea cel voinic",
                    "c": "Harap-Alb",
                    "d": "Ridichea uriașă"
                },
                "corect": "b"
            },
            {
                "intrebare": "Baba Dochia simbolizează:",
                "variante": {
                    "a": "Vara",
                    "b": "Trecerea de la iarnă la primăvară",
                    "c": "Furtunile de vară",
                    "d": "Recolta"
                },
                "corect": "b"
            },
            {
                "intrebare": "'Capra cu trei iezi' este scrisă de:",
                "variante": {
                    "a": "Ion Creangă",
                    "b": "Mihai Eminescu",
                    "c": "Petre Ispirescu",
                    "d": "I.L. Caragiale"
                },
                "corect": "a"
            },
            {
                "intrebare": "Când se sărbătoresc Sânzienele?",
                "variante": {
                    "a": "pe 16 august, de Adormirea Maicii Domnului",
                    "b": "pe 24 iunie, de Sf. Ioan Botezătorul",
                    "c": "de Paște",
                    "d": "de Florii"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce rol au ursitoarele?",
                "variante": {
                    "a": "Conduc sufletele celor morți în lumea de apoi",
                    "b": "Predau magie copiilor care se nasc sub semnul norocului",
                    "c": "Stabilesc destinul unui nou-născut în numele Sorții",
                    "d": "Vindecă bolile copiilor în primele 3 zile după naștere"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce scop are ritualul Paparudei?",
                "variante": {
                    "a": "Să alunge spiritele rele din gospodării",
                    "b": "Să prevestească norocul și destinul copiilor",
                    "c": "Să aducă fertilitate fetelor de măritat",
                    "d": "Să invoce ploaia în perioade de secetă"
                },
                "corect": "d"
            },
            {
                "intrebare": "Cum se comportă Ielele în mitologie?",
                "variante": {
                    "a": "Răzbună pe cei care le deranjează sau le privesc în timpul dansului",
                    "b": "Ajută agricultorii să aibă recolte bogate",
                    "c": "Ghidează călătorii pierduți în pădure",
                    "d": "Aduc ploaia în perioade de secetă"
                },
                "corect": "a"
            },
            {
                "intrebare": "Ce simbolizează Dochia, fiica lui Decebal, în legendă?",
                "variante": {
                    "a": "Victoria romanilor asupra dacilor",
                    "b": "Legătura de neclintit a poporului de pământul și neamul său",
                    "c": "Înțelepciunea zeilor romani",
                    "d": "Primăvara și recolta bogată"
                },
                "corect": "b"
            }
        ],
        "stiinta": [
            {
                "intrebare": "Formula chimică a apei este:",
                "variante": {
                    "a": "CO₂",
                    "b": "H₂O",
                    "c": "O₂",
                    "d": "NH₃"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce organ pompează sângele?",
                "variante": {
                    "a": "Creierul",
                    "b": "Plămânii",
                    "c": "Inima",
                    "d": "Rinichii"
                },
                "corect": "c"
            },
            {
                "intrebare": "Gravitația a fost descrisă de:",
                "variante": {
                    "a": "Newton",
                    "b": "Einstein",
                    "c": "Tesla",
                    "d": "Bohr"
                },
                "corect": "a"
            },
            {
                "intrebare": "Care dintre următoarele este responsabil pentru transmiterea informațiilor genetice într-o celulă?",
                "variante": {
                    "a": "Ribozomii",
                    "b": "Mitochondriile",
                    "c": "ADN-ul",
                    "d": "Lisozomii"
                },
                "corect": "c"
            },
            {
                "intrebare": "Care este cea mai mare glandă a corpului uman?",
                "variante": {
                    "a": "Glanda tiroidă",
                    "b": "Glanda pituitară",
                    "c": "Ficatul",
                    "d": "Glanda suprarenală"
                },
                "corect": "c"
            },
            {
                "intrebare": "Care este rădăcina pătrată a lui 144?",
                "variante": {
                    "a": "10",
                    "b": "12",
                    "c": "14",
                    "d": "16"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce particulă subatomică are sarcină negativă?",
                "variante": {
                    "a": "Proton",
                    "b": "Neutron",
                    "c": "Electron",
                    "d": "Fotom"
                },
                "corect": "c"
            },
            {
                "intrebare": "Care este unitatea de măsură pentru intensitatea curentului electric?",
                "variante": {
                    "a": "Volt",
                    "b": "Watt",
                    "c": "Amper",
                    "d": "Ohm"
                },
                "corect": "c"
            },
            {
                "intrebare": "Cine a formulat legile mișcării și gravitației universale?",
                "variante": {
                    "a": "Albert Einstein",
                    "b": "Galileo Galilei",
                    "c": "Isaac Newton",
                    "d": "Nikola Tesla"
                },
                "corect": "c"
            },
            {
                "intrebare": "Care este viteza luminii în vid aproximativ?",
                "variante": {
                    "a": "300.000 km/h",
                    "b": "300.000 km/s",
                    "c": "3.000 km/s",
                    "d": "30.000 km/s"
                },
                "corect": "b"
            }
        ],
        "astronomie": [
            {
                "intrebare": "Cea mai apropiată stea de Pământ:",
                "variante": {
                    "a": "Proxima Centauri",
                    "b": "Luna",
                    "c": "Soarele",
                    "d": "Sirius"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce planetă este cunoscută drept 'Planeta Roșie'?",
                "variante": {
                    "a": "Venus",
                    "b": "Marte",
                    "c": "Mercur",
                    "d": "Saturn"
                },
                "corect": "b"
            },
            {
                "intrebare": "Calea Lactee este:",
                "variante": {
                    "a": "Cometă",
                    "b": "Galaxia noastră",
                    "c": "Constelație",
                    "d": "Nebuloasă planetară"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce planete sunt gazoase?",
                "variante": {
                    "a": "Marte și Venus",
                    "b": "Pământ și Mercur",
                    "c": "Jupiter și Saturn",
                    "d": "Pluto și Uranus"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce obiect ceresc are coadă de praf și gheață?",
                "variante": {
                    "a": "Asteroid",
                    "b": "Cometă",
                    "c": "Meteorit",
                    "d": "Lună"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce planetă are celebra 'Pată Roșie'?",
                "variante": {
                    "a": "Jupiter",
                    "b": "Uranus",
                    "c": "Venus",
                    "d": "Mercur"
                },
                "corect": "a"
            },
            {
                "intrebare": "Galaxia Andromeda este:",
                "variante": {
                    "a": "Foarte mică",
                    "b": "Cea mai apropiată galaxie spirală de noi",
                    "c": "Un satelit natural al Soarelui",
                    "d": "În centrul Universului"
                },
                "corect": "b"
            },
            {
                "intrebare": "Luna este:",
                "variante": {
                    "a": "Stea",
                    "b": "Planetă",
                    "c": "Satelit natural al Pământului",
                    "d": "Pulsar"
                },
                "corect": "c"
            },
            {
                "intrebare": "Un an-lumină măsoară:",
                "variante": {
                    "a": "Timp",
                    "b": "Spațiu (distanță parcursă de lumină într-un an)",
                    "c": "Masă",
                    "d": "Energie"
                },
                "corect": "b"
            },
            {
                "intrebare": "Cine a fost primul om în spațiu?",
                "variante": {
                    "a": "Neil Armstrong",
                    "b": "Yuri Gagarin",
                    "c": "Buzz Aldrin",
                    "d": "Alan Shepard"
                },
                "corect": "b"
            }
        ],
        "gastronomie": [
            {
                "intrebare": "Din ce țară provine preparatul paella?",
                "variante": {
                    "a": "Italia",
                    "b": "Spania",
                    "c": "Franța",
                    "d": "Portugalia"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce tip de brânză este specifică Greciei?",
                "variante": {
                    "a": "Mozzarella",
                    "b": "Roquefort",
                    "c": "Feta",
                    "d": "Cheddar"
                },
                "corect": "c"
            },
            {
                "intrebare": "În ce țară este tradițional preparatul gulașul?",
                "variante": {
                    "a": "Ungaria",
                    "b": "Polonia",
                    "c": "Cehia",
                    "d": "Austria"
                },
                "corect": "a"
            },
            {
                "intrebare": "Ce ingredient principal conține specialitatea italiană risotto alla milanese?",
                "variante": {
                    "a": "Orez",
                    "b": "Paste",
                    "c": "Porumb",
                    "d": "Cartofi"
                },
                "corect": "a"
            },
            {
                "intrebare": "Ce conține desertul Baklava, specific Europei de Sud-Est și Orientului Mijlociu?",
                "variante": {
                    "a": "Foi fine de aluat, nuci și sirop de miere",
                    "b": "Orez și lapte",
                    "c": "Mere și scorțișoară",
                    "d": "Albușuri și frișcă"
                },
                "corect": "a"
            },
            {
                "intrebare": "Ce fel de preparat este moussaka?",
                "variante": {
                    "a": "Un preparat din vinete, carne tocată și sos bechamel",
                    "b": "O salată de fructe",
                    "c": "Un desert cu miere",
                    "d": "O supă cu legume"
                },
                "corect": "a"
            },
            {
                "intrebare": "Ce băutură alcoolică este considerată tradițională în Irlanda?",
                "variante": {
                    "a": "Vin roșu",
                    "b": "Whisky irlandez",
                    "c": "Vodcă",
                    "d": "Coniac"
                },
                "corect": "b"
            },
            {
                "intrebare": "În ce țară se consumă tradițional fish and chips?",
                "variante": {
                    "a": "Marea Britanie",
                    "b": "Norvegia",
                    "c": "Franța",
                    "d": "Suedia"
                },
                "corect": "a"
            },
            {
                "intrebare": "Din ce țară provine celebra supă borscht (borș roșu)?",
                "variante": {
                    "a": "Germania",
                    "b": "Ucraina",
                    "c": "Grecia",
                    "d": "Danemarca"
                },
                "corect": "b"
            },
            {
                "intrebare": "Ce preparat este simbolul gastronomiei franțuzești?",
                "variante": {
                    "a": "Pizza",
                    "b": "Șnițel",
                    "c": "Coq au vin",
                    "d": "Gulaș"
                },
                "corect": "c"
            }
        ],
        "biologie marina": [
            {
                "intrebare": "Cel mai mare mamifer marin:",
                "variante": {
                    "a": "Orca",
                    "b": "Rechinul-balenă",
                    "c": "Balena albastră",
                    "d": "Foca"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce animal formează recife?",
                "variante": {
                    "a": "Algele",
                    "b": "Coralii",
                    "c": "Delfinii",
                    "d": "Stridiile"
                },
                "corect": "b"
            },
            {
                "intrebare": "Meduzele sunt:",
                "variante": {
                    "a": "Pești",
                    "b": "Moluste",
                    "c": "Cnidari",
                    "d": "Mamifere"
                },
                "corect": "c"
            },
            {
                "intrebare": "Ce parte a oceanului este cea mai adâncă?",
                "variante": {
                    "a": "Groapa Marianelor",
                    "b": "Groapa Timișului",
                    "c": "Polul Sud",
                    "d": "Marea Roșie"
                },
                "corect": "a"
            },
            {
                "intrebare": "Calamarul gigant are:",
                "variante": {
                    "a": "Schelet osos",
                    "b": "Cioc",
                    "c": "Aripi",
                    "d": "Cochilie externă"
                },
                "corect": "b"
            },
            {
                "intrebare": "Delfinii respiră prin:",
                "variante": {
                    "a": "Branhii",
                    "b": "Pieptene",
                    "c": "Plămâni",
                    "d": "Piele"
                },
                "corect": "c"
            },
            {
                "intrebare": "Un recif de corali este format din:",
                "variante": {
                    "a": "Plante",
                    "b": "Fosile",
                    "c": "Coloniile unor animale mici",
                    "d": "Nisip"
                },
                "corect": "c"
            },
            {
                "intrebare": "Caracatița are câte brațe?",
                "variante": {
                    "a": "6",
                    "b": "8",
                    "c": "10",
                    "d": "12"
                },
                "corect": "b"
            },
            {
                "intrebare": "Peștele-lanternă trăiește în:",
                "variante": {
                    "a": "Apele de suprafață",
                    "b": "Adâncimi mari",
                    "c": "Râuri",
                    "d": "Recif"
                },
                "corect": "b"
            },
            {
                "intrebare": "Rechinii detectează mișcarea prin:",
                "variante": {
                    "a": "Antene",
                    "b": "Linia laterală",
                    "c": "Mugete",
                    "d": "Aripioare decorative"
                },
                "corect": "b"
            }
        ]
    }

    # Salvează quizurile implicite
    save_quizuri(default_quizzes)
    return default_quizzes


# Salvează quizurile
def save_quizuri(quizuri):
    with open(QUIZZES_FILE, "w", encoding="utf-8") as f:
        json.dump(quizuri, f, ensure_ascii=False, indent=2)

# Adaugă punctajul în leaderboard
def adauga_in_leaderboard(nume, scor, total):
    with open(LEADERBOARD_FILE, "a", encoding="utf-8") as f:
        f.write(f"{nume}: {scor}/{total} - {scor * 100 / total:.1f}%\n")
# Citește leaderboard
def citeste_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return "🏆 Niciun scor înregistrat încă.\nFii primul! 🎯"
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if len(lines) > 10:
            lines = lines[-10:]  # Ultimele 10 scoruri

        # Formatează leaderboard-ul
        result = "🏆 TOP 10 SCORURI 🏆\n" + "=" * 30 + "\n"
        for i, line in enumerate(reversed(lines), 1):
            result += f"{i}. {line}"
        return result