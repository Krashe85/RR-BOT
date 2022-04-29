from enum import Enum


class OrderStatus(Enum):
    SUCCESS = "success"
    WAIT = "wait"
    CANCELED = "canceled"
