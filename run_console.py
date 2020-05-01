import urwid
import konyv
import os
import sys

VVONAL = '─'
BETUK = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


class GlobalisAdat:
    def __init__(self, p_eredeti_ertek):
        self.ertek = p_eredeti_ertek

    def get(self):
        return self.ertek

    def set(self, p_uj_ertek):
        self.ertek = p_uj_ertek


g_program_info = "\
RPG-BOOK szoveges kalandjatek szimulator\n\
Version 2.1\n\
megtalalhato: github.com/kkrisp/rpg-book 2020.apr.\
"
g_kaland_lista = os.listdir("kalandok")
g_futasi_mod = GlobalisAdat(1)
g_valasztott_kaland = GlobalisAdat("Nincs")
g_jelenlegi_oldal = GlobalisAdat(0)
g_ablak_szelesseg = GlobalisAdat(86)
g_ablak_magassag = GlobalisAdat(33)
g_hatizsak = []


lablec = urwid.Pile([
    #urwid.Divider(VVONAL),
    #urwid.Text("─────────────┬─────────────────────┬" + "─"*100, align='left', wrap='clip'),
    urwid.Columns([
        ('pack', urwid.Text("Kilepes: Q")),
        ('pack', urwid.Text("Vissza a menube: esc")),
        ('pack', urwid.Text("Karakterlap: K")),
        ('pack', urwid.Text("Beallitasok: B"))],
        dividechars=4
    ),
    urwid.Divider()
])


def kilepes(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    if key in ('esc'):
        kaland_futtatas.widget = fomenu
    if key in ('b', 'B'):
        kaland_futtatas.widget = beallitasok
    if key in ('k', 'K'):
        kaland_futtatas.widget = karakterlap

def beallitasok_mentese(arg1=100, arg2=25):
    g_ablak_szelesseg.set(arg1)
    g_ablak_magassag.set(arg2)
    kaland_futtatas.widget = fomenu


def lerovidit(szoveg, sorok, sorhossz):
    """Leroviditi a szoveget, hogy beferjen egy adott magassagu es szelessegu
    szovegdobozba. Figyelembe veszi a tordelest (space-k szerint)"""
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


class Gomb(urwid.Button):
    """Ugyanaz, mint a 'Button' widget, csak nincsenek korulotte kacsacsorok
    (< Gomb > helyett Gomb)"""
    button_left = urwid.Text("")
    button_right = urwid.Text("")

    def __init__(self, *args, **kwargs):
        urwid.Button.__init__(self, *args, **kwargs)
        pass


class ValaszthatoSzoveg(urwid.Text):
    """Ugyanaz, mint a Text csak kivalaszthato"""
    ignore_focus = False
    _selectable = True

    def __init__(self, *args, **kwargs):
        urwid.Text.__init__(self, *args, **kwargs)


class Valaszthato(urwid.WidgetWrap):
    """Egy widgetet var, amit valaszthatova tesz,
    es amit kivalasztva vegrehajt egy fuggvenyt."""

    def sizing(self):
        return frozenset(['flow'])

    signals = ['click', 'enter', 'left', 'right']

    def __init__(self, p_widget, on_press=None, user_data=None, on_press2=None):
        self._w = p_widget
        urwid.WidgetWrap.__init__(self, self._w)

        # The old way of listening for a change was to pass the callback
        # in to the constructor.  Just convert it to the new way:
        if on_press:
            urwid.connect_signal(self, 'click', on_press, user_data)

    def keypress(self, size, key):
        if self._command_map[key] != 'activate':
            return key
        self._emit('click')

    def set_text(self, new):
        try:
            self._w.set_text(new)
        except:
            pass


class Beallitas(urwid.Columns):
    signals = ['click', 'enter', 'left', 'right']

    def __init__(self, cimke, valaszlehetosegek, elso=0, irhato=False, nyilak=('< ', ' >')):
        self.valaszok = valaszlehetosegek
        self.irhato = irhato
        self.jelenlegi = elso
        self.nyilak = nyilak

        self.cimke = urwid.Text(" " + cimke)
        self.ertek = ValaszthatoSzoveg(self.nyilak[0] + self.valaszok[self.jelenlegi] + self.nyilak[1])

        urwid.connect_signal(self, 'left', self.levalt)
        urwid.connect_signal(self, 'right', self.felvalt)
        if irhato:
            urwid.connect_signal(self, 'enter', self.atir)

        urwid.Columns.__init__(self, [
            self.cimke,
            self.ertek
        ])

    def levalt(self, gomb=None, userdata=None):
        kovetkezo = self.jelenlegi - 1
        if kovetkezo < 0:
            kovetkezo = len(self.valaszok)-1
        self.jelenlegi = kovetkezo
        self.ertek.set_text(self.nyilak[0] + self.valaszok[self.jelenlegi] + self.nyilak[1])

    def felvalt(self, gomb=None, userdata=None):
        kovetkezo = self.jelenlegi + 1
        if kovetkezo >= len(self.valaszok):
            kovetkezo = 0
        self.jelenlegi = kovetkezo
        self.ertek.set_text(self.nyilak[0] + self.valaszok[self.jelenlegi] + self.nyilak[1])

    def atir(self, uj_ertek):
        pass  # meg nincs kesz

    def keypress(self, size, key):
        if key == 'left':
            self._emit('left')
        elif key == 'right':
            self._emit('right')
        elif self._command_map[key] != 'activate':
            return key
        else:
            self._emit('click')


class ArnyekosAblak(urwid.Overlay):
    """A widgetet egy arnyekos ablakba rakja igy:
    Solidfill( Padding( Widget ) )"""
    def __init__(self, p_tartalom, p_szelesseg=100, p_magassag=30, padding=2):
        tartalom = urwid.Frame(p_tartalom, footer=lablec)
        tartalom = urwid.Padding(tartalom,  left=padding, right=padding, min_width=20)
        hatter = urwid.AttrWrap(urwid.SolidFill(u"\u2591"), 'hatter vilagos')
        arnyek = urwid.AttrWrap(urwid.SolidFill(u" "), 'hatter arnyekos')
        hatter = urwid.Overlay(
            arnyek, hatter, 'center', g_ablak_szelesseg.get(), 'middle', g_ablak_magassag.get(), left=4, top=2)
        urwid.Overlay.__init__(self,
            tartalom, hatter, 'center', g_ablak_szelesseg.get(), 'middle', g_ablak_magassag.get(), min_width=20, min_height=10)
        #hatter = urwid.Overlay(
        #    arnyek, hatter, 'center', p_szelesseg, 'middle', p_magassag, left=4, top=2)
        #urwid.Overlay.__init__(self,
        #    tartalom, hatter, 'center', p_szelesseg, 'middle', p_magassag, min_width=20, min_height=10)


class KalandElonezet(urwid.LineBox):
    def __init__(self, p_konyv, p_faljnev):
        self.faljnev = p_faljnev
        self.konyv = p_konyv
        tartalom = urwid.Pile([
            (2, urwid.Filler(ValaszthatoSzoveg(self.konyv.cim), valign='top')),
            urwid.Divider(VVONAL, 0, 0),
            (4, urwid.Filler(urwid.Text(lerovidit(self.konyv[0].szoveg, 4, 32)), valign='top'))
        ])
        tartalom = Valaszthato(tartalom, self.kivalaszt)
        urwid.LineBox.__init__(self, tartalom)

    def kivalaszt(self, p_button):
        g_valasztott_kaland.set(self.faljnev)
        g_futasi_mod.set(2)
        km = urwid.Frame(urwid.AttrWrap(
            ArnyekosAblak(KalandKonyvMegjelenito(g_valasztott_kaland.get(), 1),
                          g_ablak_szelesseg.get(),
                          g_ablak_magassag.get()),
            'szoveg'))
        kaland_futtatas.widget = km


class ValaszGomb(Valaszthato):
    button_left = urwid.Text("")
    button_right = urwid.Text("")

    def __init__(self, p_oldal, szoveg="Ures valasz", celoldal=-1, p_jutalom=None):
        self.oldal = p_oldal
        self.celoldal = celoldal
        self.jutalom = p_jutalom
        Valaszthato.__init__(self, ValaszthatoSzoveg(szoveg), self.kivalaszt)

    def kivalaszt(self, p_gomb):
        g_jelenlegi_oldal.set(self.celoldal)
        if self.jutalom is None:
            return
        for j in self.jutalom:
            g_hatizsak.append(j)
        # a lapozas a hatizsak feltoltese utan kell jojjon, kulonben olyan, mintha a nem frissult volna
        self.oldal.lapoz(g_jelenlegi_oldal.get())


class KalandKonyvMegjelenito(urwid.Filler):
    def __init__(self, p_konyv_fajlnev=None, elso_oldal=1):
        self.alapkonyv = None

        self.jelen_oldal = elso_oldal-1
        jelenet = [
            urwid.Divider(),
            urwid.Text("Ures oldal"),
            urwid.Divider(VVONAL, 1, 1),
            urwid.Text("Nincsenek valaszok.")
        ]
        urwid.Filler.__init__(self, urwid.Pile(jelenet), 'top')
        if p_konyv_fajlnev is not None: self.konyvet_megnyit(p_konyv_fajlnev)
        if self.alapkonyv is not None: self.oldalt_betolt(self.alapkonyv[self.jelen_oldal])

    def oldalt_betolt(self, p_konyv_oldal):
        szoveg = p_konyv_oldal.szoveget_general(g_hatizsak)
        valaszok = p_konyv_oldal.valaszlistat_general(g_hatizsak)
        jelenet = [
            urwid.Divider(),
            urwid.Text(szoveg),
            urwid.Divider(VVONAL, 1, 1)]
        l_valasz_szama = 0
        valaszl = []
        for l_v in valaszok:
            valaszl.append(
                urwid.AttrMap(  # minden valasz kulon van formazva, hogy latsszon a kijeloles
                    ValaszGomb(self, BETUK[l_valasz_szama]+") "+l_v.szoveg, l_v.celoldal, l_v.jutalom),
                    None, focus_map="kivalasztott"
                )
            )
            valaszl.append(urwid.Divider())
            l_valasz_szama += 1
        l_valaszlehetosegek = urwid.SimpleListWalker(valaszl)
        self.original_widget = urwid.Pile(jelenet + l_valaszlehetosegek)

    def lapoz(self, celoldal):
        self.jelen_oldal = celoldal-1
        if celoldal < 0:
            kaland_futtatas.widget = fomenu
        self.oldalt_betolt(self.alapkonyv[self.jelen_oldal])

    def konyvet_megnyit(self, p_fajlnev):
        try:
            self.alapkonyv = konyv.Konyv()
            konyv.beolvas("kalandok/" + p_fajlnev, self.alapkonyv)
        except:
            self.alapkonyv = konyv.Konyv()


# ------------ Program az osztalyok felhasznalasaval ------------

lista_0_100 = [str(i) for i in range(100)]

kaland_elonezetek = []
for l_kaland_fajlnev in g_kaland_lista:
    l_konyv = konyv.Konyv()
    konyv.beolvas("kalandok/" + l_kaland_fajlnev, l_konyv)
    kaland_elonezetek.append(  # mivel ez a legkisebb egyseg, amit kivalasztunk, itt szerepel az attr.map
        urwid.AttrMap(
            KalandElonezet(l_konyv, l_kaland_fajlnev),
            'szoveg',
            focus_map="kivalasztott"
        )
    )

tartalom = [
    urwid.Divider(VVONAL, 1, 1),
    urwid.Text(g_program_info, align='center'),
    urwid.Divider(VVONAL, 1, 1),
    urwid.Text(("szoveg", u"Valaszthato kalandok")),
    urwid.Divider(),
    urwid.Padding(
        urwid.GridFlow(kaland_elonezetek, 35, 1, 0, 'left'),
        left=2, right=2, min_width=13, align='left'
    )
]
kalandvalasztoracs = urwid.ListBox(urwid.SimpleListWalker(tartalom))


fejlec = urwid.AttrWrap(urwid.Text("a fejlec ures..."), 'fejlec')
fomenu = urwid.Frame(
    urwid.AttrWrap(
        ArnyekosAblak(kalandvalasztoracs, g_ablak_szelesseg.get(), g_ablak_magassag.get(), 4),
        'szoveg'))

km = urwid.AttrWrap(
    ArnyekosAblak(
        KalandKonyvMegjelenito(g_kaland_lista[0]), g_ablak_szelesseg.get(), g_ablak_magassag.get(), 4),
    'szoveg')

beallitasok_neve = urwid.Pile([
    urwid.Text("Oldal magassaga"),
    urwid.Text("Oldal szelesege"),
    urwid.AttrMap(urwid.Button("Beallitasok mentese"), 'szoveg', focus_map="kivalasztott")
])
beallitasok_erteke = urwid.Pile([
    urwid.IntEdit("", g_ablak_szelesseg.get()),
    urwid.IntEdit("", g_ablak_magassag.get())
])
oa = [1, 1, 5, 1, 1]  # oszlopok aranya
ev = " | "
beallitasok_x = urwid.Pile([
    urwid.AttrMap(Beallitas("Oldal szelessege", lista_0_100, elso=g_ablak_szelesseg.get()),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Oldal magassaga", lista_0_100, elso=g_ablak_magassag.get()),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Anizotropikus szures", ("ki", "be")),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Karakter reszletessege", ("alacsony", "kozepes", "magas")),
                  'szoveg', focus_map="kivalasztott"),
    urwid.Divider(VVONAL, 1, 1),
    urwid.AttrMap(Beallitas("Hangok", ("klasszikus", "futurisztikus", "kozepkori")),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Zene hangereje", [str(i+1) for i in range(10)], elso=6),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Kornyezeti hangok hangereje", [str(i+1) for i in range(10)], elso=6),
                  'szoveg', focus_map="kivalasztott"),
    urwid.Divider(VVONAL, 1, 0),
    urwid.Columns([
        ('weight', oa[0], urwid.AttrMap(urwid.Button("Mentes", beallitasok_mentese), 'szoveg', focus_map="kivalasztott")),
        ('weight', oa[1], urwid.AttrMap(urwid.Button("Elvetes", beallitasok_mentese), 'szoveg', focus_map="kivalasztott")),
        ('weight', oa[2], urwid.Divider()),
    ], dividechars=2)
])

beallitasok_listaja = [
    urwid.Divider(),
    urwid.Text("Beallitasok", align='left'),
    urwid.Divider(VVONAL, 1, 1),
    beallitasok_x
]
beallitasok_alap = urwid.ListBox(urwid.SimpleListWalker(beallitasok_listaja))
beallitasok = urwid.Frame(
    urwid.AttrWrap(
        ArnyekosAblak(
            beallitasok_alap,
            g_ablak_szelesseg.get(),
            g_ablak_magassag.get(), 4), 'szoveg'))

karakterlap_alap = urwid.ListBox(urwid.SimpleListWalker([
    urwid.Divider(),
    urwid.Text("Karakterlap", align='left'),
    urwid.Divider(VVONAL, 1, 1),
    urwid.AttrMap(Beallitas("Ero", [str(i+1) for i in range(10)], elso=6),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Ugyesseg", [str(i+1) for i in range(10)], elso=6),
                  'szoveg', focus_map="kivalasztott"),
    urwid.AttrMap(Beallitas("Gyorsasag", [str(i+1) for i in range(10)], elso=6),
                  'szoveg', focus_map="kivalasztott")
]))
karakterlap = urwid.Frame(
    urwid.AttrWrap(
        ArnyekosAblak(
            karakterlap_alap,
            g_ablak_szelesseg.get(),
            g_ablak_magassag.get(), 4),
        'szoveg'))

formazas = [
    ('szoveg', 'black', 'white', ''),
    ('kivalasztott', 'white', 'black', 'bold'),
    ('hatter', 'white', 'black', ''),
    ('hatter vilagos', 'white', 'black', ''),
    ('hatter arnyekos', 'white', 'black', ''),
    ('szoveg_cim', 'black', 'light gray', ''),
    ('kiemeles', 'dark blue', 'light gray', ('standout', 'underline')),
    ('fejlec', 'white', 'dark red', 'bold')
]

kaland_futtatas = urwid.MainLoop(fomenu, formazas, unhandled_input=kilepes)
kaland_futtatas.run()