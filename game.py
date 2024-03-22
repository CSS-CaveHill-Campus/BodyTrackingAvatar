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
        parts = ["HEAD", "TORSO", "LEFT_HAND", "RIGHT_HAND", "LEFT_FOOT", "RIGHT_FOOT"]
        self.body_parts = {}
        for part in parts:
            if part == "TORSO":
                self.body_parts[part] = arcade.Sprite(f"./assets/{part.lower()}.png", SPRITE_SCALE * 1.25)
            else:
                self.body_parts[part] = arcade.Sprite(f"./assets/{part.lower()}.png", SPRITE_SCALE)


    def on_draw(self):
        self.clear()

        for part_sprite in self.body_parts.values():
            part_sprite.draw()

    def on_update(self, delta_time: float):
        try:
            landmarkList = self.parent_conn.recv()
        except EOFError:
            print("Child process has exited.")
            self.p.kill()
            raise SystemExit
        
        landmarks = landmarkList.landmark

        for part_name, sprite in self.body_parts.items():
            pos_x, pos_y = self.get_position(part_name, landmarks)
            sprite.set_position(pos_x, pos_y)
            
    def get_position(self, key, landmarks):
        """Used to get the landmark relating to a specific body part
        
        Args:
            key (str): The name of the body part.
            landmarks (NormalizedLandmark): The list of the landmarks for indexing
            
        Returns:
            tuple (x, y): The x, y coord of the part"""
        
        position_x, position_y = None, None

        if key == "HEAD":
            position_x, position_y = landmarks[HEAD_INDEX].x * SCREEN_WIDTH, landmarks[HEAD_INDEX].y * SCREEN_WIDTH

        elif key == "TORSO":
            # Yes I could do the diagnoals, but the upper half of the model is longer than the lower half.
            ul_torso, ur_torso, ll_torso = landmarks[UPPER_LEFT_TORSO], landmarks[UPPER_RIGHT_TORSO], landmarks[LOWER_LEFT_TORSO]

            position_x = (ul_torso.x * SCREEN_WIDTH + ur_torso.x * SCREEN_WIDTH) // 2
            # position_y = (ul_torso.y * SCREEN_HEIGHT + ll_torso.y * SCREEN_HEIGHT) // 2

            head: arcade.Sprite = self.body_parts["HEAD"]

            position_y = ul_torso.y * SCREEN_HEIGHT + 128

            # if position_y > SCREEN_HEIGHT:
            #     # Incase only the upper torso is visible
            #     position_y = self.body_parts["HEAD"].center_y + (64 * SPRITE_SCALE // 2) + 20

        elif "FOOT" in key:
            toe_x = landmarks[eval(f"{key}_TOE_INDEX")].x * SCREEN_WIDTH
            heel_x, position_y = landmarks[eval(f"{key}_HEEL_INDEX")].x * SCREEN_WIDTH, landmarks[eval(f"{key}_HEEL_INDEX")].y * SCREEN_HEIGHT

            position_x = (toe_x + heel_x) // 2
        
        elif "HAND" in key:
            finger_x = landmarks[eval(f"{key}_FINGER_INDEX")].x * SCREEN_WIDTH
            wrist_x, position_y = landmarks[eval(f"{key}_WRIST_INDEX")].x * SCREEN_WIDTH, landmarks[eval(f"{key}_WRIST_INDEX")].y * SCREEN_HEIGHT

            position_x = (wrist_x + finger_x) // 2
            
        return position_x, SCREEN_HEIGHT - (position_y)
        

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()

