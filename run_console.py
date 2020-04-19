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


def lerovidit(szoveg, sorok, sorhossz):
    r_szoveg = ""
    l_sor_buffer = ""
    l_szo_buffer = ""
    l_sorok_szama = 1
    for l_karakter in szoveg:
        if len(l_sor_buffer)+len(l_szo_buffer) >= sorhossz:
            l_sorok_szama += 1
            if l_sorok_szama > sorok:
                l_sor_buffer = (l_sor_buffer + l_szo_buffer)[:sorhossz-3] + "..."
                return r_szoveg + l_sor_buffer
            r_szoveg += l_sor_buffer
            l_sor_buffer = ""

        if l_karakter == " ":
            l_sor_buffer += l_szo_buffer + " "
            l_szo_buffer = ""
        else:
            l_szo_buffer += l_karakter

    return szoveg


class ArnyekosAblak(urwid.Overlay):
    def __init__(self, p_tartalom, p_szelesseg = 100, p_magassag=30):
        hatter = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
        arnyek = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')
        hatter = urwid.Overlay(arnyek, hatter,
            'center', p_szelesseg, 'middle', p_magassag, left=4, top=2)
        urwid.Overlay.__init__(self, p_tartalom, hatter,
            'center', p_szelesseg, 'middle', p_magassag, min_width=50, min_height=20)


class KalandElonezet(urwid.AttrMap):
    def __init__(self, p_cim, p_elonezet, p_tag):
        self.tag = p_tag
        kivalasztas_gomb = urwid.AttrMap(urwid.Button(p_cim, self.kivalaszt), 'szoveg_cim', focus_map='kivalasztott')
        tartalom = urwid.Pile([
            (2, urwid.Filler(kivalasztas_gomb, valign='top')),
            urwid.Divider("-", 0, 0),
            (4, urwid.Filler(urwid.Text(lerovidit(p_elonezet, 4, 32)), valign='top'))
        ])
        urwid.AttrMap.__init__(self, urwid.LineBox(tartalom), None, focus_map='kivalasztott')

    def kivalaszt(self, p_button):
        g_valsztott_kaland[0] = self.tag
        raise urwid.ExitMainLoop()


kaland_elonezetek = []
for l_kaland in kaland_lista:
    this = KalandElonezet(l_kaland[1].cim, l_kaland[1].oldalak[0].szoveg, l_kaland[0])
    kaland_elonezetek.append(this)

fomenu_tartalom = [
    urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
    urwid.Padding(urwid.Text(program_info, align='center'), left=2, right=2, min_width=20),
    urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
    urwid.Padding(urwid.Text(("szoveg", u"Valaszthato kalandok")), left=2, right=2, min_width=20),
    sorkihagyas,
    urwid.Padding(
        urwid.GridFlow(kaland_elonezetek, 35, 1, 0, 'left'),
        left=2, right=2, min_width=13, align='left'
    )
]

fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = ArnyekosAblak(urwid.Padding(urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom)), left=4, right=3, min_width=20), 86, 33)
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

urwid.MainLoop(frame, formazas, unhandled_input=kilepes).run()


if g_valsztott_kaland[0] == "Nincs":
    exit()
megnyitott_konyv = konyv.Konyv()
konyv.beolvas("kalandok/" + g_valsztott_kaland[0], megnyitott_konyv)
g_jelenlegi_oldal = [0]
g_hatizsak = []


class ValaszGomb(urwid.Button):
    def __init__(self, p_oldal, szoveg="Ures valasz", celoldal=-1, p_jutalom=None):
        self.oldal = p_oldal
        self.celoldal = celoldal
        self.jutalom = p_jutalom
        urwid.Button.__init__(self, szoveg, self.kivalaszt)

    def kivalaszt(self, p_gomb):
        g_jelenlegi_oldal[0] = self.celoldal
        if self.jutalom is None:
            return
        for j in self.jutalom:
            g_hatizsak.append(j)
        # a lapozas a hatizsak feltoltese utan kell jojjon, kulonben olyan, mintha a nem frissult volna
        self.oldal.lapoz(g_jelenlegi_oldal[0])


class KalandKonyvOldal(urwid.AttrWrap):
    def __init__(self, elso_oldal=1):
        jelenet = [
            urwid.Divider(),
            urwid.Text("Ures oldal"),
            urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto'),
            urwid.Text("Nincsenek valaszok.")
        ]
        urwid.AttrMap.__init__(self, urwid.Pile(jelenet), 'szoveg')
        self.lapoz(elso_oldal)

    def oldalt_betolt(self, p_konyv_oldal):
        szoveg = p_konyv_oldal.szoveget_general(g_hatizsak)
        valaszok = p_konyv_oldal.valaszlistat_general(g_hatizsak)
        jelenet = [
            urwid.Divider(),
            urwid.Text(szoveg),
            urwid.AttrWrap(urwid.Divider("-", 1, 1), 'elvalaszto') ]
        l_valasz_szama = 0
        valaszl = []
        for l_v in valaszok:
            valaszl.append(ValaszGomb(self, betuk[l_valasz_szama]+") "+l_v.szoveg, l_v.celoldal, l_v.jutalom))
            l_valasz_szama += 1
        l_valaszlehetosegek = urwid.SimpleListWalker(valaszl)
        self.original_widget = urwid.Pile(jelenet + l_valaszlehetosegek)

    def lapoz(self, celoldal):
        if celoldal < 0:
            raise urwid.ExitMainLoop()
        self.oldalt_betolt(megnyitott_konyv.oldalak[celoldal-1])


fomenu_tartalom = [urwid.Padding(KalandKonyvOldal(), left=4, right=3, min_width=20)]
fejlec = urwid.AttrWrap(urwid.Text(fejlec_tartalom), 'fejlec')
fomenu = ArnyekosAblak(urwid.ListBox(urwid.SimpleListWalker(fomenu_tartalom)), 86, 33)
frame = urwid.Frame(urwid.AttrWrap(fomenu, 'szoveg'), header=fejlec)

kaland_futtatas = urwid.MainLoop(frame, formazas, unhandled_input=kilepes)
kaland_futtatas.run()
