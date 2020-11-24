from typing import Tuple, Union, List, Dict

import numpy as np

Coord = Tuple[int, int]

class Board(object):
    shape: Tuple[int, int]  # hw
    obstacle: List[Coord]
    customer: List[Coord]
    salesman: List[Coord]

    def __init__(
            self,
            shape: Tuple[int, int],
            obstacle: Union[List[Coord], float],
            customer: Union[List[Coord], float],
            salesman: Union[List[Coord], float],
    ):
        super(Board, self).__init__()
        # shape
        self.shape = shape
        # obstacle
        if isinstance(obstacle, float):
            self.obstacle = Board.__random_mask(shape, obstacle)
        else:
            self.obstacle = obstacle
        # customer
        if isinstance(customer, float):
            self.customer = Board.__random_mask(shape, customer)
        else:
            self.customer = customer
        # salesman
        if isinstance(salesman, float):
            self.salesman = Board.__random_mask(shape, salesman)
        else:
            self.salesman = salesman

        self.__ensure_valid()

    def control_first(self, shift: str):
        shift_vector = {
            "w": (-1, 0),
            "s": (+1, 0),
            "a": (0, -1),
            "d": (0, +1),
        }
        if shift in shift_vector:
            first = self.salesman[0]
            new_first = (first[0] + shift_vector[shift][0], first[1] + shift_vector[shift][1])
            if not Board.__in_range(self.shape, new_first[0], new_first[1]):
                self.salesman = self.salesman[1:]
            else:
                self.salesman[0] = new_first
            self.__ensure_valid()

    def view(self) -> Tuple[str, List[Coord], List[Coord], List[Coord]]:
        win = len(self.customer) == 0
        lose = len(self.salesman) == 0
        state = ""
        if lose:
            state = "lose"
        if win:
            state = "win"

        return (
            state,
            self.obstacle,
            self.customer,
            self.salesman,
        )

    def __ensure_valid(self):
        obstacle = Board.__mask_to_array(self.shape, self.obstacle)
        customer = Board.__mask_to_array(self.shape, self.customer)
        salesman = Board.__mask_to_array(self.shape, self.salesman)
        customer[salesman] = False  # if a salesman stands on a customer, remove customer
        cs = np.logical_or(customer, salesman)
        invalid = np.logical_and(cs, obstacle)
        customer[invalid] = False # if a salesman or a customer stands on a obstacle, remove it
        salesman[invalid] = False
        self.obstacle = Board.__array_to_mask(obstacle)
        self.customer = Board.__array_to_mask(customer)
        self.salesman = Board.__array_to_mask(salesman)


    @staticmethod
    def __array_to_mask(arr: np.ndarray) -> List[Coord]:
        mask = []
        for h in range(arr.shape[0]):
            for w in range(arr.shape[1]):
                if arr[h, w]:
                    mask.append((h, w))
        return mask

    @staticmethod
    def __mask_to_array(shape: Tuple[int, int], mask: List[Coord]) -> np.ndarray:
        arr = np.zeros(shape=shape, dtype=bool)
        for h, w in mask:
            arr[h, w] = True
        return arr

    @staticmethod
    def __random_mask(shape: Tuple[int, int], prob: float) -> List[Coord]:
        mask_float = np.random.random(size=shape)
        mask = mask_float < prob
        out = []
        height, width = mask.shape
        for h in range(height):
            for w in range(width):
                if mask[h][w]:
                    out.append((h, w))
        return out


    @staticmethod
    def __in_range(shape: Tuple[int, int], h: int, w: int) -> bool:
        return h < shape[0] and h >= 0 and w < shape[1] and w >= 0

    @staticmethod
    def __create_graph(shape: Tuple[int, int], obstacle: List[Coord]) -> Tuple[np.ndarray, List[Coord], Dict[Coord, int]]:
        height, width = shape
        index2coord: List[Coord] = []
        coord2index: Dict[Coord, int] = {}
        for h in range(height):
            for w in range(width):
                if (h, w) not in obstacle:
                    index2coord.append((h, w))
                    coord2index[(h, w)] = len(index2coord) - 1
        num_nodes = len(index2coord)
        adj = np.zeros(shape=(num_nodes, num_nodes), dtype=bool)
        for index1 in range(num_nodes):
            h0, w0 = index2coord[index1]
            neighbours = [
                (h0 + 1, w0),
                (h0 - 1, w0),
                (h0, w0 + 1),
                (h0, w0 - 1),
            ]
            for h1, w1 in neighbours:
                if Board.__in_range(shape, h1, w1):
                    index2 = coord2index[(h1, w1)]
                    if index2 > index1:
                        adj[index1][index2] = True
                        adj[index2][index1] = True
        return adj, index2coord, coord2index
