from __future__ import annotations

import time
import cv2
from datetime import datetime

from edgevisionx.nodes.base import Node
from edgevisionx.utils import ThreadingLocked


class CameraNode(Node):
    """
    Camera capture node with automatic reconnection, FPS control, and health monitoring.

    Args:
        config (Dict[str, Any]): Configuration dictionary with the following keys:
            source (int | str, optional): Camera index (0, 1, ...) or video file path/RTSP URL.
                Defaults to 0.
            width (int, optional): Target frame width in pixels. Defaults to 640.
            height (int, optional): Target frame height in pixels. Defaults to 480.
            fps (int, optional): Target frames per second. Defaults to 30.

    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'frame' (np.ndarray): Captured frame
            - 'frame_id' (int): Sequential frame identifier
            - 'timestamp' (float): Capture timestamp
            - 'shape' (tuple): Frame dimensions (height, width, channels)

    Example:
        >>> node = CameraNode(config={'source': 0, 'width': 1280, 'height': 720})
        >>> node.setup()
        >>> output = node()
        >>> print(output['frame_id'], output['shape'])

    Note:
        For video files, the source should be a file path string. For live cameras,
        use an integer index (typically 0 for the default camera).
    """

    def setup(self):
        self.source = self.config.get("source", 0)
        self.target_width = self.config.get("width", 640)
        self.target_height = self.config.get("height", 480)
        self.target_fps = self.config.get("fps", 30)

        self.cap = None

        self._frame_buffer = None  # TODO: Add frame buffer logic
        self._metrics.update({
            'fps_actual': 0,
            'health_status': 'initializing',
            'frame_count': 0
        })

        if not self._open_camera():
            self.logger.error(
                f"Failed to open camera source: {self.source}. "
                f"Make sure the camera is connected and accessible. "
            )
        self._initialized = True

    def _open_camera(self) -> bool:
        """Internal method to setup the camera"""
        self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.target_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.target_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)

        # warm up
        for _ in range(5):
            ret, _ = self.cap.read()
            if not ret:
                self.logger.warning(
                    "Camera opened but failed to read frames during warmup")
                return False

        self._metrics['health_status'] = 'healthy'
        return True

    @ThreadingLocked()
    def __call__(self):
        """
        This function would return an image frame captured using the camera
        Other features: add frame buffer, check for reconnections, return frame id, 
        """
        ret, frame = self.cap.read()

        if not ret:
            self._metrics['health_status'] = 'error'
            self.logger.error(
                "Failed to grab frame from camera. Camera may be disconnected.")

        self._metrics['frame_count'] += 1

        output = {
            'frame': frame,
            'frame_id': self._metrics['frame_count'],
            'timestamp': datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"),
            'shape': frame.shape,
        }

        return output

    def teardown(self):
        """Release the video capture object"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None


if __name__ == "__main__":

    camera_node = CameraNode(
        config={'source': 'edgevisionx/assets/videos/test_video.mp4'})
    camera_node.setup()
    while True:
        output = camera_node()
        cv2.imshow("Camera Feed", output['frame'])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera_node.release()
    cv2.destroyAllWindows()
