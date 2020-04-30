import random
import targy

szint_tabla = {1: 0, 2: 100, 3:200, 4:500}


class Karakter(dict):
    TULAJDONSAGOK = ["ero", "ugyesseg", "gyorsasag", "intelligencia"]

    def __init__(self,
                 p_nev="Nevtelen Karakter",
                 p_leiras="Egy ismeretlen, jellegtelen kulseju szemely all veled szemben.",
                 p_alapertek=10,
                 **p_tulajdonsagok):
        self.nev = p_nev
        self.leiras = p_leiras
        self.targyak = []
        self.tudas = []  # =kepzettsegek
        dict.__init__(self)
        self.eletero = [100, 100]
        for l_tul in Karakter.TULAJDONSAGOK:
            if l_tul in p_tulajdonsagok.keys(): self[l_tul] = p_tulajdonsagok[l_tul]
            else:                               self[l_tul] = p_alapertek

    def van_e_nala(self, targy_neve):
        for targy in self.targyak:
            if targy == targy_neve:
                return True
        return False

    def eleterot_modosit(self, mennyiseg):
        uj_eletero = self.eletero[1] + mennyiseg
        if uj_eletero < 0:
            self.eletero[1] = 0
        elif uj_eletero > self.eletero[0]:
            self.eletero[1] = self.eletero[0]
        else:
            self.eletero = uj_eletero

    def nevet_general(self, nevek_listaja, vezeteknevek_listaja=None):
        random_szam = random.randint(0, len(nevek_listaja)-1)
        self.nev = nevek_listaja[random_szam]

    def felvesz(self, p_targy):
        self.targyak.append(p_targy)
        for l_tul, l_bonusz in p_targy.items():
            if l_tul in Karakter.TULAJDONSAGOK:
                self[l_tul] += l_bonusz

    def letesz(self, p_targy):
        leadott_targy = None
        for i in range(len(self.targyak)):
            if self.targyak[i].cimke == p_targy.cimke:
                leadott_targy = self.targyak.pop(i)
                break
        if leadott_targy is None: return False
        for l_tul in self.keys():
            if l_tul in leadott_targy.keys():
                self[l_tul] -= leadott_targy[l_tul]
        return True

    def tanul(self, p_uj_tudas, ismetlodes=False):
        if ismetlodes:
            for l_t in self.tudas:
                if l_t.cimke == p_uj_tudas.cimke:
                    return
        self.tudas.append(p_uj_tudas)

    def elfelejt(self, p_tudas):
        elfelejtett_tudas = None
        for i in range(len(self.tudas)):
            if self.tudas[i].cimke == p_tudas.cimke:
                elfelejtett_tudas = self.tudas.pop(i)
                break
        if elfelejtett_tudas is None: return False
        return True


class Ork(Karakter):
    nevek = ["Rushgar", "Mork", "Ugluuk", "Ghrisna", "Mrzimor"]

    def __init__(self):
        super(Ork, self).__init__()
        self.nevet_general(Ork.nevek)
        self.leiras = "Egy ismeretlen, jellegtelen kulseju ork all veled szemben."

    def spec(self):
        print("Rothado belgazaidat kieresztetted, fujh")


class Ember(Karakter):
    nevek = ["Darvados", "Brom", "Tom", "Edua", "Olo", "D'Louhy", "Pero"]

    def __init__(self):
        super(Ember, self).__init__()
        self.nevet_general(Ember.nevek)
        self.leiras = "Egy ismeretlen, jellegtelen kulseju ember all veled szemben."

    def spec(self):
        print("Ember vagyok, mi kell ennel tobb?!")


class Elf(Karakter):
    nevek = ["Nebelvir", "Fiumiel", "Z'Elenach", "Undomiel", "Syr"]

    def __init__(self):
        super(Elf, self).__init__()
        self.nevet_general(Elf.nevek)
        self.leiras = "Egy ismeretlen, jellegtelen kulseju elf all veled szemben."

    def spec(self):
        print("Csodas enekhangodat kieresztetted, a novenyek zoldebbek, a fak magasabbak lettek!")


class Targy:
    def __init__(self):
        self.nev = "ures targy"
        # a bonususzokat es a felteteleket egy dictionary tarolja
        # {tulajdonsag_1 : bonusz_merteke, tulajodonsag_2 : bonusz_merteke}
        self.feltetelek = {}  # ures dict
        self.bonuszok = {}  # ures dict

    def uj_bonusz(self, tulajdonsag, bonusz):
        '''Uj bonuszt ad a targyhoz. '''
        if tulajdonsag in TULAJDONSAGOK:  # annak vizsgalata, hogy letezo tulajdonsag van-e megadva (robosztussag)
            self.bonuszok[tulajdonsag] = bonusz
            return True
        else:
            return False

    def uj_feltetel(self, tulajdonsag, bonusz):
        '''Uj hasznalati feltetelt ad a targyhoz'''
        if tulajdonsag in Karakter.TULAJDONSAGOK:  # annak vizsgalata, hogy letezo tulajdonsag van-e megadva (robosztussag)
            self.feltetelek[tulajdonsag] = bonusz
            return True
        else:
            return False

    def hasznalhato(self, karakter_tulajdonsagok):
        '''Egy karakter tulajdonsaglistajat varja parameterkent, es visszaadja,
        hogy a targy hasznalhato-e az adott kepessegekkel.'''
        hasznalhato = True
        for tul in Karakter.TULAJDONSAGOK:  # vegigmegy a lehetseges tulajdonsagokon
            if tul in self.feltetelek.keys():  # ha ez nincs a feltetelek kozott, megy a kovatkezore...
                #       ... igy, ha a targynak nincs feltetele azonnal hasznalhato
                if karakter_tulajdonsagok[tul] < self.feltetelek[tul]:  # ha kisebb a karakter tul.-a mint a feltetel
                    hasznalhato = False  # a hasznalhatosag hamis lesz
        return hasznalhato

    def bonusz(self, karakter_tulajdonsag):
        '''Egy tulajdonsagot var parameterkent, es visszaadja a tulajdonsaghoz tartozo bonuszt'''
        return self.bonuszok[karakter_tulajdonsag]
