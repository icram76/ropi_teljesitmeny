import numpy as np

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