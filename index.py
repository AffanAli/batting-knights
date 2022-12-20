##########################################
#
#   Battling Knights
#
##########################################
from arena import Arena
from helpers import Knight, PowerItem


def get_game_moves(file_name):
    starting_prefix: str = "GAME-START"
    ending_prefix: str = "GAME-END"
    instructions: list[str] = []
    do_push: bool = False

    with open(file_name) as f:
        for line in f.readlines():
            if line.strip() == starting_prefix:
                do_push = True
            elif line.strip() == ending_prefix:
                do_push = False
                break
            elif do_push:
                instructions.append(line.strip())

    status: bool = bool(len(instructions)) and not do_push

    if not status:
        raise ValueError('Givens Instructions in file are not valid')

    return instructions


if __name__ == "__main__":
    instruction_file_name = 'moves.txt'
    final_status_file_name = "final_state.json"
    moves = get_game_moves(instruction_file_name)

    max_valid_row = 8
    max_valid_column = 8
    knights: dict = {
        'R': Knight('red', [0, 0]),
        'B': Knight('blue', [max_valid_row-1, 0]),
        'G': Knight('green', [max_valid_row-1, max_valid_column-1]),
        'Y': Knight('yellow', [0, max_valid_column-1])
    }

    power_items: list[PowerItem] = [
        PowerItem(name='Axe', location=[2, 2], attack=2, priority=1),
        PowerItem(name='Dagger', location=[2, 5], attack=1, priority=3),
        PowerItem(name='Magic Staff', location=[5, 2], attack=1, defence=1, priority=2),
        PowerItem(name='Helmet', location=[5, 5], defence=1, priority=4)
    ]

    valid_directions = {
        'N': lambda location: [location[0]-1, location[1]],
        'S': lambda location: [location[0]+1, location[1]],
        'E': lambda location: [location[0], location[1]+1],
        'W': lambda location: [location[0]-1, location[1]-1],
    }

    """"
    Reason for passing knights / power_items/ valid_directions from outside
        In order to make the broad (battle field) independent from
            `Knights` / `Power Items` / `Directions`
    """
    arena = Arena(max_valid_row, max_valid_column, knights, power_items, valid_directions)

    arena.start_game(moves)
    # arena.print_broad()

    arena.save_broad(final_status_file_name)

