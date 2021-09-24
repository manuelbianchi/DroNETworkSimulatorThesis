
import src.utilities.utilities as util
import numpy as np
#from src.entities.uav_entities import Drone



from src.routing_algorithms.BASE_routing import BASE_routing






class CPVF_routing(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        drone.type_drone = "CPVF"



    def relay_selection(self, opt_neighbors):
        """ arg min score  -> geographical approach, take the drone closest to the depot """

        """Qui andiamo a prendere il prossimo drone che è più vicino al depot per inviare i pacchetti.Questo drone è chiamato
         path parent e viene controllato se è connesso, cioè se attraverso una rete di droni o direttamente riesce a comunicare con 
         il depot.
         Nel caso in cui il drone non ha vicini, allora dovrà avvicinarsi al depot"""



        bestDrone = None
        #bestDroneDistance = np.inf


        for pck, droneIstance in opt_neighbors:
            exp_position = self.__estimated_neighbor_drone_position(pck)
            neighbors_to_depot_distance = util.euclidean_distance(exp_position, self.simulator.depot.coords)
            myDrone_to_depot_distance = util.euclidean_distance(self.drone.coords, self.simulator.depot.coords)


            #se il nostro vicino è connesso ed è più vicino al depot, viene preso in considerazione per inviare i
            #messaggi...
            if (droneIstance.routing_algorithm.is_connected == True) and\
            (neighbors_to_depot_distance < myDrone_to_depot_distance):
                  bestDrone = droneIstance

            #altrimenti se è il nostro drone più vicino, il bestdDrone sarà lui.
            elif(self.drone.routing_algorithm.is_connected == True) and\
                    (myDrone_to_depot_distance < neighbors_to_depot_distance) and\
                    (myDrone_to_depot_distance <= util.config.DEPOT_COMMUNICATION_RANGE) and\
                    (self.drone.communication_range >= myDrone_to_depot_distance):
                bestDrone = self.drone
                #self.lazy_movement(self.drone,pck,self.drone.simulator.cur_step)

             # Nel caso in cui il drone parent non è ancora connesso, ma è più vicino al depot allora verrà
             # considerato come miglior drone. Quindi verranno inviati i pacchetti al più vicino anche se
             # non è connesso. (NON SO SE LASCIARLO)
            elif(droneIstance.routing_algorithm.is_connected == False) and\
                    (neighbors_to_depot_distance < myDrone_to_depot_distance):

                    bestDrone = droneIstance

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










