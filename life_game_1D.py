from time import sleep
import curses

def evolution():
    for i in range(0, len(grille)):
        cellule = grille[i]
        if i == 0:
            left = 0
        else : left = grille[i-1]

        if i < len(grille)-1:
            right = grille[i+1]
        else : right = 0

        match left, cellule, right:
            case 1,1,1: grille[i] = 0
            case 1,1,0: grille[i] = 1
            case 1,0,1: grille[i] = 1
            case 1,0,0: grille[i] = 0
            case 0,1,1: grille[i] = 1
            case 0,1,0: grille[i] = 1
            case 0,0,1: grille[i] = 1
            case 0,0,0: grille[i] = 0


def afficher_grille(stdscr):
    curses.curs_set(0)  # Masquer le curseur
    stdscr.nodelay(1)   # Ne pas bloquer sur l'entrée utilisateur
    stdscr.timeout(10) # Rafraîchir tous les 10ms

    while True:
        stdscr.clear()
        evolution()
        stdscr.addstr(0,0, ''.join("\u25a0" if cell else " " for cell in grille))
        stdscr.refresh()
        sleep(0.1)

        key = stdscr.getch()
        if key == ord("q"):  # Quitter avec 'q'
            break

def config1(taille_grille):
    """
    1 au milieu de la liste et le reste à 0
    """
    grille = [0] * taille_grille
    grille[taille_grille // 2] = 1
    return grille

def config2(taille_grille):
    """
    101 au début de la liste
    """
    grille = [0] * taille_grille
    grille[0] = 1
    grille[2] = 1

    return grille

def config3(taille_grille):
    """
    1 à la fin de la liste et au début et le reste à 0
    """
    grille = [0] * taille_grille
    grille[0] = 1
    grille[taille_grille-1] = 1

    return grille

if __name__ == "__main__":
    taille_grille = int(input("Taille de la grille 1D : "))
    # grille = config1(taille_grille)
    # grille = config2(taille_grille)
    grille = config3(taille_grille)
    curses.wrapper(afficher_grille)

