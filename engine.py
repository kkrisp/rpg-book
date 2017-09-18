# A program a lapozgatos szerepjatekkonyveket
# szimulalja, melyeknek minden lapjan van egy
# leiras es valasztasi lehetosegek, hova
# lapozzon a jatekos tovabb... 

# A program text fajloket olvas be, es bizonyos
# flagek szerint meghatarozza az oldalakat, azokon a
# szoveget, a valaszlehetosegeket es a targyakat/felteteleket...

import sys

# a konyv egy oldala - kiirasra keszen...
class Page:
    def __init__(self):
        self.text = ""
        self.actions = []
    
    def print_text(self):
        print("\n" + self.text)

    def print_actions(self):
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        print()
        for x in range(0, len(self.actions)):
            print(abc[x] + ") - " + self.actions[x].text)
        print("\n[x - kilepes]\t[p - profil]")

    def add_text(self, text):
        self.text = self.text + text

    def add_action(self, action):
        self.actions.append(action)

# kiirasra kesz valasz...
class Action:
    def __init__(self):
        self.text = "empty action"
        self.destination = "END"
        self.reward = []
    
    def add_destination(self, destination):
        self.destination = destination
    
    def add_reward(self, reward):
        self.reward.append(reward)

    def add_text(self, text):
        self.text = text

def load_profile(filename):
    profile = ["default"]
    try:
        with open(filename) as fh:
            for line in fh:
                buff = line.split(sep=" ")
                for s in buff:
                    profile.append(s.strip())
    except IOError:
        print("Ures profil betoltese...")
    return profile

def matchlist(list1, list2):
    for element in list1:
        if element not in list2:
            return False
    return True

def matchelement(list1, element2):
    for element in list1:
        #print("keresi", element, element2)
        if element in element2:
            #print("talalta")
            return True
    return False

# ez a fuggveny allitja ossze az oldalt
# csak azokat a reszeket rakja bele, amelyek
# a profilnak megfelelnek...
def page_processor(fh):
    page = Page()
    istext = False

    for line in fh:
        if line.startswith("CONTENT"):
            istext = True
            line = line.split(sep=" ",maxsplit=1)[1]
            page.add_text(line.strip() + ' ')

        elif line.startswith("SPEC"):
            if matchelement(profile, line.split(sep=" ")[1]):
                istext = True                
                page.add_text(fh.readline().strip() + ' ')
            else:
                istext = False
        
        elif line.startswith("ACT"):
            istext = False
            get = False
            rm = False
            line_elements = line.split(sep=" ")
            action = Action()
            action.add_destination(line_elements[1].strip())

            #if len(line_elements) <= 2:
            #    line_elements.append("default")
            match = True
            for x in range(2, len(line_elements)):
                if line_elements[x] == "GET":
                    get = True
                elif get:
                    action.add_reward(line_elements[x].strip())
                elif not matchelement(profile, line_elements[x]):
                    match = False
            if match:
                action.add_text(fh.readline().strip())
                page.add_action(action)
        elif line.startswith("ENDPAGE"):
            break
        elif istext and line != "\n":
            page.add_text("\n" + line.strip())
    return page

def choose_action(page):
    options = {'p':-2, 'x':-1, 'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8}
    while 1:
        opt = input()
        try:
            opt_num = options[opt.lower()]
            if opt_num >= len(page.actions):
                raise KeyError("Out of range...")
            else:
                if opt_num == -1:
                    return "end"
                if opt_num == -2:
                    print()
                    print(profile)
                    page.print_actions()
                else:
                    for element in page.actions[opt_num].reward:
                        profile.append(element)
                    return page.actions[opt_num].destination
        except KeyError:
            print("Nincs ilyen opcio!")

def file_processor(filename, pagename):
    try:
        with open(filename) as fh:
            for line in fh:
                if line.startswith("PAGE"):
                    line = line.split(sep=" ",maxsplit=1)
                    if len(line) != 1:
                        if line[1].strip() == pagename:
                            page = page_processor(fh)
                            page.print_text()
                            page.print_actions()
                            return choose_action(page)
        return "end"
    except IOError:
        print("Missing text file: {}".format(filename))

current_file = "test.txt"
current_page = "start"
profile = load_profile("pistike867.txt")
while current_page != "end":
    #print(current_page)
    current_page = file_processor(current_file, current_page)