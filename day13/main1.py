import time


def main():
    total = 0
    for grid in get_grids():
        score = process_grid(grid)
        total += score
    print(total)


def get_grids():
    result = []
    for line in get_lines():
        if line == '':
            yield result
            result = []
        else:
            result.append(line)
    yield result


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


def process_grid(grid):
    reflection_point = find_vertical_reflection(grid)    
    if reflection_point is not None:
        return reflection_point + 1
    reflection_point = find_horizontal_reflection(grid)
    if reflection_point is not None:
        return (reflection_point + 1) * 100
    return 0


def print_grid(grid):
    print()
    for row in grid:
        print(row)


def find_vertical_reflection(grid):
    for i in range(len(grid[0])):
        if is_reflection_point(grid, i, i + 1, get_column):
            return i
    return None


def find_horizontal_reflection(grid):
    for i in range(len(grid)):
        if is_reflection_point(grid, i, i + 1, get_row):
            return i
    return None


def is_reflection_point(grid, i, j, grid_accessor):
    a, b = grid_accessor(grid, i), grid_accessor(grid, j)
    if a is None or b is None or a != b:
        return False
    i, j = i - 1, j + 1
    while True:
        a, b = grid_accessor(grid, i), grid_accessor(grid, j)
        if a is None or b is None:
            return True
        if a != b:
            return False
        i, j = i - 1, j + 1


def get_row(grid, row):
    if row < 0:
        return None
    if row < len(grid):
        return grid[row]
    return None


def get_column(grid, col):
    if col < 0:
        return None
    if col < len(grid[0]):
        return ''.join([row[col] for row in grid])
    return None


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
