import src.utilities.utilities as util
import numpy as np
#from src.entities.uav_entities import Drone



from src.routing_algorithms.BASE_routing import BASE_routing


class FLOOR_routing(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        drone.type_drone = "FLOOR"


    def relay_selection(self, opt_neighbors):
        """ arg min score  -> path parent approach, take the drone parent or relay the packet directly to the depot """
        bestDrone = None
        #bestDroneDistance = np.inf

        for pck, droneIstance in opt_neighbors:
            exp_position = self.__estimated_neighbor_drone_position(pck)
            neighbors_to_depot_distance = util.euclidean_distance(exp_position, self.simulator.depot.coords)
            myDrone_to_depot_distance = util.euclidean_distance(self.drone.coords, self.simulator.depot.coords)

            # # se il nostro drone è dentro il raggio del depot, inviamo i pacchetti al depot.
            # if self.drone.routing_algorithm.is_connected and\
            #         myDrone_to_depot_distance <= util.config.COMMUNICATION_RANGE_DRONE:
            #     bestDrone = self.drone
            #     break
            # altrimenti se il nostro parent è un drone che è connesso alla rete e noi siamo connessi a lui, allora sarà
            # lui il nostro bestDrone a cui inviare i pacchetti
            # self.drone.parentPath.identifier != self.drone.depot.identifier and\
            if (droneIstance.routing_algorithm.is_connected) and self.drone.parentPath != None and\
                    droneIstance.stop and self.drone.parentPath.identifier == droneIstance.identifier:
                bestDrone = droneIstance
                break
            # altrimenti se il nostro drone, trova un drone vicino, il quale è più vicino di lui al depot, seleziona lui
            # come bestDrone al quale inviare i pacchetti
            elif self.drone.routing_algorithm.is_connected is False and \
                neighbors_to_depot_distance < myDrone_to_depot_distance :
                   bestDrone = droneIstance

            #altrimenti è il nostro drone il bestDrone
            else:
                bestDrone = self.drone

        return bestDrone


    def __estimated_neighbor_drone_position(self,hello_message) ->float:
        """ estimate the current position of the drone """

        # get known info about the neighbor drone
        hello_message_time = hello_message.time_step_creation
        known_position = hello_message.cur_pos
        known_speed = hello_message.speed
        known_next_target = hello_message.next_target

        # compute the time elapsed since the message sent and now
        # elapsed_time in seconds = elapsed_time in steps * step_duration_in_seconds
        elapsed_time = (self.simulator.cur_step - hello_message_time) * self.simulator.time_step_duration  # seconds

        # distance traveled by drone
        distance_traveled = elapsed_time * known_speed

        # direction vector
        a, b = np.asarray(known_position), np.asarray(known_next_target)
        v_ = (b - a) / np.linalg.norm(b - a)

        # compute the expect position
        c = a + (distance_traveled * v_)

        return tuple(c)