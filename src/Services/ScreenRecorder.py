import time 
import logging
import imageio
import pyautogui
import numpy as np
from PIL import Image


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MyLogger')


class ScreenRecorder:

    def __init__(
        self, 
        x: int=100, 
        y: int=100, 
        width: int=500, 
        height: int=500,
        fps: int=20,
        filename: str = "Record.mp4"
    ):
        self._x = x 
        self._y = y 
        self._width = width 
        self._height = height 
        self._filename = filename 
        self._fps = fps 

    def __get_region(self) -> tuple[int, int, int, int]:
        return self._x, self._y, self._width, self._height

    @property 
    def record(self):
        logger.debug(f"Record has been started!")
        screenshots: list[np.array] = []
        while True:
            try:
                time.sleep(1 / self._fps)
                screenshot: Image = pyautogui.screenshot(region=self.__get_region())
                screenshot_np: np.array = np.array(screenshot) 
                screenshots.append(screenshot_np)
            except KeyboardInterrupt:
                with imageio.get_writer(self._filename, fps=self._fps) as video_writer:
                    for frame in screenshots:
                        video_writer.append_data(frame)
                logger.debug(f"Screen recording saved as '{self._filename}'")
                exit(-1)


if __name__ == "__main__":
    ScreenRecorder(filename="..\Footage\Record.mp4").record