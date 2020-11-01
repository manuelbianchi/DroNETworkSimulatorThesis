
import src.utilities.utilities as util
import numpy as np

from src.routing_algorithms.BASE_routing import BASE_routing

#function that calculates the intermediate coordinates after a period of time
def real_position(cur_pos, next_target, speed, time_step_creation, curr_step):
    x0,y0 = cur_pos
    xf,yf = next_target
    #calculate angular coefficient
    if (xf - x0) != 0:
        m = (yf - y0) / (xf - x0)
    else:
        m = np.inf
    angle = np.arctan(m)
    d = speed * (curr_step - time_step_creation)
    xn = d*np.sin(angle)
    yn = d*np.cos(angle)
    expected_position = (xn,yn)
    return expected_position


class GeoRouting(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)






    def relay_selection(self, opt_neighbors):
        """ arg min score  -> geographical approach, take the drone closest to the depot """
        #bestDrone and relative distace are set to 'None' and infinity.
        bestDrone = None
        bestDroneDistance = np.inf
        # for every neighbors_drone we take the distance from it to the depot. Then, we take the distance between our drone and depot and finally we compare
        # the two distance taking the best distance and so we take the bestdrone.
        for pck, droneIstance in opt_neighbors:


            real_pos = real_position(pck.cur_pos,pck.next_target,pck.speed,pck.time_step_creation,self.drone.simulator.cur_step )
            neighbors_to_depot_distance = util.euclidean_distance(real_pos, self.simulator.depot.coords)
            myDrone_to_depot_distance = util.euclidean_distance(self.drone.coords, self.simulator.depot.coords)

            #check if we are enough close to depot
            if myDrone_to_depot_distance < util.config.COMMUNICATION_RANGE_DRONE:
                bestDrone = self.drone
            elif myDrone_to_depot_distance > neighbors_to_depot_distance and neighbors_to_depot_distance < bestDroneDistance:
                bestDrone = droneIstance
                bestDroneDistance = neighbors_to_depot_distance

        return bestDrone


