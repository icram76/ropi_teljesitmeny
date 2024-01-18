import numpy as np
import pickle
import json 

def tomb_to_file(tomb,filename):
    with open(filename, "wb") as fp:   #Pickling
        pickle.dump(tomb, fp)
        print(f"tomb kiírva ide:{filename}")

def file_to_tomb(file):
    with open(file, "rb") as fp:   # Unpickling
        return pickle.load(fp)

def json_to_file(data, filename):
    with open(filename, 'w') as convert_file: 
        convert_file.write(json.dumps(data, indent=2))

def file_to_json (filename):
    try:
        with open(filename) as json_file:
            return json.load(json_file)
    except Exception as e:
        return {}

def tomb_mentese_allomanyba(tomb, allomany_neve):
    try:
        np.savetxt(allomany_neve, tomb, fmt='%s', delimiter=', ')
        print(f"A tömb sikeresen elmentve az {allomany_neve} állományba.")
    except Exception as e:
        print(f"Hiba történt a mentés során: {e}")

def allomanybol_tombot_letrehoz(allomany_neve):
    try:
        beolvasott_tomb = np.genfromtxt(allomany_neve, delimiter=', ', dtype=str)
        print(f"A tömb sikeresen beolvasva az {allomany_neve} állományból.")
        return beolvasott_tomb
    except Exception as e:
        print(f"Hiba történt az olvasás során: {e}")
        return None