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
fomenu = urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom))
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

urwid.MainLoop(frame, szinek, unhandled_input=kilepes).run()

#print(g_valsztott_kaland)

megnyitott_konyv = konyv.Konyv()
konyv.beolvas("rpg-book/kalandok/Troll_a_hidon.md", megnyitott_konyv)
g_jelenlegi_oldal = [0]

class ValaszGomb:
    def __init__(self, celoldal, szoveg):
        self.celoldal = celoldal
        self.gomb = urwid.AttrMap(
            urwid.Button(
                szoveg,
                self.valasz_kivalasztva),
            None,
            focus_map='invertalt')

    def valasz_kivalasztva(self, p_gomb):
        g_jelenlegi_oldal[0] += 1 #self.celoldal
        if g_jelenlegi_oldal[0] > 3:
            raise urwid.ExitMainLoop()
        testoldal.oldalt_betolt(g_jelenlegi_oldal[0])
        fejlec.set_text("Valasztott celoldal: " + str(self.celoldal))

class KalandKonyvOldal:
    def __init__(self):
        self.szoveg = "Ures oldal"
        self.valaszok = ["Ures valasz"]
        self.celoldalak = []
        self.tartalom = None
        self.oldalt_betolt(g_jelenlegi_oldal[0])

    def oldalt_betolt(self, p_oldalszam):
        p_konyv_oldal = megnyitott_konyv.oldalak[p_oldalszam]
        szoveg = p_konyv_oldal.szoveget_general([])
        valaszok = p_konyv_oldal.valaszlistat_general([])
        tartalom = [
            sorkihagyas,
            urwid.Text(szoveg),
            urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
            sorkihagyas
        ]
        cnt = 0
        self.celoldalak = []
        for val in valaszok:
            valasz_szoveg = betuk[cnt] + ") " + val.szoveg
            kivalaszas_gomb = ValaszGomb(val.celoldal, valasz_szoveg)
            tartalom.append(kivalaszas_gomb.gomb)
            cnt += 1
            self.celoldalak.append(val.celoldal)
        self.tartalom = urwid.Pile(tartalom)

testoldal = KalandKonyvOldal()


fomenu_tartalom = [
    urwid.Padding(testoldal.tartalom, left=4, right=3, min_width=20)
]
fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom))
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

urwid.MainLoop(frame, szinek, unhandled_input=kilepes).run()

print(g_jelenlegi_oldal[0])
