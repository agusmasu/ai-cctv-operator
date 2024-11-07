from abc import ABC, abstractmethod


class StreamProvider(ABC):

    # This method should return the current frame from the stream.
    @abstractmethod
    def get_current_stream_frame(self, camera):
        pass


class MockedStreamProvider(StreamProvider):

    def __init__(self, image_content=None):
        self.image_content = image_content

    def get_current_stream_frame(self, camera):
        return self.image_content
