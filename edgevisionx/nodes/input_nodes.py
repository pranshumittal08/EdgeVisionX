from __future__ import annotations

from threading import Lock
import time
import cv2
from typing import Dict, Tuple, List, Optional, Union
from base import Node


class CameraNode(Node):
    """
    Camera capture node with automatic reconnection, FPS control, and health monitoring.

    User config:
        source: int | str - Camera index or RTSP URL
        width: int - Frame width (default: 640)
        height: int - Frame height (default: 480)
        fps: int - Target FPS (default: 30)
        reconnect_attempts: int - Max reconnection tries (default: 5)
    """

    def setup(self):
        self.source = self.config.get("source", 0)
        self.target_width = self.config.get("width", 640)
        self.target_height = self.config.get("height", 480)
        self.target_fps = self.config.get("fps", 30)

        self.cap = None
        self._lock = Lock()

        self._frame_buffer = None
        self._metrics.update({
            'fps_actual': 0,
            'health_status': 'initializing',
            'frame_count': 0
        })

        if not self._open_camera():
            raise RuntimeError(
                f"Failed to open camera source: {self.source}. "
                f"Make sure the camera is connected and accessible. "
            )
        self._initialized = True

    def _open_camera(self):
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
                print("Warning: Camera opened but failed to read frames during warmup")
                return False

        self._metrics['health_status'] = 'healthy'
        return True

    def __call__(self):
        """
        This function would return an image frame captured using the camera
        Other features: add frame buffer, check for reconnections, return frame id, 
        """
        ret, frame = self.cap.read()

        if not ret:
            self._metrics['health_status'] = 'error'
            raise RuntimeError(
                "Failed to grab frame from camera. Camera may be disconnected.")

        self._metrics['frame_count'] += 1

        output = {
            'frame': frame,
            'frame_id': self._metrics['frame_count'],
            'timestamp': time.time(),
            'shape': frame.shape,
        }

        return output

    def release(self):
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
