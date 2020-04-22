
g_fsz_helye = "x"   # ez jelzi a felteteles, beillesztendo szoveg helyet...
                    # nem fontos milyen, karakter, csak EGY helyet foglaljon


def listava_alakit(szoveg, elvalaszto=",", no_space=False):
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


def felteteleket_olvas(p_fajl):           # feltetelek olvasasa a felteteles szoveghez
    r_feltetelek = ""
    l_betu = "0"
    while l_betu != "]":     # feltetelek vege
        l_betu = p_fajl.read(1)
        r_feltetelek += l_betu
        r_feltetelek = listava_alakit(r_feltetelek, no_space=True)
    return r_feltetelek


def felteteles_szoveget_olvas(p_fajl, p_oldal, p_hely_a_szovegben): # felteteles szoveg olvasasa
    l_feltetelek = None
    r_felteteles_szoveg = ""
    l_betu = "0"
    while l_betu and l_betu != ")":
        l_betu = p_fajl.read(1)
        if l_betu == "[":            # feltetelek olvasasa a felteteles szoveghez
            l_feltetelek = felteteleket_olvas(p_fajl)
        # felteteles szoveg beolvasasanak vege, hozzaadas az oldalhoz (a felt. szov. 'Valasz' osztalyu)
        r_felteteles_szoveg = Valasz(r_felteteles_szoveg[:-1], p_hely_a_szovegben)
        r_felteteles_szoveg.felteteleket_hozzaad(l_feltetelek)
    return r_felteteles_szoveg


def oldalt_olvas(p_fajl, p_elsokar, p_konyv):
    # egy oldal beolvasasa
    speckar = ["#", ">", "[", "{"]
    r_oldalszam = ""
    l_betu = p_elsokar
    # az elso sor az oldalszam (es cim, de az nincs beolvasva):
    while l_betu and l_betu != "\n":
        if l_betu.isdigit() or l_betu == "-":
            r_oldalszam += l_betu
        l_betu = p_fajl.read(1)
    # ha nem sikerult beolvasni az oldalszamot, nem olvassuk tovabb az oldalt:
    if r_oldalszam == "":
        return
    # oldalszam a sikeres beolvasas utan - 1, mivel a lista 0-val kezdodik, a konyv lapjai 1-el
    l_osz = int(r_oldalszam)-1
    p_konyv.kibovit(l_osz)
    # a szoveg olvasasa ameddig a valaszok (>) vagy uj oldal (#) nem jon:
    p_konyv[l_osz].szoveg = ""
    l_betu = p_fajl.read(1)
    l_kar_szam = 0
    while l_betu and l_betu != ">" and l_betu != "#":
        if l_betu == "(":                    # felteteles szoveg olvasasa
            l_feltetelek = ""
            l_felteteles_szoveg = ""
            while l_betu != ")":
                l_betu = p_fajl.read(1)
                if l_betu == "[":            # feltetelek olvasasa a felteteles szoveghez
                    l_feltetelek = ""
                    l_betu = p_fajl.read(1)
                    while l_betu != "]":     # feltetelek vege
                        l_feltetelek += l_betu
                        l_betu = p_fajl.read(1)
                    l_feltetelek = listava_alakit(l_feltetelek, no_space=True)
                else:
                    l_felteteles_szoveg += l_betu
            # felteteles szoveg beolvasasanak vege, hozzaadas az oldalhoz (a felt. szov. 'Valasz' osztalyu)
            l_felteteles_szoveg = Valasz(l_felteteles_szoveg[:-1], l_kar_szam)
            l_felteteles_szoveg.felteteleket_hozzaad(l_feltetelek)
            p_konyv[l_osz].felteteles_szoveg.append(l_felteteles_szoveg)
            p_konyv[l_osz].szoveg += g_fsz_helye
        else: # a beolvasott szoveg sima szoveg...
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
            l_valasz_buffer.felteteleket_hozzaad(listava_alakit(l_lista_buffer[:-1], no_space=True))
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
            l_valasz_buffer.jutalom = listava_alakit(l_lista_buffer[:-1], no_space=True)
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
    olvasasi_mod = 0        # olvasasi mod:
                            # 0 - semmi
                            # 1 - konyv cim
                            # 2 - fejezet cim
                            # 3 - oldal tartalma
    konyv.cim = ""          # konyv cimenek uresre allitasa (eredetileg 'Uj kaland')
    l_oldal_olvasas_volt = False
    beolvasott_oldalak_szama = 0

    while k:  # ameddig el nem erjuk a file veget
        k = f.read(1)

        if k == "#":
            # '#' - konyv cim
            # '##' - fejezet cim/szam (meg nincs megoldva)
            # '###' - oldalszam
            olvasasi_mod = 0
            if l_oldal_olvasas_volt:
                l_oldal_olvasas_volt = False
                olvasasi_mod = 1
            while k == "#":
                olvasasi_mod += 1
                k = f.read(1)

        elif olvasasi_mod == 1:  # kaland cimenek beolvasasa
            # kaland cim - majd kesobb
            konyv.cim += k

        elif olvasasi_mod == 2:
            # fejezet cim beolvasasa - meg nincs implementalva
            continue

        elif olvasasi_mod == 3:  # uj oldal beolvasasa
            if beolvasott_oldalak_szama > max_oldalszam:
                break
            oldalt_olvas(f, k, konyv)
            l_oldal_olvasas_volt = True
            beolvasott_oldalak_szama += 1

    konyv.cim = konyv.cim.strip()  # kosza spacek es enterek eltuntetese a cim vegerol
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
        l_eddig = 0
        l_ettol = 0
        for i in range(len(self.felteteles_szoveg)):
            mehet = (len(self.felteteles_szoveg[i].feltetel_ha_van) < 1)
            for felt in p_meglevo_feltetelek:
                if felt in self.felteteles_szoveg[i].feltetel_ha_van:
                    mehet = True
            for felt in p_meglevo_feltetelek:
                if felt in self.felteteles_szoveg[i].feltetel_ha_nincs:
                    mehet = False
            l_eddig = self.felteteles_szoveg[i].celoldal
            r_szoveg += self.szoveg[l_ettol:l_eddig].strip()
            l_ettol = l_eddig+1
            if mehet:
                r_szoveg += " " + self.felteteles_szoveg[i].szoveg.strip() + " "

        r_szoveg += self.szoveg[l_ettol:].strip()

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
    def __init__(self, p_fn = None):
        self.faljnev = p_fn
        self.cim = "Nevtelen kaland"
        list.__init__(self)

    def megnyit(self, p_fn = None):
        if p_fn is not None:
            self.faljnev = p_fn
        if self.faljnev is not None:
            print("Nincs fajlnev megadva")
        else:
            beolvas(self.faljnev, self)

    def kibovit(self, legnagyobb_oldalszam):
        while legnagyobb_oldalszam >= len(self):
            self.append(Oldal())

    def oldal_hozzaadd(self, oldalszam, szoveg):
        self.kibovit(oldalszam)
        self[oldalszam].szoveg = szoveg
