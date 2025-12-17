import random
import string

SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

EMPTY = "."
SHIP = "■"
HIT = "X"
MISS = "o"


def create_field():
    return [[EMPTY] * SIZE for _ in range(SIZE)]


def print_field(field):
    print("  " + " ".join(string.ascii_uppercase[:SIZE]))
    for i, row in enumerate(field):
        print(f"{i+1:2} " + " ".join(row))
    print()


def parse_cell(cell):
    col = string.ascii_uppercase.index(cell[0].upper())
    row = int(cell[1:]) - 1
    return row, col


def neighbors(row, col):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr, nc = row + dr, col + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                yield nr, nc


def can_place_cells(field, cells):
    rows = [r for r, c in cells]
    cols = [c for r, c in cells]

    if not (len(set(rows)) == 1 or len(set(cols)) == 1):
        return False

    if len(cells) != max(rows.count(rows[0]), cols.count(cols[0])):
        return False

    for r, c in cells:
        if field[r][c] != EMPTY:
            return False
        for nr, nc in neighbors(r, c):
            if field[nr][nc] == SHIP:
                return False

    return True


def place_ship_manual(field, size):
    while True:
        print_field(field)
        cells_input = input(f"Введи {size} клетки: ").split()
        if len(cells_input) != size:
            print("Неверное количество клеток\n")
            continue

        try:
            cells = [parse_cell(c) for c in cells_input]
        except:
            print("Неверный формат\n")
            continue

        if can_place_cells(field, cells):
            for r, c in cells:
                field[r][c] = SHIP
            return
        else:
            print("Нельзя поставить корабль\n")


def place_ship_auto(field, size):
    while True:
        horizontal = random.choice([True, False])
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        cells = []

        for i in range(size):
            nr = r + (0 if horizontal else i)
            nc = c + (i if horizontal else 0)
            if nr >= SIZE or nc >= SIZE:
                break
            cells.append((nr, nc))

        if len(cells) == size and can_place_cells(field, cells):
            for r, c in cells:
                field[r][c] = SHIP
            return


def has_ships(field):
    return any(SHIP in row for row in field)


def shoot(field, r, c):
    if field[r][c] == SHIP:
        field[r][c] = HIT
        return True
    if field[r][c] == EMPTY:
        field[r][c] = MISS
    return False


def bot_move(field):
    while True:
        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)
        if field[r][c] in (EMPTY, SHIP):
            return r, c


def game():
    player = create_field()
    bot = create_field()
    bot_visible = create_field()

    for size in SHIPS:
        place_ship_manual(player, size)

    for size in SHIPS:
        place_ship_auto(bot, size)

    while True:
        print("ТВОЁ ПОЛЕ")
        print_field(player)
        print("ПОЛЕ БОТА")
        print_field(bot_visible)

        move = input("Твой выстрел: ")
        try:
            r, c = parse_cell(move)
        except:
            print("Неверный ввод\n")
            continue

        hit = shoot(bot, r, c)
        bot_visible[r][c] = HIT if hit else MISS

        if not has_ships(bot):
            print("ТЫ ПОБЕДИЛ")
            break

        br, bc = bot_move(player)
        shoot(player, br, bc)

        if not has_ships(player):
            print("БОТ ПОБЕДИЛ")
            break


game()
