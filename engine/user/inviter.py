from common.api.customer.customer import Customer
from common.models.customer import CustomerModel
from engine.cache import Cache
import uuid


class InviteUserToClient:
    def __init__(self):
        self._storage = Cache("inviter")

    def get_invite_customer_from_id(self, identification: str) -> Customer:
        client_id = self._storage.get(f"invite_{identification}", None)
        if client_id is None:
            raise RuntimeError("Unknown invite")

        return Customer(CustomerModel.get_from_id(client_id))

    def create_invite(self, customer: Customer) -> str:
        invite = uuid.uuid4().hex
        self._storage.set(f"invite_{invite}", customer.id)
        return invite
