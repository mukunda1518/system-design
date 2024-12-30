from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    row: int
    col: int

class Player(ABC):
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def get_move():
        pass

class HumanPlayer(Player):
    def get_move(self, board: 'Board') -> Position:
        while True:
            try:
                row = int(input(f"Player {self.name} ({self.symbol}), Enter row (0-{board.size - 1}): "))
                col = int(input(f"Player {self.name} ({self.symbol}) Enter col (0-{board.size - 1}): "))
                return Position(row, col)
            except Exception as e:
                print("Please enter valid number")

class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]

    def make_move(self, position: Position, symbol: str):
        if self.is_valid_move(position):
            self.grid[position.row][position.col] = symbol
            return True
        return False
    
    def is_valid_move(self, position: Position) -> bool:
        if position.row >= self.size or position.col >= self.size:
            return False
        return self.grid[position.row][position.col] == " "

    def is_full(self) -> bool:
        return all(cell != " " for row in self.grid for cell in row)

    def display(self):
        for row in self.grid:
            print("|".join(row))
            print("-" * (self.size * 2))

    def is_winner(self, last_move: Position, symbol: str):
        # check the row
        if all(self.grid[last_move.row][col] == symbol for col in range(self.size)):
            return True

        # check the column
        if all(self.grid[row][last_move.col] == symbol for row in range(self.size)):
            return True

        # check the left diagonal
        if last_move.row == last_move.col:
            if all(self.grid[row][row] == symbol for row in range(self.size)):
                return True

        # check the right diagonal
        if last_move.row + last_move.col == self.size - 1:
            if all(self.grid[row][self.size - 1 - row] == symbol for row in range(self.size)):
                return True

        return False

class Game:
    def __init__(self, board_size: int, players: list[Player]):
        self.board = Board(board_size)
        self.players = players
        self.current_player_index = 0

    def play(self):
        last_move = None
    
        while True:
            self.board.display()
            current_player = self.players[self.current_player_index]
            
            # Get valid move from player
            while True:
                position = current_player.get_move(self.board)
                if self.board.make_move(position, current_player.symbol):
                    last_move = position
                    break
                print("Invlaid move try again")
            
            if self.board.is_winner(last_move, current_player.symbol):
                self.board.display()
                print(f"Player {current_player.name} ({current_player.symbol}) wins!")
                break
            
            if self.board.is_full():
                self.board.display()
                print("The game is a tie!")
                break
            
            self.current_player_index = self._switch_player()
    
    def _switch_player(self) -> int:
        return (self.current_player_index + 1) % len(self.players)

class GameBuilder:
    
    def __init__(self):
        self.board_size = 3 # default size
        self.players = []

    def set_board_size(self, size: int) -> 'GameBuilder':
        if size < 3:
            raise ValueError("Board size must be at least 3")
        self.board_size = size
        return self

    def add_player(self, player: Player) -> 'GameBuilder':
        if len(self.players) >= self.board_size:
            raise ValueError(f"Maximum {self.board_size} players allowed")
        self.players.append(player)
        return self

    def build(self) -> Game:
        if len(self.players) < 2:
            raise ValueError("At least 2 players are required")
        return Game(self.board_size, self.players)


def main():
    # Example 1: Traditional 3x3 game with 2 players
    game1 = (GameBuilder()
             .set_board_size(3)
             .add_player(HumanPlayer("Player1", "X"))
             .add_player(HumanPlayer("Player2", "O"))
             .build()
             )
    print("Starting 3x3 game with 2 players...")
    game1.play()

    # Example 2: 5x5 game with 3 players
    game_builder = GameBuilder()
    game_builder.set_board_size(5)
    game_builder.add_player(HumanPlayer("Player1", "X"))
    game_builder.add_player(HumanPlayer("Player2", "O"))
    game_builder.add_player(HumanPlayer("Player3", "#"))
    game2 = game_builder.build()
    print("\nStarting 5x5 game with 3 players...")
    game2.play()

    
if __name__ == "__main__":
    main()
        
