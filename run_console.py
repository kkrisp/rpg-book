import urwid
import konyv
import os

program_info = "\
RPG-BOOK szoveges kalandjatek szimulator\n\
Version 2.1\n\
megtalalhato: github.com/kkrisp/rpg-book 2020.apr.\
"
fejlec_tartalom = "Kilepes: Q | Karakterlap: I "
kalandvalasztas_menu = "Kalan"
betuk = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
szamok = {"a": 0, "b": 1, "c": 1, "d": 2, "e": 3, "f": 4}

def kilepes(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

formazas = [
    ('kivalasztott', 'standout', '', ''),
    ('szoveg', 'black', 'light gray', ''),
    ('szoveg_cim', 'black', 'light gray', ''),
    ('kiemeles', 'dark blue', 'light gray', ('standout', 'underline')),
    ('elvalaszto', 'black', 'light gray', ''),
    ('szovegdoboz', 'black', 'dark red'),
    ('hatter', 'black', 'dark blue'),
    ('fejlec', 'white', 'dark red', 'bold')
]

kaland_faljnev_lista = os.listdir("kalandok")
kaland_lista = []

cnt = 0
for k_fn in kaland_faljnev_lista:
    kaland_lista.append([k_fn, konyv.Konyv()])
    konyv.beolvas("kalandok/" + k_fn, kaland_lista[cnt][1], max_oldalszam=2)
    cnt += 1

sorkihagyas = urwid.Divider()

g_valsztott_kaland = ["Nincs"]

def lerovidit(szoveg, sorhossz, sorok):
    r_szoveg = ""
    karakterszam = sorok * sorhossz
    if len(szoveg) > karakterszam:
        r_szoveg = szoveg[:karakterszam-3] + "..."
    else:
        r_szoveg = szoveg
    return r_szoveg

def arnyekot_hozzaad(w, p_szelesseg = 100, p_magassag=30):
    bg = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
    shadow = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')

#  left right
#  top bottom

    bg = urwid.Overlay(shadow, bg,
        'center', p_szelesseg,
        'middle', p_magassag,
        left=4, top=2)
    w = urwid.Overlay(w, bg,
        'center', p_szelesseg,
        'middle', p_magassag,
        min_width=50, min_height=20)
    return w

class KalandValszto(urwid.AttrMap):
    def __init__(self, p_cim, p_elonezet, p_tag):
        self.tag = p_tag
        kivalasztas_gomb = urwid.AttrMap(urwid.Button(p_cim, self.kivalaszt), 'szoveg_cim', focus_map='kivalasztott')
        tartalom = urwid.Pile([
            (2, urwid.Filler(kivalasztas_gomb, valign='top')),
            urwid.Divider("-", 0, 0),
            (4, urwid.Filler(urwid.Text(lerovidit(p_elonezet, 4, 30)), valign='top'))
        ])
        urwid.AttrMap.__init__(self, urwid.LineBox(tartalom), None, focus_map='kivalasztott')

    def kivalaszt(self, p_button):
        g_valsztott_kaland[0] = self.tag
        raise urwid.ExitMainLoop()

uw_kaland_lista = []
for l_kaland in kaland_lista:
    this = KalandValszto(l_kaland[1].cim, l_kaland[1].oldalak[0].szoveg, l_kaland[0])
    uw_kaland_lista.append(this)

fomenu_tartalom = [
    urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
    urwid.Padding(urwid.Text(program_info, align='center'), left=2, right=2, min_width=20),
    urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
    urwid.Padding(urwid.Text(("szoveg", u"Valaszthato kalandok")), left=2, right=2, min_width=20),
    sorkihagyas,
    urwid.Padding(
        urwid.GridFlow(uw_kaland_lista, 35, 1, 0, 'left'),
        left=2, right=2, min_width=13, align='left'
    )
]

fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = arnyekot_hozzaad(urwid.Padding(urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom)), left=4, right=3, min_width=20), 86, 33)
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

urwid.MainLoop(frame, formazas, unhandled_input=kilepes).run()

#print(g_valsztott_kaland)

if g_valsztott_kaland[0] == "Nincs":
    exit()
megnyitott_konyv = konyv.Konyv()
konyv.beolvas("kalandok/" + g_valsztott_kaland[0], megnyitott_konyv)
g_jelenlegi_oldal = [0]
g_hatizsak = []


class ValaszGomb(urwid.AttrMap):
    def __init__(self, szoveg="Ures valasz", celoldal=-1, p_jutalom=[]):
        self.celoldal = celoldal
        self.jutalom = p_jutalom
        urwid.AttrMap.__init__(self, urwid.Button(szoveg, self.kivalaszt), None, focus_map='kivalasztott')

    def kivalaszt(self, p_gomb):
        fejlec_szoveg = "Valasztott celoldal: " + str(g_jelenlegi_oldal[0])
        g_jelenlegi_oldal[0] = self.celoldal
        for j in self.jutalom:
            g_hatizsak.append(j)
            fejlec_szoveg += j + " "
        fejlec.set_text(fejlec_szoveg)
        # a lapozas a hatizsak feltoltese utan kell jojjon, kulonben olyan, mintha a nem frissult volna
        lapoz(g_jelenlegi_oldal[0], testoldal)

    def set_data(self, uj_szoveg):
        self.gomb.set_text(uj_szoveg)


class KalandKonyvOldal(urwid.AttrWrap):
    def __init__(self, elso_oldal=0):
        self.jelenet = [
            sorkihagyas,
            urwid.Text("Ures oldal"),
            urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto')
        ]
        self.valaszlehetosegek = urwid.SimpleListWalker([])
        urwid.AttrMap.__init__(self, urwid.Pile(self.jelenet + self.valaszlehetosegek), 'szoveg')
        self.lapoz(elso_oldal)

    def oldalt_betolt(self, p_konyv_oldal):
        szoveg = p_konyv_oldal.szoveget_general(g_hatizsak)
        valaszok = p_konyv_oldal.valaszlistat_general(g_hatizsak)
        self.jelenet[1] = urwid.Text(szoveg)
        l_valaszlista = []
        cnt = 0
        for l_v in valaszok:
            l_valaszlista.append(ValaszGomb(betuk[cnt]+") "+l_v.szoveg, l_v.celoldal, l_v.jutalom))
            cnt += 1
        self.valaszlehetosegek = urwid.SimpleListWalker(l_valaszlista)
        self.original_widget = urwid.Pile(self.jelenet + self.valaszlehetosegek)

    def lapoz(self, celoldal):
        if celoldal < 0:
            raise urwid.ExitMainLoop()
        self.oldalt_betolt(megnyitott_konyv.oldalak[celoldal])

testoldal = KalandKonyvOldal()
fomenu_tartalom = [
    urwid.Padding(testoldal, left=4, right=3, min_width=20)
]

def lapoz(celoldal, kalankonyvoldal):
    if celoldal < 0:
        raise urwid.ExitMainLoop()
    kalankonyvoldal.oldalt_betolt(megnyitott_konyv.oldalak[celoldal-1])


fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = arnyekot_hozzaad(urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom)), 86, 33)
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)


loop = urwid.MainLoop(frame, formazas, unhandled_input=kilepes)
loop.run()
