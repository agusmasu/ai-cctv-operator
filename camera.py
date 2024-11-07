class Camera:
    def __init__(self, camera_id, name, location):
        self.camera_id = camera_id
        self.name = name
        self.location = location

    def to_json(self):
        return {
            "camera_id": self.camera_id,
            "name": self.name,
            "location": self.location,
        }

def get_user_cameras():
    return [
        Camera(camera_id=1, name="Camera 1", location="Garage"),
        Camera(camera_id=2, name="Camera 2", location="Garage"),
    ]