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
                    self.feltetel_ha_nincs.append(feltetel[1:])
                else:
                    self.feltetel_ha_van.append(feltetel)

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
        self.valaszok.append(Valasz(valasz), ide_vezet)
        self.valaszok[len(self.valaszok)-1].felteteleket_hozzaad(feltetelek)

class Konyv:
    def __init__(self):
        self.oldalak = []

    def kibovit(self, oldalszam):
        while oldalszam >= len(self.oldalak):
            self.oldalak.append(Oldal)

    def oldal_hozzaadd(self, oldalszam, szoveg):

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