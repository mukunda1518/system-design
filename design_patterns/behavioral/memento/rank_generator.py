# Memento class to store the state
class RankMemento:
    def __init__(self, performance, health, rank):
        self._performance = performance
        self._health = health
        self._rank = rank

    def get_state(self):
        return {
            'performance': self._performance,
            'health': self._health,
            'rank': self._rank
        }

# Originator class
class Rank:
    def __init__(self):
        self.performance = 0
        self.health = "Healthy"
        self.rank = "Not Ranked"

    def set_performance(self, performance):
        self.performance = performance
        self.rank_generator()

    def set_health(self, health):
        self.health = health
        self.rank_generator()

    def rank_generator(self):
        if self.health == "Healthy":
            if self.performance >= 80:
                self.rank = "Excellent"
            elif self.performance >= 60:
                self.rank = "Good"
            elif self.performance >= 40:
                self.rank = "Average"
            elif self.performance >= 20:
                self.rank = "Poor"
            else:
                self.rank = "Very Poor"
        else:  # Unhealthy
            if self.performance >= 60:
                self.rank = "Good"
            elif self.performance >= 40:
                self.rank = "Average"
            else:
                self.rank = "Poor"

    def save_to_memento(self):
        """Save current state to memento"""
        return RankMemento(self.performance, self.health, self.rank)

    def restore_from_memento(self, memento):
        """Restore state from memento"""
        state = memento.get_state()
        self.performance = state['performance']
        self.health = state['health']
        self.rank = state['rank']

    def get_details(self):
        return f"Performance: {self.performance}, Health: {self.health}, Rank: {self.rank}"

# Caretaker class to manage history
class TrainingSession:
    def __init__(self):
        self.history = []
        self.current_session = 0

    def add_session(self, memento):
        """Add a new session to history"""
        # Remove any future sessions if we're in the middle of history
        while len(self.history) > self.current_session:
            self.history.pop()
        self.history.append(memento)
        self.current_session += 1
        # Debug print to show history state
        print(f"History now contains {len(self.history)} sessions")
        print(f"Current session index: {self.current_session}")
        print("Session details in history:")
        for i, mem in enumerate(self.history):
            state = mem.get_state()
            print(f"Session {i + 1}: Performance={state['performance']}, "
                  f"Health={state['health']}, Rank={state['rank']}")
        print("-" * 50)

    def undo(self):
        """Undo to previous session"""
        if self.current_session > 0:
            self.current_session -= 1
            print(f"Undoing to session {self.current_session}")
            return self.history[self.current_session - 1] if self.current_session > 0 else None
        return None

    def redo(self):
        """Redo to next session if available"""
        if self.current_session < len(self.history):
            self.current_session += 1
            print(f"Redoing to session {self.current_session}")
            return self.history[self.current_session - 1]
        return None

# Example usage with detailed output
def run_example():
    # Create player rank and training session
    player_rank = Rank()
    training_sessions = TrainingSession()

    print("\nCreating Session 1:")
    player_rank.set_performance(85)
    player_rank.set_health("Healthy")
    print("Session 1:", player_rank.get_details())
    training_sessions.add_session(player_rank.save_to_memento())

    print("\nCreating Session 2:")
    player_rank.set_performance(70)
    player_rank.set_health("Unhealthy")
    print("Session 2:", player_rank.get_details())
    training_sessions.add_session(player_rank.save_to_memento())

    print("\nCreating Session 3:")
    player_rank.set_performance(90)
    player_rank.set_health("Healthy")
    print("Session 3:", player_rank.get_details())
    training_sessions.add_session(player_rank.save_to_memento())

    # Undo last session (e.g., due to failed drug test)
    print("\nUndoing last session:")
    memento = training_sessions.undo()
    if memento:
        player_rank.restore_from_memento(memento)
        print("Current state after undo:", player_rank.get_details())

if __name__ == "__main__":
    run_example()