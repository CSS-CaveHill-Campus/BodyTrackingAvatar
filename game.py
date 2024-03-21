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
        self.head = arcade.Sprite("./assets/head.png", 2)

    def on_draw(self):
        self.clear()

        self.head.draw()

    def on_update(self, delta_time: float):
        try:
            landmarkList = self.parent_conn.recv()
            landmarks = landmarkList.landmark
            head_pos_x, head_pos_y = landmarks[HEAD_INDEX].x, landmarks[HEAD_INDEX].y
            if head_pos_y > 1: # If it's greater than 1, then it isn't visible (probably)
                return 
            self.head.set_position(head_pos_x * SCREEN_WIDTH, SCREEN_HEIGHT - head_pos_y * SCREEN_HEIGHT)
            # raise EOFError
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

