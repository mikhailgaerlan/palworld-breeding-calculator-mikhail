# Palworld Multi-Pal and Single-Pal Breeding Calculator

## Single-Pal Breeding Calculator

The single-pal breeding calculator will return a subset of all possible shortest paths for a given parent and child.

## Multi-Pal Breeding Calculator

The multi-pal breeding calculator will return a path for a child starting from the given combinations of parents. The calculator is not guaranteed to find the shortest possible path but is guaranteed to find one if possible.

# Installation

Copy the repo and install the required files using `pip install -r requirements.txt`.

# Examples:
## Command Line Example:

Basic syntax: `python calculator.py Parent1 Parent2 ... ParentN Child`

Example 1: `python calculator.py Lamball Warsect`

Output 1:
```
Found 136 path(s) with length 3
Sample path:
Lamball + Tanzee = Jolthog
Jolthog + Blazamut = Univolt
Univolt + Blazamut = Warsect
```

Example 2: `python calculator.py Lamball Penking Digtoise`

Output 2:
```
Found 6 path(s) in 5 gen(s) with score 5
Sample path:
[Lamball + Penking = Verdash]
[Penking + Verdash = Tombat]
[Tombat + Penking = Bushi]
[Lamball + Bushi = Direhowl]
[Bushi + Direhowl = Digtoise]
```

## Python Example

Example 1:
```python
from calculator import PalworldParentPathFinder

path_finder = PalworldParentPathFinder('Lamball')
paths = path_finder.find_path('Warsect')
```

Output 1:
```
Found 136 path(s) with length 3
Sample path:
Lamball + Tanzee = Jolthog
Jolthog + Blazamut = Univolt
Univolt + Blazamut = Warsect
```
Example 1:
```python
from calculator import PalworldParentPathFinder

path_finder = PalworldParentPathFinder('Lamball', 'Penking')
paths = path_finder.find_path('Digtoise')
```

Output 2:
```
Found 6 path(s) in 5 gen(s) with score 5
Sample path:
[Lamball + Penking = Verdash]
[Penking + Verdash = Tombat]
[Tombat + Penking = Bushi]
[Lamball + Bushi = Direhowl]
[Bushi + Direhowl = Digtoise]
```
