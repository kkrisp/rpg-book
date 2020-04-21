# read mode
#  0 - nincs
#  1 - kaland cim
#  2 - fejezet cim
#  3 - oldalszam/cim
#  4 - oldal szoveg
#  5 - valasz kriterium
#  6 - valasz szoveg
#  7 - valasz celoldal


def listat_olvas(szoveg, elvalaszto=",", no_space=False):
    r_lista = []
    l_listaelem_buffer = ""
    for l_kar in szoveg:
        if no_space and l_kar == " ":  # a spaceket atugorja ha kell
            continue
        elif l_kar == elvalaszto:                    # elvalasztohoz erve
            if len(l_listaelem_buffer) > 0:          # ha a buffer nem ures
                r_lista.append(l_listaelem_buffer)   # hozzaadja a listahoz
            l_listaelem_buffer = ""                  # nullazza a buffert (akkor is ha ures volt)
        else:
            l_listaelem_buffer += l_kar              # karakter hozzaaadsa a bufferhez

    if len(l_listaelem_buffer) > 0:          # ha a buffer nem ures
        r_lista.append(l_listaelem_buffer)   # hozzaadja a listahoz
    return r_lista


def oldalt_olvas(p_fajl, p_elsokar, p_konyv):
    speckar = ["#", ">", "[", "{"]
    r_oldalszam = ""
    l_betu = p_elsokar
    # az elso sor az oldalszam (es cim)
    while l_betu and l_betu != "\n":
        if l_betu.isdigit() or l_betu == "-":
            r_oldalszam += l_betu
        l_betu = p_fajl.read(1)
    if r_oldalszam == "":
        return
    l_osz = int(r_oldalszam)-1
    p_konyv.kibovit(l_osz)
    # a szoveg, ameddig a valaszok (>) vagy uj oldal (#) nem jon
    p_konyv[l_osz].szoveg = ""
    l_betu = p_fajl.read(1)
    l_kar_szam = 0
    while l_betu:
        if l_betu == ">" or l_betu == "#":
            break
        elif l_betu == "(":
            l_feltetelek = ""
            l_felteteles_szoveg = ""
            while l_betu != ")":
                l_betu = p_fajl.read(1)
                if l_betu == "[":          # nyito zarojel: feltetelek a valaszhoz
                    l_feltetelek = ""
                    l_betu = p_fajl.read(1)
                    while l_betu != "]":    # addig olvassuk, ameddig el nem erjuk a csuko zarojelet
                        l_feltetelek += l_betu
                        l_betu = p_fajl.read(1)
                    l_feltetelek = listat_olvas(l_feltetelek, no_space=True)
                else:
                    l_felteteles_szoveg += l_betu
            l_valasz = Valasz(l_felteteles_szoveg[:-1], l_kar_szam)
            l_valasz.felteteleket_hozzaad(l_feltetelek)
            p_konyv[l_osz].felteteles_szoveg.append(l_valasz)
            # ------ paste vege
        else:
            p_konyv[l_osz].szoveg += l_betu
        l_kar_szam += 1
        l_betu = p_fajl.read(1)
    p_konyv[l_osz].szoveg = p_konyv[l_osz].szoveg.strip()
    # valaszok beolvasasa, ha vannak
    while l_betu == ">":
        l_valasz_buffer = Valasz()
        l_betu = p_fajl.read(3)  # ' * '
        l_betu = p_fajl.read(1)
        # feltetelek beolvasasa
        if l_betu == "[":
            l_lista_buffer = ""
            while l_betu != "]":
                l_betu = p_fajl.read(1)
                l_lista_buffer += l_betu
            l_valasz_buffer.felteteleket_hozzaad(listat_olvas(l_lista_buffer[:-1], no_space=True))
            l_betu = p_fajl.read(1)

        while l_betu == " " or l_betu == "]":
            l_betu = p_fajl.read(1)
            pass

        # szoveg beolvasasa
        l_valasz_buffer.szoveg = ""
        while l_betu not in speckar:
            l_valasz_buffer.szoveg += l_betu
            l_betu = p_fajl.read(1)
        # jutalom beolvasasa
        if l_betu == "{":
            l_lista_buffer = ""
            while l_betu != "}":
                l_betu = p_fajl.read(1)
                l_lista_buffer += l_betu
            l_valasz_buffer.jutalom = listat_olvas(l_lista_buffer[:-1], no_space=True)
        while l_betu not in speckar:
            pass
            l_betu = p_fajl.read(1)
        # celoldal beolvasasa
        if l_betu == "[":
            l_szam_buffer = ""
            while l_betu != "]":
                l_betu = p_fajl.read(1)
                if l_betu.isdigit() or l_betu == "-": l_szam_buffer += l_betu
            l_valasz_buffer.celoldal = int(l_szam_buffer)
        p_konyv[l_osz].valaszok.append(l_valasz_buffer)
        while l_betu not in speckar:
            l_betu = p_fajl.read(1)
            pass
    # oldal feltoltve...


def beolvas(faljnev, konyv, max_oldalszam=100):
    f = open(faljnev, 'r')  # 'md' kiterjesztesu fajl, ahonnan a kalandot beolvassuk
    k = "0"                 # a beolvasott karakter (a fajlt karakterenkent olvassuk)
    #max_oldalszam = 100    # a maximalis beolvashato oldalak szama (memoria vedelme)
    read_mode = 0           # olvasasi mod (lasd a kommentet a fuggveny felett)
    oldal_buffer = Oldal()
    valasz_buffer = Valasz()
    konyv.cim = ""          # kaland cime - nullazas
    oldalszam = 0           # buffer: jelenlegi oldalszam
    valasz_szoveg = ""      # buffer: egy valasz szovege
    ide_vezet = 1           # buffer: celoldal, ahova egy valasz vezet
    feltetelek = []         # buffer: feltetelek listaja egy valaszhoz
    jutalmak = []           # buffer: jutalmak listaja egy valaszhoz
    listaszamlalo = 0
    l_oldal_olvasas_volt = False
    beolvasott_oldalak_szama = 0

    while k:  # ameddig el nem erjuk a file veget
        k_elozo = k
        k = f.read(1)

        if k == "#":
            # '#' - konyv cim
            # '##' - fejezet cim/szam (meg nincs megoldva)
            # '###' - oldalszam
            read_mode = 0
            if l_oldal_olvasas_volt:
                l_oldal_olvasas_volt = False
                read_mode = 1
            while k == "#":
                read_mode += 1
                k = f.read(1)

        elif k == ">":  # valasz beolvasasanak kezdete
            konyv[int(oldalszam) - 1] = oldal_buffer
            konyv[int(oldalszam) - 1].valaszok.append(valasz_buffer)
            valasz_buffer = Valasz()
            oldal_buffer = Oldal()
            oldal_buffer.szoveg = ""
            listaszamlalo = 0
            if read_mode == 6:
                konyv[int(oldalszam) - 1].valaszok.append(valasz_buffer)
            read_mode = 6  # valasz beolvasasa
            continue

        elif read_mode == 1:  # kaland cimenek beolvasasa
            # kaland cim - majd kesobb
            konyv.cim += k

        elif read_mode == 2:
            # fejezet cim beolvasasa- majd kesobb
            continue

        elif read_mode == 3:  # uj oldal
            if beolvasott_oldalak_szama > max_oldalszam:
                break
            oldalt_olvas(f, k, konyv)
            l_oldal_olvasas_volt = True
            beolvasott_oldalak_szama += 1

        elif read_mode == 4:  # oldal szovegenek beolvasasa
            if k == "(":
                l_felteteles_szoveg = ""
                while k != ")":
                    k = f.read(1)
                    if k == "[":          # nyito zarojel: feltetelek a valaszhoz
                        l_feltetelek = ""
                        k = f.read(1)
                        while k != "]":    # addig olvassuk, ameddig el nem erjuk a csuko zarojelet
                            l_feltetelek += k
                            k = f.read(1)
                        feltetelek = listat_olvas(l_feltetelek[:-1], no_space=True)
                    else:
                        l_felteteles_szoveg += k
                l_valasz = Valasz(l_felteteles_szoveg[:-1], 0)
                l_valasz.felteteleket_hozzaad(feltetelek)
                oldal_buffer.felteteles_szoveg.append(l_valasz)
            else:
                oldal_buffer.szoveg += k

        elif read_mode == 6:  # valasz beolvasasa
            valasz_buffer = Valasz()
            k = f.read(3)       # minden valasz igy kezdodik: '> * '
            k = f.read(1)
            if k == "[":           # nyito zarojel: feltetelek a valaszhoz
                l_lista = ""
                if listaszamlalo == 0:
                    listaszamlalo += 1
                    while k != "]":
                        k = f.read(1)
                        l_lista += k
                    valasz_buffer.felteteleket_hozzaad(listat_olvas(l_lista[:-1], no_space=True))
                elif listaszamlalo == 1:
                    listaszamlalo += 1
                    while k != "]":
                        k = f.read(1)
                        if k.isdigit(): l_lista += k
                    valasz_buffer.celoldal = int(l_lista)
            if k == "{":
                l_jutalmak = ""
                while k != "}":
                    k = f.read(1)
                    l_jutalmak += k
                jutalmak = listat_olvas(l_jutalmak[:-1], no_space=True)
            else:
                valasz_buffer.szoveg += k

        if read_mode == 10:
            if ide_vezet == "":
                ide_vezet = "-1"
            konyv[int(oldalszam)-1].valasz_hozzaadasa(valasz_szoveg, int(ide_vezet), feltetelek, jutalmak)
            valasz_szoveg = ""
            ide_vezet = 0
            feltetelek = []
            jutalmak = []
            read_mode = 1
    konyv.cim = konyv.cim.strip()
    f.close()


class Valasz:
    def __init__(self, szoveg="<ures valasz>", celoldal=0):
        self.szoveg = szoveg
        self.celoldal = celoldal
        self.feltetel_ha_van = []    # ami kell, hogy ez a valasz valaszthato legyen
        self.feltetel_ha_nincs = []  # ami, ha van, ez a valasz nem valaszthato
        self.jutalom = []  # amit a karakter kap, ha ezt a valaszt valasztja

    def felteteleket_hozzaad(self, feltetel):
        if len(feltetel) < 1:
            return
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
        self.felteteles_szoveg = []
        self.valaszok = []

    def valasz_hozzaadasa(self, valasz, ide_vezet, feltetelek=[], jutalmak=[]):
        self.valaszok.append(Valasz(valasz, ide_vezet))
        self.valaszok[len(self.valaszok)-1].felteteleket_hozzaad(feltetelek)
        self.valaszok[len(self.valaszok)-1].jutalom = jutalmak

    def felteteles_szoveg_hozzaadasa(self, p_szoveg, p_feltetelek, p_pozicio=-1):
        l_szoveg = Valasz(p_szoveg, p_pozicio)
        l_szoveg.felteteleket_hozzaad(p_feltetelek)
        self.felteteles_szoveg.append(l_szoveg)

    def szoveget_general(self, p_meglevo_feltetelek):
        """"A meglevo feltetelek alapjan beilleszti vagy kihagyja a felteteles szovegeket
        es az igy generalt szoveget adja vissza"""
        r_szoveg = ""
        l_kar_szam = 0

        for i in range(len(self.felteteles_szoveg)):
            mehet = False
            if len(self.felteteles_szoveg[i].feltetel_ha_van) < 1:
                mehet = True
            for felt in p_meglevo_feltetelek:
                if felt in self.felteteles_szoveg[i].feltetel_ha_van:
                    mehet = True
            for felt in p_meglevo_feltetelek:
                if felt in self.felteteles_szoveg[i].feltetel_ha_nincs:
                    mehet = False

            if not mehet:
                continue
                
            l_kar_szam = self.felteteles_szoveg[i].celoldal
            r_szoveg = self.szoveg[:l_kar_szam].strip()
            r_szoveg += " " + self.felteteles_szoveg[i].szoveg.strip()

        r_szoveg += " " + self.szoveg[l_kar_szam:]

        return r_szoveg

    def valaszlistat_general(self, p_meglevo_feltetelek):
        r_lista = []
        for i in range(len(self.valaszok)):
            mehet = False
            for felt in p_meglevo_feltetelek:
                if felt in self.valaszok[i].feltetel_ha_van:
                    mehet = True
            if len(self.valaszok[i].feltetel_ha_van) < 1:
                mehet = True
            for felt in p_meglevo_feltetelek:
                if felt in self.valaszok[i].feltetel_ha_nincs:
                    mehet = False
            if mehet:
                r_lista.append(self.valaszok[i])

        return r_lista


class Konyv(list):
    def __init__(self):
        self.cim = "Nevtelen kaland"
        list.__init__(self)

    def kibovit(self, legnagyobb_oldalszam):
        while legnagyobb_oldalszam >= len(self):
            self.append(Oldal())

    def oldal_hozzaadd(self, oldalszam, szoveg):
        self.kibovit(oldalszam)
        self[oldalszam].szoveg = szoveg

    def feltolt_faljbol(self, faljnev):
        l_oldalt_olvas = False
        valaszt_olvas = False
        szam = 0
        kf = open(faljnev, 'r')
        for line in kf:
            if line[0] == '-':
                if line[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    adatok = line.split('-')
                    szam = adatok[1]
                    self.kibovit(szam)
                    l_oldalt_olvas = True
                    valaszt_olvas = False
                elif line[1] == '>':
                    l_oldalt_olvas = False
                    valaszt_olvas = True
            else:
                if l_oldalt_olvas:
                    self[szam].szoveg = line
                elif valaszt_olvas:
                    adat = line.split('[')
                    szoveg = adat[0]
                    adat = adat[1].split(']')
                    valaszok = adat[0].split('/')
                    cel = int(adat[1][1:])
                    self[szam].valasz_hozzaadasa(szoveg, cel, valaszok)
