class Message:
    def __init__(self, topic: str, payload: str):
        self.topic: str = topic
        self.payload: bytes = payload.encode("utf-8")
