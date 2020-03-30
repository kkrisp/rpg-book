# read mode
#  0 - nincs
#  1 - kaland cim
#  2 - fejezet cim
#  3 - oldalszam/cim
#  4 - oldal szoveg
#  5 - valasz kriterium
#  6 - valasz szoveg
#  7 - valasz celoldal

def takarit(szovegsor):
    utolso_karakter = szovegsor[-1:]
    while utolso_karakter == "\n":
        szovegsor = szovegsor[:-1]
        utolso_karakter = szovegsor[-1:]
    return szovegsor



def beolvas(faljnev, konyv):
    f = open(faljnev, 'r')
    k_elozo = "0"
    k = "0"
    maxpage = 100
    read_mode = 0
    kaland_cim = ""
    oldalszam = ""
    oldal_szoveg = ""
    valasz_szoveg = ""
    ide_vezet = ""
    feltetel = ""
    feltetelek = []
    while k:
        k_elozo = k
        k = f.read(1)

        if k == "#":
            if read_mode == 4:
                oldal_szoveg = takarit(oldal_szoveg)
                konyv.oldalak[int(oldalszam) - 1].szoveg = oldal_szoveg
            oldalszam = ""
            if k_elozo == "#":
                read_mode += 1
                continue
            else:
                read_mode = 1
                continue

        elif k == ">":
            konyv.oldalak[int(oldalszam) - 1].szoveg = oldal_szoveg
            feltetelek = []
            feltetel = ""
            k = f.read(1)  # space
            k = f.read(1)  # *
            k = f.read(1)  # space
            k = f.read(1)  # [ or text
            if k == "[":
                read_mode = 5
            else:
                valasz_szoveg += k
                read_mode = 6
        elif k == "[":
            if read_mode == 4:
                read_mode = 5
            elif read_mode == 6:
                read_mode = 7

        elif read_mode == 1:
            if k_elozo == "#":
                k = f.read(1)
                if k == " ":
                    continue
                else:
                    kaland_cim += k
                    continue
            # kaland cim - majd kesobb
            if k == "\n":
                continue
            else:
                kaland_cim += k
                continue

        elif read_mode == 2:
            # fejezet cim - majd kesobb
            continue

        elif read_mode == 3:
            # oldalszam
            if k.isdigit():
                oldalszam += k
            elif k == "\n":
                if int(oldalszam) > maxpage:
                    break
                oldal_szoveg = ""
                konyv.kibovit(int(oldalszam)-1)
                read_mode = 4

        elif read_mode == 4:
            # oldal szoveg
            if k == ">":
                konyv.oldalak[int(oldalszam) - 1].szoveg = oldal_szoveg
                oldal_szoveg = ""
                k = f.read(1)  # space
                k = f.read(1)  # *
                k = f.read(1)  # space
                k = f.read(1)  # [ or text
                if k == "[":
                    read_mode = 5
                else:
                    valasz_szoveg += k
                    read_mode = 6

            else:
                oldal_szoveg += k

        elif read_mode == 5:
            # kitetelek
            if k == "[":
                continue
            elif k == "]":
                if len(feltetel) > 0:
                    feltetelek.append(feltetel)
                read_mode += 1
                k = f.read(1)  # space olvasasa
                continue
            elif k == ",":
                feltetelek.append(feltetel)
                feltetel = ""
                continue
            else:
                feltetel += k

        elif read_mode == 6:
            # valasz szoveg
            if k == "[":
                read_mode = 7
                continue
            else:
                valasz_szoveg += k
                continue

        elif read_mode == 7:
            # celoldal, ahova a valasz vezet
            if k == " ":
                continue
            elif k == "]":
                read_mode = 8
                continue
            elif k.isdigit() or k == "-":
                ide_vezet += k

        elif read_mode == 8:
            if ide_vezet == "":
                ide_vezet = "0"
            konyv.oldalak[int(oldalszam)-1].valasz_hozzaadasa(valasz_szoveg, int(ide_vezet), feltetelek)
            valasz_szoveg = ""
            ide_vezet = ""
            feltetelek = []
            read_mode = 1
    f.close()

class Valasz:
    def __init__(self, szoveg="<ures valasz>", celoldal=0):
        self.szoveg = szoveg
        self.celoldal = celoldal
        self.feltetel_ha_van = []
        self.feltetel_ha_nincs = []

    def felteteleket_hozzaad(self, feltetel):
        if isinstance(feltetel, str):
            if feltetel[0] == '-':
                self.feltetel_ha_nincs.append(feltetel[1:])
            else:
                self.feltetel_ha_van.append(feltetel)
        else:
            for fel in feltetel:
                if fel[0] == '-':
                    self.feltetel_ha_nincs.append(fel[1:])
                else:
                    self.feltetel_ha_van.append(fel)

    def teljesul(self, feltetel=None):
        if feltetel in self.feltetel_ha_van:
            return True
        if feltetel in self.feltetel_ha_nincs:
            return False
        else:
            return True

    def felteteleket_vizsgal(self, feltetelek_listaja, mind=True):
        egy_igaz = False
        mind_igaz = True
        for f in feltetelek_listaja:
            if self.teljesul(f):
                egy_igaz = True
            else:
                mind_igaz = False
        if mind:
            return mind_igaz
        else:
            return egy_igaz


class Oldal:
    def __init__(self):
        self.szoveg = "Ez az oldal ures."
        self.valaszok = []

    def valasz_hozzaadasa(self, valasz, ide_vezet, feltetelek):
        self.valaszok.append(Valasz(valasz, ide_vezet))
        self.valaszok[len(self.valaszok)-1].felteteleket_hozzaad(feltetelek)

class Konyv:
    def __init__(self):
        self.oldalak = []

    def kibovit(self, oldalszam):
        while oldalszam >= len(self.oldalak):
            self.oldalak.append(Oldal())

    def oldal_hozzaadd(self, oldalszam, szoveg):
        self.kibovit(oldalszam)
        self.oldalak[oldalszam].szoveg = szoveg

    def feltolt_faljbol(self, faljnev):
        oldalt_olvas = False
        valaszt_olvas = False
        szam = 0
        kf = open(faljnev, 'r')
        for line in kf:
            if line[0] == '-':
                if line[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    adatok = line.split('-')
                    szam = adatok[1]
                    self.kibovit(szam)
                    oldalt_olvas = True
                    valaszt_olvas = False
                elif line[1] == '>':
                    oldalt_olvas = False
                    valaszt_olvas = True
            else:
                if oldalt_olvas:
                    self.oldalak[szam].szoveg = line
                elif valaszt_olvas:
                    adat = line.split('[')
                    szoveg = adat[0]
                    adat = adat[1].split(']')
                    valaszok = adat[0].split('/')
                    cel = int(adat[1][1:])
                    self.oldalak[szam].valasz_hozzaadasa(szoveg, cel, valaszok)
