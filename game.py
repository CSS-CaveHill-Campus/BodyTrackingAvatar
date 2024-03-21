import arcade
from arcade import View, Window
from constants import *
from multiprocessing import Process, Pipe
from tracker import track

class MainView(View):
    def __init__(self):
        super().__init__()
        self.parent_conn, child_conn = Pipe()
        self.p = Process(target=track, args=(child_conn, ))
        self.p.start()

    def setup(self):
        pass
    
    def on_update(self, delta_time: float):
        try:
            self.positions = self.parent_conn.recv()
            self.p.kill()
            raise SystemExit
        except EOFError:
            print("Child process has exited.")
            self.p.kill()
            raise SystemExit


    
def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()

