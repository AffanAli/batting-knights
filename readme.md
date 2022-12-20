## Battling Knights

There are four knights who are about to do battle. 
```
RED (R) 
BLUE (B)
GREEN (G) 
YELLOW (Y) 
```
Their world consists of an 8x8 square "Arena" which looks suspiciously like a chess-board. The Arena is surrounded by water on all sides. The 64 tiles on the board are identified with (row, col) co-ordinates with (0,0) being the top left tile and (7,0) being the bottom left tile (row 7 col 0).
If a Knight moves onto a tile with an item they are immediately equipped with that item, gaining the bonus. A Knight may only hold one item. If a knight with an item moves over another item then they ignore it. If a knight moves onto a tile which has two items on it then they pick up the best item in this order: (A, M, D, H). Knights will pick up an item on a tile before fighting any enemies on that tile. Knights that die in battle drop their item (if they have one). Knights that drown throw their item to the bank before sinking down to Davy Jones' Locker - the item is left on the last valid tile that the knight was on.

### Fighting 
Each Knight has a base attack and defence score of 1: Attack (1) Defence (1) If one knight moves onto the tile of another knight then they will attack. The knight already on the tile will defend. The outcome of a fight is determined as follows: • The attacker takes their base attack score and adds any item modifiers. • The attacker adds 0.5 to their attack score (for the element of surprise). • The defender takes their base defence score and adds any item modifiers. • The attackers final attack score is compared to the defenders final defence score. • The higher score wins, the losing knight dies. DEAD knights drop any equipped items immediately. Further moves do not apply to DEAD knights. The final position of a DEAD knight is the tile that they die on. A DEAD or DROWNED knight has attack 0 and defence 0.

### Instructions 
Open a file called moves.txt and, if the contents are a valid set of moves, determine the final state of the board. The output should be a json file called <b>final_state.json</b> with the following information: 
    
    Position of the knights
    Status of the knights (LIVE, DEAD, DROWNED)
    Attack Power of each knight (including weapons but not surprise bonus)
    Defence Power of each knight (inluding weapons)
    Position of the items (and whether they are held by a knight or not) 

In the following format: 

    { 
        "red": [<R position>,<R status>,<R item (null if no item)>,R Attack,<R Defence>], 
        "blue": [<B position>,<B status>,<B item (null if no item)>,B Attack,<B Defence>], 
        "green": [<G position>,<G status>,<G item (null if no item)>,G Attack,<G Defence>], 
        "yellow": [<Y position>,<Y status>,<Y item (null if no item)>,Y Attack,<Y Defence>], 
        "magic_staff": [<M position>,<M equipped>], "helmet": [<H position>,<H equipped>], 
        "dagger": [<D position>,<D equipped>], "axe": [<A position>,<A equipped>]
    }

## Solution

Dependencies

    > Python 3.9

Execute the Code

    $ python index.py

## Details

#### Classes

1. KnightStatus
    
        Enum type class for handing the Knight status

2. Knight
    
        Data Class for managing and handling the knight related operations

3. PowerItem

        Data Class for managing and handling the Power Items related operations

4. Arena
        
        Main Class for managing & handling the arena broad / knights/ items


#### files

1. helper.py
    
        Helper file containing `KnightStatus` / `Knight` Classes

2. arena.py
    
        file containing main class `Arena`

3. index.py

        1. File defining pre-requisites of `Arena` clas and initializing `Arena` broad object
        2. Read instruction from `moves.txt`
        3. Store the final status of broad in `final_state.json` file


