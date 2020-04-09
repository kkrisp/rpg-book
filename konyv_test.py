# a konyvet tesztelo program...

import konyv


def szoveg_kiirasa(szoveg):
    sorhossz = 0
    sor = ""
    for karakter in szoveg:
        sorhossz += 1
        sor += karakter
        if sorhossz > 80:
            print(sor)
            sorhossz = 0
            sor = ""

betuk = ["a", "b", "c", "d", "e", "f", "g", "h"]
betuk_szamokka = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
valasz = ""

k = konyv.Konyv()
konyv.beolvas("BekeX_csajozos.md", k)
cnt = 0
jelenlegi_oldalszam = 1
jelenlegi_valasz = 1
program_fut = True

while program_fut:
    print()
    szoveg_kiirasa(k.oldalak[jelenlegi_oldalszam-1].szoveg)
    print()
    szamlalo = 0
    for val in k.oldalak[jelenlegi_oldalszam-1].valaszok:
        valasz_sor = "   " + betuk[szamlalo] + ") "
        valasz_sor += val.szoveg
        szamlalo += 1
        print(valasz_sor)
    valasz = input(">> ")

    if valasz == 'q' or valasz == 'x' or valasz == 'Q' or valasz == 'X':
        program_fut = False
    elif valasz in betuk:
        valasz_szama = betuk_szamokka[valasz]
        if valasz_szama < len(k.oldalak[jelenlegi_oldalszam-1].valaszok):
            jelenlegi_oldalszam = k.oldalak[jelenlegi_oldalszam-1].valaszok[valasz_szama].celoldal
            print()
            print(" " + "-"*78 + " ")
        else:
            print("Nincs ilyen valasz...")
    else:
        print("Nincs ilyen lehetoseg...")
