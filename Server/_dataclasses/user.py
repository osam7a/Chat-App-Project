from dataclasses import dataclass

class User:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.kwargs = kwargs

    @property
    def to_dict(self):
        return self.kwargs