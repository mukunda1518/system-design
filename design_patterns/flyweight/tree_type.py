

# Flyweight Class
class TreeType:
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, canvas, x, y):
        print(f"Drawing a tree of type {self.name}, color {self.color}, and texture {self.texture} at {x}  {y} on {canvas}")


# Flyweight factory
class TreeFactory:
    _tree_types = {}

    @staticmethod
    def get_tree_type(name, color, texture):
        key = (name, color, texture)
        if key not in TreeFactory._tree_types:
            TreeFactory._tree_types[key] = TreeType(name, color, texture)
            print(f"Created new TreeType: {key}")
        else:
            print(f"Reusing existing TreeType: {key}")
        return TreeFactory._tree_types[key]


# Contextual class
class Tree:
    def __init__(self, x, y, tree_type):
        self.x = x
        self.y = y
        self.type = tree_type

    def draw(self, canvas):
        self.type.draw(canvas, self.x, self.y)


# Client class
class Forest:
    def __init__(self):
        self.trees = []

    def plant_tree(self, x, y, name, color, texture):
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)
        self.trees.append(tree)

    def draw(self, canvas):
        for tree in self.trees:
            tree.draw(canvas)


# Example usage
if __name__ == "__main__":
    forest = Forest()
    forest.plant_tree(10, 20, "Oak", "Green", "Rough")
    forest.plant_tree(30, 40, "Pine", "Brown", "Smooth")
    forest.plant_tree(50, 60, "Oak", "Green", "Rough")  # Reuses the existing "Oak" type
    forest.draw("Canvas1")

