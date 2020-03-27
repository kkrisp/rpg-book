
TULAJDONSAGOK = ["ero", "ugyesseg", "gyorsasag", "intelligencia"]


class Karakter:
    def __init__(self):
        self.nev = "Nevtelen Karakter"
        self.leiras = "Egy ismeretlen, jellegtelen kulseju szemely all veled szemben."
        self.targyak = []
        self.tulajdonsagok = {}
        self.max_eletero = 100
        self.eletero = 100
        self.tulajdonsagok_feltoltese(10)

    def van_e_nala(self, targy_neve):
        for targy in self.targyak:
            if targy == targy_neve:
                return True
        return False

    def eleterot_modosit(self, mennyiseg):
        uj_eletero = self.eletero + mennyiseg
        if uj_eletero <= 0:
            self.eletero = 0
        elif uj_eletero > self.max_eletero:
            self.eletero = self.max_eletero
        else:
            self.eletero = uj_eletero
            
    class Ork(Karakter):
        def spec(self):
            print("Rothado belgazaidat kieresztetted, fujh")
            
    class Ember(Karakter):
        def spec(self):
            print("Ember vagyok, mi kell ennel tobb?!"
            
    class Elf(Karakter):
        def spec(self):
            print("Csodas enekhangodat kieresztetted, a novenyek zoldebbek, a fak magasabbak lettek!")
            

    def tulajdonsagok_feltoltese(self, alapertek=10):
        for tul in TULAJDONSAGOK:
            self.tulajdonsagok[tul] = alapertek

class Targy:
    def __init__(self):
        self.nev = "ures targy"
        # a bonususzokat es a felteteleket egy dictionary tarolja
        # {tulajdonsag_1 : bonusz_merteke, tulajodonsag_2 : bonusz_merteke}
        self.feltetelek = {}  # ures dict
        self.bonuszok = {}    # ures dict

    def uj_bonusz(self, tulajdonsag, bonusz):
        '''Uj bonuszt ad a targyhoz. '''
        if tulajdonsag in TULAJDONSAGOK:  # annak vizsgalata, hogy letezo tulajdonsag van-e megadva (robosztussag)
            self.bonuszok[tulajdonsag] = bonusz
            return True
        else:
            return False

    def uj_feltetel(self, tulajdonsag, bonusz):
        '''Uj hasznalati feltetelt ad a targyhoz'''
        if tulajdonsag in TULAJDONSAGOK:  # annak vizsgalata, hogy letezo tulajdonsag van-e megadva (robosztussag)
            self.feltetelek[tulajdonsag] = bonusz
            return True
        else:
            return False

    def hasznalhato(self, karakter_tulajdonsagok):
        '''Egy karakter tulajdonsaglistajat varja parameterkent, es visszaadja,
        hogy a targy hasznalhato-e az adott kepessegekkel.'''
        hasznalhato = True
        for tul in TULAJDONSAGOK:               # vegigmegy a lehetseges tulajdonsagokon
            if tul in self.feltetelek.keys():   # ha ez nincs a feltetelek kozott, megy a kovatkezore...
                                                #       ... igy, ha a targynak nincs feltetele azonnal hasznalhato
                if karakter_tulajdonsagok[tul] < self.feltetelek[tul]:  # ha kisebb a karakter tul.-a mint a feltetel
                    hasznalhato = False         # a hasznalhatosag hamis lesz
        return hasznalhato

    def bonusz(self, karakter_tulajdonsag):
        '''Egy tulajdonsagot var parameterkent, es visszaadja a tulajdonsaghoz tartozo bonuszt'''
        return self.bonuszok[karakter_tulajdonsag]
