import urwid
import konyv

program_info = "\
RPG-BOOK szoveges kalandjatek szimulator\n\
Version 0.2\n\
megtalalhato: github.com/kkrisp/rpg-book 2020.aprilis\
"
fejlec_tartalom = "Kilepes: Q | Karakterlap: I "
kalandvalasztas_menu = "Kalan"
betuk = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
szamok = {"a":0, "b":1, "c":1, "d":2, "e":3, "f":4}

def kilepes(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

szinek = [
    ('invertalt', 'standout', ''),
    ('szoveg', 'black', 'light gray', 'standout'),
    ('szoveg_cim', 'black, bold', 'light gray', ''),
    ('kiemeles', 'dark blue', 'light gray', ('standout', 'underline')),
    ('elvalaszto', 'black', 'light gray', 'standout'),
    ('szovegdoboz', 'black', 'dark red'),
    ('hatter', 'black', 'dark blue'),
    ('fejlec', 'white', 'dark red', 'bold')
]

test_kaland_lista = [["Troll a hidon", "Amint at akarsz kelni a hidon, egy nagy troll bujik ki a hid alol. Bore zold..."],
                ["Hazibuli", "Kiveszed a zsebedbol a vodkat, es diadalittas vigyorral..."]]

sorkihagyas = urwid.Divider()

g_valsztott_kaland = ["Nincs"]


def arnyekot_hozzaad(w):

    bg = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
    shadow = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')

#  left right
#  top bottom

    bg = urwid.Overlay(shadow, bg,
        'center', 100,
        'middle', 33,
        left=4, top=2)
    w = urwid.Overlay(w, bg,
        'center', 100,
        'middle', 33,
        min_width=50, min_height=20)
    return w

class KalandValszto:
    def __init__(self, p_cim, p_elonezet, p_tag):
        self.tag = p_tag
        kivalaszas_gomb = urwid.AttrMap(urwid.Button("Kivalaszt", self.kivalaszt), None, focus_map='invertalt')
        self.tartalom = urwid.LineBox(urwid.Pile([
            urwid.Text(p_cim),
            sorkihagyas,
            urwid.Text(p_elonezet),
            sorkihagyas,
            kivalaszas_gomb,
        ]))
    def kivalaszt(self, p_button):
        g_valsztott_kaland[0] = self.tag
        raise urwid.ExitMainLoop()

uw_kaland_lista = []
for l_kaland in test_kaland_lista:
    this = KalandValszto(l_kaland[0], l_kaland[1], l_kaland[0])
    uw_kaland_lista.append(this.tartalom)

fomenu_tartalom = [
    sorkihagyas,
    urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
    urwid.Padding(urwid.Text(program_info, align='center'), left=2, right=2, min_width=20),
    urwid.AttrWrap(urwid.Divider("-", 1, 0), 'elvalaszto'),
    sorkihagyas,
    urwid.Padding(urwid.Text(("szoveg", u"Valaszthato kalandok")), left=2, right=2, min_width=20),
    sorkihagyas,
    urwid.Padding(
        urwid.GridFlow(uw_kaland_lista, 30, 3, 1, 'center'),
        left=4, right=3, min_width=13
    )
]

fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = arnyekot_hozzaad(urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom)))
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

urwid.MainLoop(frame, szinek, unhandled_input=kilepes).run()

#print(g_valsztott_kaland)

megnyitott_konyv = konyv.Konyv()
konyv.beolvas("kalandok/Troll_a_hidon.md", megnyitott_konyv)
g_jelenlegi_oldal = [0]
g_hatizsak = ['kard']


class ValaszGomb:
    def __init__(self, szoveg="Ures valasz", celoldal=-1, p_jutalom=[]):
        self.celoldal = celoldal
        self.jutalom = p_jutalom
        self.gomb = urwid.AttrMap(
            urwid.Button(
                szoveg,
                self.kivalaszt),
            None,
            focus_map='invertalt')

    def kivalaszt(self, p_gomb):
        g_jelenlegi_oldal[0] = self.celoldal
        lapoz(g_jelenlegi_oldal[0], testoldal)
        fejlec.set_text("Valasztott celoldal: " + str(g_jelenlegi_oldal[0]))
        jut_szoveg = ""
        for j in self.jutalom:
            g_hatizsak.append(j)
            jut_szoveg += j + " "

    def set_data(self, uj_szoveg):
        self.gomb.set_text(uj_szoveg)

class KalandKonyvOldal:
    def __init__(self, p_szoveg="Ures oldal"):
        self.jelenet = [
            sorkihagyas,
            urwid.Text(p_szoveg),
            urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto')
        ]
        self.valaszlehetosegek = urwid.SimpleListWalker([])
        self.tartalom = urwid.AttrWrap(urwid.Pile(self.jelenet + self.valaszlehetosegek), 'szoveg')
        self.lapoz(0)

    def oldalt_betolt(self, p_konyv_oldal):
        szoveg = p_konyv_oldal.szoveget_general(g_hatizsak)
        valaszok = p_konyv_oldal.valaszlistat_general(g_hatizsak)
        #self.jelenet[1].set_text(szoveg)
        self.jelenet[1] = urwid.Text(szoveg)
        l_valaszlista = []
        cnt = 0
        for l_v in valaszok:
            l_valaszlista.append(ValaszGomb(betuk[cnt]+") "+l_v.szoveg, l_v.celoldal, l_v.jutalom).gomb)
            cnt += 1
        self.valaszlehetosegek = urwid.SimpleListWalker(l_valaszlista)
        self.tartalom.original_widget = urwid.Pile(self.jelenet + self.valaszlehetosegek)

    def lapoz(self, celoldal):
        if celoldal < 0:
            raise urwid.ExitMainLoop()
        self.oldalt_betolt(megnyitott_konyv.oldalak[celoldal])

testoldal = KalandKonyvOldal()
fomenu_tartalom = [
    urwid.Padding(testoldal.tartalom, left=4, right=3, min_width=20)
]

def lapoz(celoldal, kalankonyvoldal):
    if celoldal < 0:
        raise urwid.ExitMainLoop()
    kalankonyvoldal.oldalt_betolt(megnyitott_konyv.oldalak[celoldal-1])
    loop.watch_pipe("test")


fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = arnyekot_hozzaad(urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom)))
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

loop = urwid.MainLoop(frame, szinek, unhandled_input=kilepes)
loop.run()
