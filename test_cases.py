from calculator import PalworldParentPathFinder

def test_1():
    parents = {'Lamball', 'Penking'}
    child = 'Foxcicle'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert paths[0].path_score == 6
    assert len(paths) == 3

def test_2():
    parents = {'Lamball', 'Penking'}
    child = 'Warsect'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert paths[0].path_score == 11
    assert len(paths) == 1

def test_3():
    parents = {'Lamball', 'Penking', 'Cattiva'}
    child = 'Warsect'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert paths[0].path_score == 11
    assert len(paths) == 1

def test_4():
    parents = {'Lamball', 'Penking'}
    child = 'Digtoise'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert paths[0].path_score == 5
    assert len(paths) == 6

def test_5():
    parents = {'Lamball', 'Penking'}
    child = 'Faleris'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert paths[0].path_score == 6
    assert len(paths) == 1

def test_6():
    parents = {'Lamball', 'Penking', 'Lunaris'}
    child = 'Faleris'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert paths[0].path_score == 6
    assert len(paths) == 1

def test_7():
    parents = {'Lamball'}
    child = 'Warsect'
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)
    assert len(paths) > 0
    assert len(paths[0]) == 3