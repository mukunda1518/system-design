from abc import ABC, abstractmethod

# Define Abstract Products

class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass


# Define Concrete Products

class WindowsButton(Button):
    def render(self):
        return "Rendering Windows Button"

class MacOSButton(Button):
    def render(self):
        return "Rendering MacOS Button"

class WindowsCheckbox(Checkbox):
    def render(self):
        return "Rendering Windows Checkbox"

class MacOSCheckbox(Checkbox):
    def render(self):
        return "Rendering MacOS Checkbox"


# Define Abstract Factory

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass


# Define Concrete Factories

class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()

class MacOSFactory(GUIFactory):
    def create_button(self):
        return MacOSButton()

    def create_checkbox(self):
        return MacOSCheckbox()


# Client code

def render_gui(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(button.render())
    print(checkbox.render())

# Example usage
if __name__ == "__main__":
    for os_type in ["windows", "macos"]:
        if os_type == "windows":
            factory = WindowsFactory()
        elif os_type == "macos":
            factory = MacOSFactory()
        else:
            raise ValueError("Unsupported OS type")

        render_gui(factory)
