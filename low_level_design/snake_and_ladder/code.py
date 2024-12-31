import random

from typing import Optional
from enum import Enum
from abc import ABC, abstractmethod

class GameStatus(Enum):
    GAME_IN_PROGRESS = "IN_PROGRESS"
    GAME_FINISHED = "FINISHED"


class Player(ABC):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.position = 1  # start position

    @abstractmethod
    def roll_dice(num_dice: int):
        pass

    @abstractmethod
    def set_position(new_position: int):
        pass

    @abstractmethod
    def get_position() -> int:
        pass

class HumanPlayer(Player):

    def roll_dice(self, num_dice: int) -> int:
        return sum(random.randint(1, 6) for _ in range(num_dice))

    def set_position(self, new_position: int):
        self.position = new_position

    def get_position(self) -> int:
        return self.position

class ComputerPlayer(Player):

    def roll_dice(self, num_dice: int) -> int:
        return sum(random.randint(1, 6) for _ in range(num_dice))
    
    def set_position(self, new_position: int):
        self.position = new_position

    def get_position(self) -> int:
        return self.position

class Snake:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def is_valid(self, board_size: int) -> bool:
        return 1 <= self.start <= board_size and 1 <= self.end <= board_size and self.end > self.start

    def get_start_position(self) -> int:
        return self.start

    def get_end_position(self) -> int:
        return self.end

class Ladder:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def is_valid(self, board_size: int) -> bool:
        return 1 <= self.start <= board_size and 1 <= self.end <= board_size and self.end > self.start

    def get_start_position(self) -> int:
        return self.start

    def get_end_position(self) -> int:
        return self.end

class Board:
    def __init__(self, rows: int, cols: int, num_dice: int):
        self.rows = rows
        self.cols = cols
        self.dimension = rows * cols
        self.num_dice = num_dice
        self.board = self._initialize_board(rows, cols)
        self.snakes: dict[int, int] = {}
        self.ladders: dict[int, int] = {}
        self.player_positions: dict[str, int] = {}

    def _initialize_board(self, rows: int, cols: int) -> list[list[int]]:
        """Initialize board with natural numbers in snake-like pattern"""
        board = [[ 0 for _ in range(cols)] for _ in range(rows)]
        number = 1
        
        for row in range(self.rows - 1, -1 , -1):
            if (self.rows - 1 - row) % 2 == 0:
                for col in range(self.cols):
                    board[row][col] = number
                    number += 1
            else:
                for col in range(self.cols - 1, -1, -1):
                    board[row][col] = number
                    number += 1
        return board

    def get_position_coordinates(self, position: int) -> tuple[int, int]:
        """ Get coordinates of the position on the board """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == position:
                    return row, col
        return -1, -1

    def make_move(self, player: Player, dice_number: int) -> bool:
        curr_pos = player.get_position()
        new_pos = curr_pos + dice_number
        
        if new_pos > self.dimension:
            return False
        
        if new_pos in self.snakes:
            old_pos = new_pos
            new_pos = self.snakes[new_pos]
            old_row, old_col = self.get_position_coordinates(old_pos)
            new_row, new_col = self.get_position_coordinates(new_pos)
            print(f"Oops! Snake at Position {old_pos} ({old_row} {old_col}) brings down to {new_pos} ({new_row} {new_col})")
        
        if new_pos in self.ladders:
            old_pos = new_pos
            new_pos = self.ladders[new_pos]
            old_row, old_col = self.get_position_coordinates(old_pos)
            new_row, new_col = self.get_position_coordinates(new_pos)
            print(f"Yay! Ladder at position {old_pos} ({old_row} {old_col})takes up to {new_pos} ({new_row} {new_col})")
        
        player.set_position(new_pos)
        self.player_positions[player.id] = new_pos
        return True

    def is_winner(self, player: Player) -> bool:
        if player.get_position() == self.dimension:
            return True
        return False

    def display_board(self) -> None:
        print("\nCurrent Board State:")
        print("\n")
        
        # Print board with cell numbers and player positions
        for row in range(self.rows):
            for col in range(self.cols):
                cell_num = self.board[row][col]
                cell_str = f"{cell_num:7}"
                
                # Add player markers if any players are on this cell
                players_here = [pid for pid, pos in self.player_positions.items() if pos == cell_num]
                if players_here:
                    cell_str += f"({','.join(players_here)})"

                # Add snake or ladder markers
                if cell_num in self.snakes:
                    cell_str += " S"
                elif cell_num in self.ladders:
                    cell_str += " L"
                else:
                    cell_str += " "
                
                print(f"{cell_str:5}", end="")
            print()  # New line after each row
        
        print("\nSnakes:", {pos: end for pos, end in self.snakes.items()})
        print("Ladders:", {pos: end for pos, end in self.ladders.items()})


class Game:
    def __init__(self, rows: int, cols: int, num_dice: int):
        self.board = Board(rows, cols, num_dice)
        self.num_moves = 0
        self.players: list[Player] = []
        self.winners: list[Player] = []
        self.runner: Player = None
        self.num_dice = num_dice
        self.game_status = GameStatus.GAME_IN_PROGRESS

    def add_player(self, player: Player) -> None:
        self.players.append(player)
        self.board.player_positions[player.id] = player.position

    def create_ladder(self, start: int, end: int) -> bool:
        ladder = Ladder(start, end)
        if ladder.is_valid(self.board.dimension):
            self.board.ladders[start] = ladder.end
            return True
        else:
            return False

    def create_snake(self, end: int, start: int) -> bool:
        snake = Snake(start, end)
        if snake.is_valid(self.board.dimension):
            self.board.snakes[end] = start
            return True
        else:
            return False

    def play(self) -> None:
        self.board.display_board() # print initial board state
        players = self.players
        no_of_palyer = len(players)
        while no_of_palyer > 1:
            for player in players:
                input(f"\nPress Enter for Player {player.name} to roll the dice") # Wait for user input

                dice_number = player.roll_dice(self.num_dice)
                print(f"Player {player.name} rolled a {dice_number}")

                self.board.make_move(player, dice_number)
                self.board.display_board()

                if self.board.is_winner(player):
                    self.winners.append(player)
                    print(f"-------- {player.name} Wins! ---------")
                    players.remove(player)
                    no_of_palyer -= 1

                self.num_moves += 1

        self.runner = players[0]
        print(f"----------- {self.runner.name} Lose! -----------")
        
        self.game_status = GameStatus.GAME_FINISHED
    
    def print_result(self) -> None:
        for winner in self.winners:
            print(f"\nGame Over! {winner.name} wins!")

        if self.runner:
            print(f"\nGame Over! {self.runner.name} lose!")

        print(f"Total moves: {self.num_moves}")


#### client code

if __name__ == "__main__":

      # Initialize game with 10x10 board and  dice
    game = Game(10, 10, 1)
    player1 = HumanPlayer("id_1", "Alice")
    player2 = ComputerPlayer("id_2", "Bob")
    player3 = HumanPlayer("id_3", "Sam")

    # Add players
    game.add_player(player1)
    game.add_player(player2)
    game.add_player(player3)

    # Add snakes
    game.create_snake(89, 10)
    game.create_snake(70, 50)
    game.create_snake(45, 5)
    
    # Add ladders
    game.create_ladder(11, 40)
    game.create_ladder(25, 65)
    game.create_ladder(30, 90)
    
    game.play()
    game.print_result()


        
        


                
            