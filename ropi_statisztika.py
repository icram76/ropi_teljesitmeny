from pynput import keyboard
from datetime import datetime

def count_occurrences(array, value):
    count = 0
    for row in array:
        for element in row:
            if element == value:
                count += 1
    return count

def melyikcsapat (jatekos):
    
    if jatekos in a_csapat:
        return 'A'

    if jatekos in b_csapat:
        return 'B'


def menet_ertekelo(menet:list):
    hibaszam = count_occurrences(menet, 'Hiba')
    pont = count_occurrences(menet, 'pont')

    if hibaszam + pont == 0:
        print("Nincs pont a menetben")
    
    if hibaszam + pont > 1:
        print("több mint 1 pont van a menetben")
     
    res = "" 

    for esemeny in menet:
        if esemeny[2] == 'Hiba' and esemeny[1] in ['Támad', 'Nyit', 'Felad']: 
            if melyikcsapat(esemeny[0]) == 'A':
                res = "Pont B Csapatnak"
            elif melyikcsapat(esemeny[0]) == 'B':
                res = "Pont A Csapatnak"
        elif esemeny[2] == 'pont':
            if melyikcsapat(esemeny[0]) == 'A':
                res = "Pont A Csapatnak"
            elif melyikcsapat(esemeny[0]) == 'B':
                res = "Pont B Csapatnak"
    menet.append(res)
    print(res)

def kereses (kulcs):
    
    global statusz
    global esemeny
    global esemenyek
    if statusz == 1:
        if kulcs in jatekosok:
            statusz = 2
            print(f'Játékos: {jatekosok[kulcs]}')
            esemeny.append(jatekosok[kulcs])
            return kulcs
    
    if statusz == 2:
        if kulcs in akciok:
            statusz = 3
            print(f'Akcio: {akciok[kulcs]}')
            esemeny.append(akciok[kulcs])
            return kulcs
    
    if statusz == 3:
        if kulcs in eredmenyek:
            statusz = 1
            print(f'Eredmény: {eredmenyek[kulcs]}')
            esemeny.append(eredmenyek[kulcs])
            esemenyek.append(esemeny)
            esemeny = []
            return kulcs
    
    return False

def on_press(key):
    
    global key_hit_time 
    global queue
    global esemenyek
    global statusz

    try:
        char = key.char  # Megpróbáljuk karakterként kezelni a lenyomott billentyűt
    except AttributeError:
        char = str(key)  # Ha nem karakter, akkor stringként kezeljük

    if len(queue)==0:
        queue.append(char)

    if kereses(char):
        queue.clear()
    
    # funkció billenytyűk
    if key == keyboard.Key.enter:
        labda_menet.append(esemenyek)
        menet_ertekelo(esemenyek)
        esemenyek = []
 
    if key == keyboard.Key.f1:
        print(esemenyek)
    
    if key == keyboard.Key.backspace:
        if len(esemeny) > 0:
            esemeny.pop()
            statusz = statusz - 1
            print(esemenyek)

    if key == keyboard.Key.left:
        print('Bill: left')        
    
    if key == keyboard.Key.right:
        print('Bill: right')        
    
    if key == keyboard.Key.space:
        print('Bill: space')  

    '''if char in jatekosok:
        print(f"Játékos: {jatekosok[char]}")
        queue.clear()
    '''

    now = datetime.now()
    delta = now - key_hit_time
    if delta.total_seconds() > 1 and len(queue) > 0:
        queue.clear()
        queue.append(char) #2karkter
    else:
        queue.append(char)
    
    if len(queue) ==2:
        key_to_search = ''.join(queue)
        if kereses(key_to_search):
            queue.clear()
        '''
        if key_to_search in jatekosok:
            print(f"Játékos: {jatekosok[key_to_search]}")
            queue.clear()
        '''
        queue.clear()

    key_hit_time =  datetime.now()
        
    
def on_release(key):
    if key == keyboard.Key.esc:
        print("Kilépés")
        return False

if __name__ == "__main__":
    #fix változók feltöltése
    #akciok, eredmenyek, jatekosok változókban van a billentyű összerendelés
    akciok = {'t': 'Támad',
             's': 'Felad',              
             'n': 'Nyit',
             'f': 'Fogad',
             'v': 'Véd',
             'b': 'Blokk'}
    eredmenyek = {'h':'Hiba',
                's': 'Sikeres',
                'p': 'pont',
                'b': 'bravur',
                'a': 'átüti'
                }
    
    jatekosok = {'ba' : 'Bandi', 
                 'cs' : 'Csiki', 
                 'h': 'Hofi',
                 'da': 'Deák Attila',
                 'ka': 'Kovács Attila',
                 'bo': 'Bongyi',
                 'v': 'Vera',
                 'kl': 'Kovács Laci',
                 'ká': 'Kovács Áron',
                 't': 'Marci',
                 'má': 'Márkus Áron',
                 'mc': 'Molnár Csabi',
                 'mm': 'Molnár Mira',
                 'bb': 'Bubu'}  
    #csapat összeállítás jatekosok kulcsaival
    a_csapat = {'Bandi', 'Csiki', 'Hofi','Deák Attila', 'Kovács Attila', 'Bongyi'}
    b_csapat = {'Vera','Kovács Laci', 'Kovács Áron', 'Marci', 'Márkus Áron', 'Molnár Csabi'}

    queue = [] #leütött billentyű kódok tárolására
    esemeny = [] #játékos, akció, eredmény hármas tárolás, más szóval labda interakció ki, mit, hogyan
    esemenyek = [] #játék menete, érintések v események sora
    labda_menet = [] # események sora, aminek a végén az egyik csapat pontot kap
    merkozes = [] #labda_menet-ek összessége
    key_hit_time =  datetime.now()
    statusz = 1

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    print(labda_menet)
