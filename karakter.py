kepessegek_neve = ["ero", "ugyesseg", "gyorsasag", "intelligencia"]

class Karakter:
    def __init__(self):
        self.targyak = []
        self.max_eletero = 100
        self.eletero = 100

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
    class Ember(Karakter):
    class Elf(Karakter):
