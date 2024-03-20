import arcade
from arcade import View, Window
from constants import *
from mediator import my_mediator

class MainView(View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        print(my_mediator.get_last_position())

    
def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()

