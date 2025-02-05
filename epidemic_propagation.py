import copy
from time import sleep
import curses
import os
from random import *


class CellState:
    morte = 0
    malade = 1
    immunise = 2
    saine = 3

def liste_diviseurs(nombre):
    """
    Version optimisée qui calcule tous les diviseurs d'un nombre donné.
    Cette version ne teste que jusqu'à la racine carrée du nombre.

    Args:
        nombre (int): Le nombre dont on veut trouver les diviseurs

    Returns:
        list: Une liste contenant tous les diviseurs du nombre
    """
    diviseurs = []
    # On ne va que jusqu'à la racine carrée du nombre
    for i in range(1, int(nombre ** 0.5) + 1):
        if nombre % i == 0:
            diviseurs.append(i)
            # Si i n'est pas la racine carrée, on ajoute aussi nombre/i
            if i != nombre // i:
                diviseurs.append(nombre // i)

    return sorted(diviseurs)

def calc_lignes_colonnes(nb_indiv):
    """
    Calcul le nombre de colonnes et lignes nécessairent pour avoir
    le nombre d'individus souhaités
    :param nb_indiv: string
    :return: tuple of integer
    """
    diviseurs = liste_diviseurs(nb_indiv)
    indice_diviseur = len(diviseurs) // 2

    nb_lignes = diviseurs[indice_diviseur]
    nb_colonnes = nb_indiv // nb_lignes

    if nb_colonnes == 1:
        return calc_lignes_colonnes(nb_indiv + 1)
    else:
        if nb_colonnes < nb_lignes:
            return nb_colonnes, nb_lignes
        else:
            return nb_lignes, nb_colonnes


def init_grille(nb_li, nb_col, immun):
    """Crée une grille"""
    if immun:
        return [[CellState.immunise if random()<=0.3 else CellState.saine for _ in range(nb_col)] for _ in range(nb_li)] # Grille avec 30% immunisés
    else :
        return [[CellState.saine for _ in range(nb_col)] for _ in range(nb_li)] # grille avec 100% de personnes saines


def voisines_malade(x, y, grille):
    """Compte le nombre de cellules malades autour d'un individu"""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)] # indices à vérifier dans le tableau
    nb_voisines = 0
    nb_li = len(grille)
    nb_col = len(grille[0])

    for dx, dy in directions:
        nx, ny = x + dx, y + dy # parcourt autour de l'individu
        if 0 <= nx < nb_col and 0 <= ny < nb_li: # vérification pour éviter les out of range (bords de tableau)
            if grille[ny][nx] == CellState.malade:
                nb_voisines += 1

    return nb_voisines

"""
cellule morte => reste morte
cellule immunisé ==> reste immunisée
cellule malade ==> devient morte avec une proba p1 ou immunisé avec une proba (1-p1)
cellule saine => devient malade si 1 voisine malade avec une proba p2 sinon reste saine
"""

def evolution(grille, p1, p2):
    """Calcul la nouvelle génération"""
    nb_li = len(grille)
    nb_col = len(grille[0])

    nouvelle_grille = copy.deepcopy(grille) # initialisation de la nouvelle grille
    changement = 0

    for y in range(nb_li):
        for x in range(nb_col):
            nb_voisines = voisines_malade(x, y, grille)
            cell = grille[y][x]

            if cell == CellState.saine and nb_voisines > 0:
                if random() <= p2:
                    nouvelle_grille[y][x] = CellState.malade
                    changement += 1

            if cell == CellState.malade:
                if random() <= p1:
                    nouvelle_grille[y][x] = CellState.morte
                    changement += 1
                elif random() <= 1-p1: # proba : 1-p1
                    nouvelle_grille[y][x] = CellState.immunise
                    changement += 1

    return nouvelle_grille

def est_stable(grille):
    """
    Détermine si l'épidémie est dans un état stable,
    c'est-à-dire plus aucune cellules malades (état transitoire)
    :param grille: list of list of CellState
    :return: boolean
    """
    for ligne in grille:
        for indiv in ligne:
            if indiv == CellState.malade:
                return False
    return True


def get_stats(grille):
    """
    Statistiques de l'épidémie
    :param grille: list of list of CellState
    :return: tuple of integer
    """
    nb_saine = 0
    nb_immunise = 0
    nb_malade = 0
    nb_morte = 0

    for y in range(len(grille)):
        for x in range(len(grille[0])):
            if grille[y][x] == CellState.saine:
                nb_saine += 1
            if grille[y][x] == CellState.immunise:
                nb_immunise += 1
            if grille[y][x] == CellState.malade:
                nb_malade += 1
            if grille[y][x] == CellState.morte:
                nb_morte += 1

    return nb_saine, nb_immunise, nb_malade, nb_morte

def affiche_stats(stdscr, nb_col, nb_indiv, nb_sains, nb_immunise, nb_malade, nb_morte):
    """Affichage des statistiques de l'épidémie (pourcentages et nombres d'individus)"""
    percent_saine = round((nb_sains / nb_indiv) * 100, 2)
    percent_immunise = round((nb_immunise / nb_indiv) * 100, 2)
    percent_malade = round((nb_malade / nb_indiv) * 100, 2)
    percent_morte = round((nb_morte / nb_indiv) * 100, 2)

    str_sains = f"{percent_saine} %\td'individus sains ({nb_sains} individus)"
    str_immunise = f"{percent_immunise} %\td'individus immunisés ({nb_immunise} individus)"
    str_malade = f"{percent_malade} %\td'individus malades ({nb_malade} individus)"
    str_morte = f"{percent_morte} %\td'individus morts ({nb_morte} individus)"

    stdscr.addstr(13, nb_col + 5, str_sains)
    stdscr.addstr(14, nb_col + 5, str_immunise)
    stdscr.addstr(15, nb_col + 5, str_malade)
    stdscr.addstr(16, nb_col + 5, str_morte)


def init_colors():
    """Initialise les paires de couleurs pour curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Sain (blanc)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Immunisé (vert)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Malade (jaune)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # Mort (rouge)

def legende(stdscr, nb_col):
    """
    légende de la grille de représentation de l'épidémie
    :param nb_col: integer
    """
    blanc = curses.color_pair(1)  # Blanc
    vert = curses.color_pair(2)  # Vert
    jaune = curses.color_pair(3)  # Jaune
    rouge = curses.color_pair(4)  # Rouge

    stdscr.addstr(0, nb_col + 5, "\u2588", blanc)
    stdscr.addstr(": individu sain\n")

    stdscr.addstr(2, nb_col + 5, "\u2588", vert)
    stdscr.addstr(": individu immunisé\n")

    stdscr.addstr(4, nb_col + 5, "\u2588", jaune)
    stdscr.addstr(": individu malade\n")

    stdscr.addstr(6, nb_col + 5, "\u2588", rouge)
    stdscr.addstr(": individu mort\n")


def affiche_grille(stdscr, grille):
    """affiche_grille la grille en adaptant à la taille de l'écran"""
    init_colors()
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()  # Taille du terminal

    for y in range(min(len(grille), max_y - 1)):  # -1 pour éviter les erreurs
        for x in range(min(len(grille[0]), (max_x // 2))):
            # Couleurs des celulles
            cell = grille[y][x]
            if cell == CellState.saine:
                couleur = curses.color_pair(1)  # Blanc
            elif cell == CellState.immunise:
                couleur = curses.color_pair(2)  # Vert
            elif cell == CellState.malade:
                couleur = curses.color_pair(3)  # Jaune
            elif cell == CellState.morte:
                couleur = curses.color_pair(4)  # Rouge

            stdscr.attron(couleur) # active la couleur
            stdscr.addch(y, x, "\u2588")  # Afficher le carré
            stdscr.attroff(couleur)  # Désactiver la couleur

    stdscr.refresh()


def epidemic_simulation(stdscr, nb_indiv, p1, p2, immun):
    """Boucle principale de la simulation"""
    curses.curs_set(0)  # Masquer le curseur
    stdscr.nodelay(1)   # Ne pas bloquer sur l'entrée utilisateur
    stdscr.timeout(100)  # Rafraîchir tous les 100ms

    nb_li, nb_col = calc_lignes_colonnes(nb_indiv)

    if immun.upper() == 'Y':
        grille = init_grille(nb_li, nb_col, True)
    else:
        grille = init_grille(nb_li, nb_col, False)

    grille[randint(0, nb_li)//2][randint(0, nb_col)//2] = CellState.malade # Placement d'une cellule malade aléatoirement (//2 pour s'assurer d'être dans la liste)

    nb_sains, nb_immun, nb_malade, nb_morte = get_stats(grille) #initialisation des statistiques

    affiche_grille(stdscr, grille)

    stdscr.addstr(10,nb_col + 5, "Touche 'Entrée' pour lancer la simulation")
    stdscr.addstr(11, nb_col + 5, "'q' pour quitter")
    affiche_stats(stdscr, nb_col, nb_indiv, nb_sains, nb_immun, nb_malade, nb_morte)
    legende(stdscr, nb_col)
    stdscr.refresh()

    go = False

    # touche "entrée" pour lancer la simulation
    while not go:
        key = stdscr.getch()
        if key == 10 or key == 459:
                go = True
        if key == ord("q"):
            exit(1)

    while go:

        grille = evolution(grille, p1, p2)  # Mise à jour de la grille
        nb_sains, nb_immun, nb_malade, nb_morte = get_stats(grille) # mise à jour des stats

        affiche_grille(stdscr, grille)

        legende(stdscr, nb_col)
        stdscr.addstr(10, nb_col + 5, "'q' pour quitter")
        affiche_stats(stdscr, nb_col, nb_indiv, nb_sains, nb_immun, nb_malade, nb_morte)

        key = stdscr.getch()
        if key == ord("q"):  # Quitter avec 'q'
            go = False

        if est_stable(grille):
            go = False # Si la grille est stable on stoppe les évolutions et go à False permet de faire tourner une dernière boucle pour que la grille reste affichée

    # Quand la grille est stable on sort du while pour éxecuter un nouveau while afin que la grille reste afficher et que l'on puisse quitter avec 'q'
    while not go:
        key = stdscr.getch()
        if key == ord("q"):  # Quitter avec 'q'
            go = True


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")  # Efface le terminal avant de lancer le jeu

    nb_individus = int(input("Nombre d'individus : "))
    p1 = float(input("\nProbabilité (p1) de mourir quand un individu est malade (nombre entre 0 et 1) :"))
    print(f"Probabilité d'être immunisé : {1-p1}\n")
    p2 = float(input("Probabilité (p2) de devenir malade au contact d'un malade (nombre entre 0 et 1) : "))
    immun = input("\nCommencer la simulation avec 30% d'individus immunisés, y/n ? ")

    curses.wrapper(epidemic_simulation, nb_individus, p1, p2, immun)