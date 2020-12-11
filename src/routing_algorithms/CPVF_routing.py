import src.entities.uav_entities as uav
import src.utilities.utilities as util
import numpy as np
import time


from src.routing_algorithms.BASE_routing import BASE_routing
from src.routing_algorithms.georouting import real_position

from src.utilities import config





class CPVF_routing(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)



    def relay_selection(self, opt_neighbors):
        """ arg min score  -> geographical approach, take the drone closest to the depot """

        """Qui andiamo a prendere il prossimo drone che è più vicino al depot per inviare i pacchetti.Questo drone è chiamato
         path parent e viene controllato se è connesso, cioè se attraverso una rete di droni o direttamente riesce a comunicare con 
         il depot
         Nel caso in cui il drone non ha vicini, allora dovrà avvicinarsi al depot"""



        bestDrone = None
        bestDroneDistance = np.inf


        #ToDo aggiungere la direzione del drone, che deve essere verso il depot.
        if len(opt_neighbors) == 0:
            self.drone.stop = True
        for pck, droneIstance in opt_neighbors:
            exp_position = self.__estimated_neighbor_drone_position(pck)
            neighbors_to_depot_distance = util.euclidean_distance(exp_position, self.simulator.depot.coords)
            myDrone_to_depot_distance = util.euclidean_distance(self.drone.coords, self.simulator.depot.coords)


            if (self.drone.routing_algorithm.is_connected == True):
                self.lazy_movement(self.drone,pck,self.drone.simulator.cur_step)
            else:
                self.drone.stop = False

            if (droneIstance.routing_algorithm.is_connected == True) and\
                (neighbors_to_depot_distance < myDrone_to_depot_distance):
                  bestDrone = droneIstance
                  bestDroneDistance = neighbors_to_depot_distance
                  self.lazy_movement(bestDrone,pck,bestDrone.simulator.cur_step)
                 # check if we are enough close to depot
            elif(self.drone.routing_algorithm.is_connected == True) and\
                    (myDrone_to_depot_distance < neighbors_to_depot_distance) and\
                    (myDrone_to_depot_distance <= util.config.DEPOT_COMMUNICATION_RANGE) and\
                    (self.drone.communication_range >= myDrone_to_depot_distance):
                bestDrone = self.drone
                bestDroneDistance = myDrone_to_depot_distance
                self.lazy_movement(self.drone,pck,self.drone.simulator.cur_step)

             # il drone parent non è ancora connesso, quindi il nostro drone aspetterà, un determinato quantitativo di tempo
             # per far si che il drone parent trovato si connetta. Altrimenti ritorna in movimento.
            elif(droneIstance.routing_algorithm.is_connected == False) and\
                    (neighbors_to_depot_distance < myDrone_to_depot_distance):
                if(self.lazy_movement(self.drone,pck,self.drone.simulator.cur_step) == True):
                    bestDroneDistance = neighbors_to_depot_distance
                    bestDrone = droneIstance

            elif(droneIstance.routing_algorithm.is_connected == False) and\
                    (neighbors_to_depot_distance > myDrone_to_depot_distance):
                droneIstance.stop = False

        #print("Drone",self.drone,"DroneParent",bestDrone)
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

    def lazy_movement(self,drone,pck,cur_step):
        """Qui vengono rallentati i movimenti del drone e abbiamo vari casi:
       1. il drone ha trovato il suo path parent ma non è ancora connesso, quindi aspetta un po' di tempo stando sulla posizione corrente
          aspettando che il drone "path parent" si 'connetta', altrimenti tornerà a muoversi.
       2. il drone ha trovato il suo path parent ed è anche connesso, in questo caso se dopo molto tempo rimane nella stessa posizione
          viene inviato dal drone un pacchetto al suo path parent che attraverserà tutta la rete connessa per verificare se c'è un ciclo
          (se il pacchetto inviato dal drone sorgente ritorna a se stesso)
          in caso di ciclo il drone ricomincerà a muoversi"""

        if (drone.routing_algorithm.is_connected) == False:
            while(pck.time_step_creation < cur_step - config.OLD_HELLO_PACKET):
                drone.stop = True
                if(drone.routing_algorithm.is_connected) == True:
                   return True
            drone.stop = False
            return False
        elif (drone.routing_algorithm.is_connected) == True:
            # while (drone.routing_algorithm.is_connected):
            #     if(self.drone.simulator.cur_step < pck.time_step_creation + config.OLD_HELLO_PACKET )
                 drone.stop = True
                 if(pck.time_step_creation > cur_step - config.OLD_HELLO_PACKET ) and (self.there_exists_cycle == True):
                     drone.stop = False
                     self.there_exists_cycle = False


        else :
                 drone.stop = False

                 return

    def unicast_message(self, packet, src_drone, dst_drone, curr_step):
        self.simulator.network_dispatcher.send_packet_to_medium(packet, src_drone, dst_drone, curr_step)
        #print("Packet: ",packet,"Drone sorgente",src_drone,"Drone destinatario ",dst_drone)







