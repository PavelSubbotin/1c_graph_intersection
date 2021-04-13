import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import sys

res = []

def get_rectangle(x, y, picture, r):
    left = max(0, y - r)
    right = min(len(picture[0]) - 1, y + r)
    top = max(0, x - r)
    bottom = min(len(picture) - 1, x + r)
    return left, right, top, bottom

def get_neigh(x, y, picture, r):
    left, right, top, bottom = get_rectangle(x, y, picture, r)
    return [[picture[i][j] for i in range(top, bottom + 1)] for j in range(left, right + 1)]

def read_picture(name):
    A = imread(name).astype(np.float)
    heigh, lengh, dim = A.shape
    return [[(A[i][j] == [0., 0., 0.])[0] for i in range(heigh)] for j in range(lengh)], heigh, lengh

def pixels_per_row(x, y, picture, heigh, lengh):
    x_ = x
    row, column = 0, 0
    # print('  ', x, y)
    while (x < heigh and picture[x][y]):
        column += 1
        x += 1
    x -= column + 1
    while (x > -1 and picture[x][y]):
        column += 1
        x -= 1
    x = x_
    while (y < lengh and picture[x][y]):
        row += 1
        y += 1
    y -= row + 1
    while (y > -1 and picture[x][y]):
        row += 1
        y -= 1
    # print(row, column)
    return min(row, column)

def find_line_width(picture, heigh, lengh):
    distances = []
    heigh, lengh = len(picture), len(picture[0])
    for i in range(len(picture)):
        for j in range(len(picture[0])):
            if not picture[i][j]:
                continue
            distances.append(pixels_per_row(i, j, picture, heigh, lengh))  # Для каждого черного пикселя мы смотрим сколько с ним в ряду и в 
    return min(distances)                                     # столбце подряд стоит черных пикселей и берем минимум по всем полученным значениям, 
                                                              # таким образом, мы получаем ширину линии на изображении

def custom_print(picture):
    for i in picture:
        for j in i:
            print(int(j), end=' ')
        print('')

def is_intersection(piece, p):
    black_quan, total = sum([sum(i) for i in piece]), len(piece) * len(piece[0])
    if (p != 0.8):
        res.append(black_quan / total)
    return black_quan / total > p

def clear_intersection(x, y, picture, r):
    left, right, top, bottom = get_rectangle(x, y, picture, r)
    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            picture[i][j] = False

def find_intersection_quantity(picture, heigh, lengh, r): # Здесь мы не отличаем вершины от пересечений, так как по условию количество вершин 
                                                       # мы можем передать в программу
    quantity = 0
    for i in range(heigh):
        for j in range(lengh):
            if picture[i][j] or not is_intersection(get_neigh(i, j, picture, 2 * r), 0.55):
                continue
            clear_intersection(i, j, picture, 2 * r)
            quantity += 1
    return quantity



def main(argv):
    name = argv[1]
    vertices = int(argv[2])
    print(name)
    picture, lengh, heigh = read_picture(name)
    print(find_intersection_quantity(picture, heigh, lengh, find_line_width(picture, heigh, lengh)) - vertices)
    print(len(res))
    res.sort(reverse=True)
    for i in range(12):
        print(res[i])

main(sys.argv)
