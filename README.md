# TP2 - Jeu de la vie

Développé par : Nathan ROI

---

## Prérequis

Python > 3.10 avec la bibliothèque curses :

**Sur windows :**

```powershell
pip install windows-curses
```

**Sur linux** cette bibliothèque est normalement incluse avec Python.

Pour vérifier si curses est installé :

```bash
python3 -c "import curses; print('curses est installé')"
```

Si pas d’erreur curses est installé sinon :

- **Debian / Ubuntu / Linux mint :**
    
    ```bash
    sudo apt install libncurses5-dev libncursesw5-dev
    ```
    
- **Arch Linux / Manjaro :**
    
    ```bash
    sudo pacman -S ncurses
    ```
    
- **Fedora :**
    
    ```bash
    sudo dnf install ncurses-devel
    ```
    

## Lancer le programme

### Partie 1 : Automate cellulaire sur une dimension

- **Windows :**
    
    ```powershell
    python .\life_game_1D.py
    ```
    

- **Linux :**
    
    ```bash
    python3 ./life_game_1D.py
    ```
    

### Partie 2 : Jeu de la vie

- **Windows :**
    
    ```powershell
    python .\life_game.py
    ```
    
- **Linux :**
    
    ```bash
    python3 ./life_game.py
    ```
    

### Partie 3 : Simulation de propagation d’une épidémie

- **Windows :**
    
    ```powershell
    python .\epidemic_propagation.py
    ```
    

- **Linux :**
    
    ```bash
    python3 ./epidemic_propagation.py
    ```
    

**Supposons que p1 soit à 0.5, à partir de quelle valeur de p2 l’ensemble des cellules va être contaminée ?**

Quand p2 est égal à 0.90, on a des simulations où  l’ensemble des cellules va être contaminée.

**Supposons maintenant que 30% de la population soit immunisée au début de la propagation, que
vaut p2 ?**

Pour une population qui est déjà immunisée à 30%, j’obitens : p2 = 0.75.