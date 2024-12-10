from abc import ABC, abstractmethod


# Component
class FileSystemComponent(ABC):
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def ls(self, detailed: bool = False, indent: int = 0):
        pass


# Leaf
class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size    # File size in bytes

    def ls(self, detailed: bool = False, indent: int = 0):
        if detailed:
            print(f"{' ' * indent}- File: {self.name} (Size: {self.size}) bytes")
        else:
            print(f"{' ' * indent}- {self.name}")


# Composite
class Directory(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def ls(self, detailed: bool = False, indent: int = 0):
        if detailed:
            print(f"{' ' * indent}+ Directory: {self.name}")
        else:
            print(f"{' ' * indent}{self.name}")

        for child in self.children:
            child.ls(detailed, indent + 2)
        

# Client code
if __name__ == "__main__":
    
    # Create files
    file1 = File("file1.txt", 500)
    file2 = File("file2.txt", 1500)
    file3 = File("file3.txt", 300)


    # Create directories
    dir1 = Directory("dir1")
    dir2 = Directory("dir2")
    root = Directory("root")

    # Build the structure
    dir1.add(file1)
    dir1.add(file2)
    dir2.add(file3)
    root.add(dir1)
    root.add(dir2)
    
    # Simulate `ls` command
    print("Simple ls:")
    root.ls()   # List contents without details

    print("\nDetailed ls:")
    root.ls(detailed=True)
    
    
    