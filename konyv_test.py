# a konyvet tesztelo program...

import konyv


def szoveg_kiirasa(szoveg, margo=0, behuzas=0):
    sorhossz = 0
    elso_sor_margo = margo + behuzas
    if elso_sor_margo < 0:
        elso_sor_margo = 0
    if behuzas < 0:
        behuzas = 0
    sor = "" + " " * elso_sor_margo
    for karakter in szoveg:
        sorhossz += 1
        sor += karakter
        if sorhossz > 80:
            print(sor)
            sorhossz = 0
            sor = "" + " " * margo
    print(sor)

betuk = ["a", "b", "c", "d", "e", "f", "g", "h"]
betuk_szamokka = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
valasz = ""

k = konyv.Konyv()
konyv.beolvas("BekeX_csajozos.md", k)
cnt = 0
jelenlegi_oldalszam = 1
jelenlegi_valasz = 1
program_fut = True
elozo_valasz = "jo"

while program_fut:
    print()
    szoveg_kiirasa(k.oldalak[jelenlegi_oldalszam-1].szoveg)
    print()
    szamlalo = 0
    for val in k.oldalak[jelenlegi_oldalszam-1].valaszok:
        valasz_sor = betuk[szamlalo] + ") "
        valasz_sor += val.szoveg
        szamlalo += 1
        szoveg_kiirasa(valasz_sor, margo=5, behuzas=-3)
    print()
    if elozo_valasz == "jo":
        pass
    elif elozo_valasz == "out":
        print(">> Nincs '" + valasz + "' valasz. Valassz olyat ami van! 'Q' a kilepes.")
    elif elozo_valasz == "space":
        print(">> Nem irtal semmit. Valassz egy betut, vagy 'Q' a kilepes.")
    else:
        print(">> Honnan vetted ezt a '" + valasz + "' hulyeseget? 'Q' a kilepes, betujel a valasz...")
    valasz = input(">> ")

    if valasz == 'q' or valasz == 'x' or valasz == 'Q' or valasz == 'X':
        program_fut = False
    elif valasz in betuk:
        valasz_szama = betuk_szamokka[valasz]
        if valasz_szama < len(k.oldalak[jelenlegi_oldalszam-1].valaszok):
            jelenlegi_oldalszam = k.oldalak[jelenlegi_oldalszam-1].valaszok[valasz_szama].celoldal
            elozo_valasz = "jo"
        else:
            elozo_valasz = "out"
    elif valasz == " " or valasz == "":
        elozo_valasz = "space"
    else:
        elozo_valasz = "invalid"
    print("\n " + "-"*78 + " ")
