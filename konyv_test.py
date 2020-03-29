import konyv as k
import curses
book = k.Konyv()
k.beolvas("Troll_a_hidon.md", book)
cnt = 0
oldalakatkiir = True

if oldalakatkiir:
    for i in book.oldalak:
        cnt += 1
        print("\n", cnt, "-", i.szoveg)
        for j in i.valaszok:
            print("   >>>", j.szoveg)
            print("     > kell hozza:", j.feltetel_ha_van)
            print("     > tilos hozza:", j.feltetel_ha_nincs)
            print("     > ide visz:", j.celoldal)

betuk = ["a", "b", "c", "d", "e"]