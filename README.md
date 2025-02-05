# TP2 - Jeu de la vie
Développé par : Nathan ROI  

## Description
Automate cellulaire 1D, jeu de la vie et simulation de propagation d'une épidémie. Le tout en Python et s'affiche dans ton terminal.  
Ce projet a été réalisé dans le cadre d'un TP en 3ème année de licence informatique.  

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
