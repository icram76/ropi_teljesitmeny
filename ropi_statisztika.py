from pynput import keyboard
from datetime import datetime

def kereses (kulcs):
    
    global statusz
    global esemeny
    global esemenyek
    if statusz == 'J':
        if kulcs in jatekosok:
            statusz = 'A'
            print(f'Játékos: {jatekosok[kulcs]}')
            esemeny.append(jatekosok[kulcs])
            return kulcs
    
    if statusz == 'A':
        if kulcs in akciok:
            statusz = 'E'
            print(f'Akcio: {akciok[kulcs]}')
            esemeny.append(akciok[kulcs])
            return kulcs
    
    if statusz == 'E':
        if kulcs in eredmenyek:
            statusz = 'J'
            print(f'Eredmény: {eredmenyek[kulcs]}')
            esemeny.append(eredmenyek[kulcs])
            esemenyek.append(esemeny)
            esemeny = []
            return kulcs
    
    return False



def on_press(key):
    
    global key_hit_time 
    global queue  

    try:
        char = key.char  # Megpróbáljuk karakterként kezelni a lenyomott billentyűt
    except AttributeError:
        char = str(key)  # Ha nem karakter, akkor stringként kezeljük

    if len(queue)==0:
        queue.append(char)

    if kereses(char):
        queue.clear()

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
    akciok = {'a': 'Támad',
             's': 'Felad',              
             'n': 'Nyit',
             'f': 'Fogad',
             'd': 'Véd',
             'b': 'Blokk'}
    eredmenyek = {'h':'Hiba',
                's': 'Sikeres',
                'p': 'próba'}
    
    jatekosok = {'ba' : 'Bandi', 
                   'cs' : 'Csiki', 
                   'h': 'Hofi',
                   'da': 'Deák Attila',
                   'ka': 'kovács attila',
                   'bo': 'Bongyi',
                   'v': 'Vera',
                   'kl': 'Kovács Laci',
                   'ká': 'Áron',
                   't': 'Marci',
                   'má': 'Márkus Áron',
                   'mc': 'Molnár Csabi',
                   'mm': 'Molnár Mira',
                   'bb': 'Bubu'}  
    #csapat összeállítás jatekosok kulcsaival
    a_csapat = {'ba', 'cs', 'h','da', 'ka', 'bo'}
    b_csapat = {'v','kl', 'ká', 't', 'má', 'mc'}

    queue = [] #leütött billentyű kódok tárolására
    esemeny = [] #játékos, akció, eredmény hármas tárolás, más szóval labda interakció ki, mit, hogyan
    esemenyek = [] #játék menete, érintések v események sora
    labda_menet = [] # események sora, aminek a végén az egyik csapat pontot kap
    merkozes = [] #labda_menet-ek összessége
    key_hit_time =  datetime.now()
    statusz = 'J'

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    print(esemenyek)
