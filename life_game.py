from time import sleep
import curses
import os
from random import random

def init_grille(nb_li, nb_col):
    """Crée une grille avec environ 35% de cellules vivantes"""
    return [[1 if random() < 0.35 else 0 for _ in range(nb_col)] for _ in range(nb_li)]


def voisines(x, y, grille):
    """Compte le nombre de cellules vivantes autour de (x, y)"""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    nb_voisines = 0
    nb_li = len(grille)
    nb_col = len(grille[0])

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < nb_col and 0 <= ny < nb_li and grille[ny][nx]:
            nb_voisines += 1

    return nb_voisines

def evolution(grille):
    """Calcule la nouvelle génération"""
    nb_li = len(grille)
    nb_col = len(grille[0])
    nouvelle_grille = [[0 for _ in range(nb_col)] for _ in range(nb_li)]

    for y in range(nb_li):
        for x in range(nb_col):
            nb_voisins = voisines(x, y, grille)
            cell = grille[y][x]
            if cell and nb_voisins == 2 or nb_voisins == 3:  # Survie
                nouvelle_grille[y][x] = 1
            elif not cell and nb_voisins == 3:  # Naissance
                nouvelle_grille[y][x] = 1

    return nouvelle_grille

def affiche(stdscr, grille):
    """Affiche la grille en adaptant à la taille de l'écran"""
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()  # Taille du terminal

    for y in range(min(len(grille), max_y - 1)):  # -1 pour éviter les erreurs
        for x in range(min(len(grille[0]), (max_x // 2))):
            char = "\u25a0" if grille[y][x] else " "
            stdscr.addstr(y, x*2, char)

    stdscr.refresh()

def game_life(stdscr, nb_li, nb_col, choix):
    """Boucle principale du jeu"""
    curses.curs_set(0)  # Masquer le curseur
    stdscr.nodelay(1)   # Ne pas bloquer sur l'entrée utilisateur
    stdscr.timeout(100)  # Rafraîchir tous les 100ms

    if choix.upper() == 'Y':
        grille = create_glider(11, 36) # 9 lignes ce n'est pas assez haut
    else :
        grille = init_grille(nb_li, nb_col)

    i = 0
    while True:
        affiche(stdscr, grille)
        grille = evolution(grille)  # Mise à jour de la grille

        key = stdscr.getch()
        if key == ord("q"):  # Quitter avec 'q'
            break

        if i == 0:
            sleep(0.8)
        else: sleep(0.3)
        i += 1

def create_glider(nb_li, nb_col):
    grille = [[0 for _ in range(nb_col)] for _ in range(nb_li)]
    indices_glider = [[0, 4], [0, 5], [1, 4], [1, 5], [34, 2], [35, 2], [34, 3], [35, 3], [24, 0], [24, 1], [22, 1], [21, 2],
              [20, 2], [21, 3], [20, 3], [21, 4], [20, 4], [22, 5], [24, 5], [24, 6], [12, 8], [13, 8], [11, 7],
              [10, 6], [10, 5], [10, 4], [11, 3], [12, 2], [13, 2], [15, 3], [16, 4], [16, 5], [16, 6], [15, 7],
              [17, 5], [14, 5]]

    for i in range(len(indices_glider)):
        x = indices_glider[i][0]
        y = indices_glider[i][1]
        grille[y][x] = 1

    return grille

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")  # Efface le terminal avant de lancer le jeu
    choix = input("Volez-vous voir un canon à Glider ? y/n ")

    if choix.upper() == "N":
        nb_lignes = int(input("Nombres de lignes : "))
        nb_colonnes = int(input("Nombres de colonnes : "))
    else:
        nb_lignes = 0
        nb_colonnes = 0

    curses.wrapper(game_life, nb_lignes, nb_colonnes, choix)