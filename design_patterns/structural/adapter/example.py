
# Existing interface: RoundHole and RoundPeg
class RoundHole:
    def __init__(self, radius):
        self.radius = radius

    def fits(self, peg):
        return peg.get_radius() <= self.radius

class RoundPeg:
    def __init__(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius


# Adaptee: SquarePeg
class SquarePeg:
    def __init__(self, width):
        self.width = width

    def get_width(self):
        return self.width


# Adapter: Converts SquarePeg to RoundPeg
class SquarePegAdapter(RoundPeg):
    def __init__(self, square_peg):
        self.square_peg = square_peg

    def get_radius(self):
        # Calculate the radius equivalent for the square peg
        return self.square_peg.get_width() * (2**0.5) / 2


# Client code
def main():
    round_hole = RoundHole(5)
    round_peg = RoundPeg(5)
    
    print("Round peg fits in round hole:", round_hole.fits(round_peg))

    small_square_peg = SquarePeg(5)
    large_square_peg = SquarePeg(10)

    # Using adapters to make square pegs fit into the round hole
    small_square_adapter = SquarePegAdapter(small_square_peg)
    large_square_adapter = SquarePegAdapter(large_square_peg)
    
    print("Small square peg fits in round hole: ", round_hole.fits(small_square_adapter))  # True
    print("Large square peg fits in round hole: ", round_hole.fits(large_square_adapter))  # False

main()