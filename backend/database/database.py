from config._secrets import _MONGO_URI

from motor.motor_tornado import MotorClient

class DBClient():
    def __init__(self) -> None:
        self.client = MotorClient(_MONGO_URI)