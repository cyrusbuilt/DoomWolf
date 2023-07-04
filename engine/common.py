from engine import constants as con


def align_grid(x: float, y: float) -> tuple[float, float]:
    x_grid = (x // con.GRID_BLOCK) * con.GRID_BLOCK
    y_grid = (y // con.GRID_BLOCK) * con.GRID_BLOCK
    return x_grid, y_grid
