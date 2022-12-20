from helpers import KnightStatus, PowerItem
import json


class Arena:
    """ Class for handling battle """
    _max_row: int = 0
    _max_col: int = 0
    _knights: dict = {}
    _items: list[PowerItem] = []
    _direction_fn = {}

    def __init__(self, n_row, n_col, players, p_items, possible_directions):
        self._max_row = n_row
        self._max_col = n_col
        self._knights = players
        self._items = p_items
        self._direction_fn = possible_directions

    def __get_move(self, direction):
        """
        function will return the fn against for the given direction
        """
        return self._direction_fn[direction.upper()]

    def __execute_move(self, knight, direction):
        """
            function will update the position of current knight as per the given direction
        """
        coordinates = self._direction_fn[direction](knight.location)
        knight.update_position(coordinates)

        is_invalid_row = coordinates[0] < 0 or coordinates[0] >= self._max_row
        is_invalid_col = coordinates[1] < 0 or coordinates[1] >= self._max_col
        if is_invalid_row or is_invalid_col:
            knight.set_to_drowned()

    def __update_release_item(self, knight, new_location):
        """
        function will update the status of item which is released by any knight
        """
        item_equipped = knight.item_equipped
        if item_equipped:
            item_equipped_details = list(filter(lambda item: item.name == item_equipped, self._items))
            if len(item_equipped_details):
                knight.item_equipped = None
                item_equipped_details[0].enable_item(new_location)

    def __release_items_on_knight_die(self, death_knight):
        """
        function will update the status of item which is released by any death knight
        """
        self.__update_release_item(death_knight, death_knight.location)

    def __release_items_on_knight_drown(self, drowned_knight):
        """
        function will update the status of item which is released by any drowned knight
        """
        find_valid_pos = lambda x, max_x: min(max(x, 0), max_x)

        location = drowned_knight.location
        # finding coordinate of last valid move before drowning
        location = [find_valid_pos(location[0], self._max_row-1), find_valid_pos(location[1], self._max_col-1)]
        # update the status and location of releases item
        self.__update_release_item(drowned_knight, location)

    def __equip_item(self, knight):
        """
            function will update bonus if knight is on any power items
            If there are multiple Active items on that tile:
                Then Sort Items - Priority Wise [A, M, D, H]
                    Then Pick the first one from sorted list (with highest priority)
            else:
                pick the power item
        """
        power_tile = sorted(
            list(filter(lambda item: item.location == knight.location and item.status, self._items)) or [],
            key=lambda item: item.priority
        )

        # if there is any power item and Knight currently does not have any
        if len(power_tile) and knight.item_equipped is None:
            knight.equip_item(power_tile[0])
            power_tile[0].disable_item()

    def __fight_among_knights(self, current_knight):
        """
        Attacker = current_knight
        Defender = Rival knight

        check for other knight on that location
         if any then start fight among knights
            If Attacker's attack Score + surprise_attack_bonus >= defender defence score:
                Defender Knight will die
            else:
                Attacker knight will die
        """
        rival_knights = list(
            filter(
                lambda knight: knight.location == current_knight.location and knight.name != current_knight.name,
                self._knights.values()
            )
        )

        # no rival knight found
        if len(rival_knights) == 0:
            return None

        rival_knight = rival_knights[0]
        if current_knight.attack + current_knight.surprise_attack_bonus >= rival_knight.defence:
            rival_knight.set_to_death()
            return rival_knight
        else:
            current_knight.set_to_death()
            return current_knight

    def start_game(self, moves_list: list[str]):
        """
            ForEach Move:
                parse Move (throw Exception if not valid)
                fetch relevant knights:
                    update knight position &&
                    update knight status depending upon the current knight location
                If Knight is AlIVE:
                    check for items on that tiles && equip knight if needed
                    check for other knight on that location
                     if any then start fight among knights
                        CHECK Attacker's attack Score + surprise_attack_bonus >= defender defence score:
                            Defender Knight will die
                        else:
                            Attacker knight will die
                Else:
                    release the items equipped by current knight to it's last valid location
        """
        for move in moves_list:
            [knight_initial, direction] = map(lambda x: x.upper(), move.split(":"))
            current_knight = self._knights[knight_initial]
            self.__execute_move(current_knight, direction)
            if current_knight.status == KnightStatus.ALIVE:
                self.__equip_item(current_knight)
                rival_knight = self.__fight_among_knights(current_knight)
                if rival_knight:
                    # Put the Rival Knight's equipped items back
                    self.__release_items_on_knight_die(rival_knight)

            if current_knight.status == KnightStatus.DROWNED:
                self.__release_items_on_knight_drown(current_knight)

    def print_broad(self):
        """
        function will print the current status of arena
        """
        print(">>>> Knights")
        [print("\t", value.name, ": ", value) for key, value in self._knights.items()]
        print(">>>> Power Items")
        [print(value) for value in self._items]

    def save_broad(self, file_name):
        """
        function will write the final status of arena on the file
        """
        players = {value.name: [str(value)] for key, value in self._knights.items()}
        items = {value.name: [str(value)] for value in self._items}
        players.update(items)

        with open(file_name, "w") as write_file:
            json.dump(players, write_file, indent=4)
