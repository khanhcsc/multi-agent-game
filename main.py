from algorithm.msd import minimal_sum_of_distances
from board.board import Board
from game import game


def auto():
    while True:
        shape = (30, 40)
        board = Board(
            shape=shape,
            obstacle=0.1,
            customer=0.05,
            salesman=0.01,
        )
        g = game.Game(board, (20, 20))
        output = g.loop(minimal_sum_of_distances)
        if output == "r":
            continue
        break



def single():
    while True:
        shape = (15, 20)
        board = Board(
            shape=shape,
            obstacle=0.1,
            customer=0.05,
            salesman=0.01,
        )
        try:
            board.obstacle_list.remove((0, 0))
        except ValueError as e:
            print(e)
        board.salesman_list = [(0, 0)]
        g = game.Game(board, (40, 40))
        output = g.loop()
        if output == "r":
            continue
        break


if __name__ == "__main__":
    single()
    auto()
