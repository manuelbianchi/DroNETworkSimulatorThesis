import src.utilities.utilities as util
import numpy as np
#from src.entities.uav_entities import Drone



from src.routing_algorithms.CPVF_routing import CPVF_routing


class SVF_routing(CPVF_routing):
    def __init__(self, drone, simulator):
        CPVF_routing.__init__(self, drone, simulator)
        drone.type_drone = "SVF"


