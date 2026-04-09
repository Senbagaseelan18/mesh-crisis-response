from openenv import OpenEnvClient
from models import MeshObservation, MeshAction

class MeshNetworkClient(OpenEnvClient[MeshObservation, MeshAction]):
    """
    Client for the Emergency Mesh Network environment.
    """
    def __init__(self, url: str):
        super().__init__(url, MeshObservation, MeshAction)