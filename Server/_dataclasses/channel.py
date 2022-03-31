from dataclasses import dataclass
from .user import User

class Channel:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.kwargs = kwargs

    @property
    def to_dict(self):
        return self.kwargs