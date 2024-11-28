from abc import ABC, abstractmethod

class BgColor(ABC):
    @abstractmethod
    def apply_color(self) -> str:
        pass

class Text(ABC):
    @abstractmethod
    def render_text(self) -> str:
        pass


class LightBgColor(BgColor):
    def apply_color(self) -> str:
        return "Applying white background"


class LightText(Text):
    def render_text(self) -> str:
        return "Rendering text in black"


class DarkBgColor(BgColor):
    def apply_color(self) -> str:
        return "Applying black background"


class DarkText(Text):
    def render_text(self) -> str:
        return "Rendering text in white"

class ThemeFactory(ABC):
    @abstractmethod
    def create_bg_color(self) -> BgColor:
        pass

    @abstractmethod
    def create_text(self) -> Text:
        pass


class LightThemeFactory(ThemeFactory):
    def create_bg_color(self) -> BgColor:
        return LightBgColor()

    def create_text(self) -> Text:
        return LightText()


class DarkThemeFactory(ThemeFactory):
    def create_bg_color(self) -> BgColor:
        return DarkBgColor()

    def create_text(self) -> Text:
        return DarkText()


def client(theme_factory: ThemeFactory):
    bg_color = theme_factory.create_bg_color()
    text = theme_factory.create_text()

    print(bg_color.apply_color())
    print(text.render_text())


# Example usage
if __name__ == "__main__":
    for theme in ["light", "dark"]:
        if theme == "light":
            theme_factory = LightThemeFactory()
        elif theme == "dark":
            theme_factory = DarkThemeFactory()
        else:
            raise ValueError("Invalid theme choice")

        client(theme_factory)
