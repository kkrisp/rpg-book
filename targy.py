import karakter


class Modosito(dict):
    """Targy, fegyver, kepesseg..."""
    def __init__(self, p_cimke, **p_modositok):
        self.cimke = p_cimke
        dict.__init__(self)
        for l_nev, l_ertek in p_modositok.items():
            self[l_nev] = l_ertek

    def feltetelt_vizsgal(self, min_teljesul=0, **feltetelek):
        siker = 0
        for felt_nev, felt_ertek in feltetelek.items():
            if self[felt_nev] >= felt_ertek:
                siker += 1
                if siker >= min_teljesul: return True
            else:
                if min_teljesul <= 0: return False
        return False


class Targy(Modosito):
    def __init__(self, p_cimke, p_nev=None, p_leiras=None,
                 p_allapot=10, **p_modositok):
        self.nev = p_nev
        self.leiras = p_leiras
        self.allapott = [p_allapot, p_allapot]
        Modosito.__init__(self, p_cimke, **p_modositok)

    def javit(self, p_javitas_merteke):
        javitott_ertek = self.allapott[1] + p_javitas_merteke
        if javitott_ertek <= self.allapott[0]: self.allapott[1] = javitott_ertek
        else:                                  self.allapott[1] = self.allapott[0]

    def romlik(self, p_romlas_merteke):
        romlott_ertek = self.allapott[1] - p_romlas_merteke
        if romlott_ertek >= 0: self.allapott[1] = romlott_ertek
        else:                  self.allapott[1] = 0


class Kepesseg(Modosito):
    def __init__(self, p_cimke, p_nev=None, p_leiras=None,
                 p_szint=0, p_tapasztalat=0, **p_modositok):
        self.cimke = p_cimke
        self.nev = p_nev
        self.leiras = p_leiras
        self.szint_tabla = {1: 0, 2: 100, 3:200, 4:500}
        self.szint = [p_szint, self.szint_tabla[p_szint]]
        Modosito.__init__(self, p_cimke, **p_modositok)

    def tapasztalatot_szerez(self, p_tapasztalat):
        self.szint[1] += p_tapasztalat
        self.szintlepes()

    def szintlepes(self):
        l_szint = 1
        while self.szint[0] > self.szint_tabla[l_szint]:
            l_szint += 1
            pass
        self.szint[0] = l_szint