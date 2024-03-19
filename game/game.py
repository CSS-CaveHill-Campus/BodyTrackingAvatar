import arcade
from arcade import View, Window
from constants import *

class MainView(View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    
def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()

