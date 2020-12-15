from behaviour.behaviour import Behaviour
from pvector import Pvector
from node import Node

import math, random

class WalkerRoaming(Behaviour):

    def __init__(self, agent):
        self.host = agent

        self.u_max = 0.06
        self.vision_range = 1
        self.time = 100

        agent.agent_type = 'walker'
        self.approach_error = 2 * self.u_max #this modify
        self.host.set_v_max(0.05)
        self.safe_distance = 1
        self.preceding_node = None
        #self.walk_to_point(self.next_node.position)

#
    def set_roaming_area(self, center_vector, radius):
        self.center_vector = center_vector
        self.radius = radius

    def set_closest_node(self, node):
        self.next_node = node

        self.next_point = node.position - self.host.heading
        self.update_next_point_vector()

    def update_next_point_vector(self):
        host = self.host
        vector_next_point = self.next_point - host.position
        host.distance_to_next_point = vector_next_point.magnitude()
        vector_next_point.normalize()
        host.heading = vector_next_point.copy()

    def next_point_attraction(self):
        host = self.host
        host.acceleration = host.acceleration + host.heading.multiply(host.alpha)

    def pick_next_point(self):
        self.preceding_node = self.next_node
        self.preceding_point = self.next_point

        self.next_node = self.next_node.connected_nodes[self.random_roll()]
        self.find_distance_to_road() #

        r = self.radius*random.random()
        phi = 2*math.pi*random.random()
        x = r*math.cos(phi)
        y = r*math.sin(phi)
        delta = Pvector(x,y)

        self.next_point = self.center_vector + delta # shift point from road




    def random_roll(self):
        number = random.randint(0,len(self.next_node.connected_nodes)-1)  #pick random Node from available
        return number

    def random_destination(self):
        l = len(self.host.dest_list)
        dest = self.host.dest_list[random.randrange(0,l,1)]
        return dest

    def keep_distance_to_road(self):
        distance_to_road = self.find_distance_to_road()
        #print(distance_to_road)
        host = self.host
        if (distance_to_road < self.safe_distance):
            #exert force perpendicular from road
            host.acceleration = host.acceleration + self.n.multiply(host.alpha*0.1)
            pass

        if (distance_to_road > 2 * self.safe_distance):
            #bring walker closer to road
            host.acceleration = host.acceleration - self.n.multiply(host.alpha*0.1)
            pass

    def find_distance_to_road(self):
        distance = 0
        point2 = self.next_node.position
        point1 = self.preceding_node.position
        #Equation for the line
        A = point2.y - point1.y
        B = point1.x - point2.x
        D = (point2.y - point1.y)*point1.x - (point2.x - point1.x)*point1.y

        n = Pvector(A,B)
        x1 = self.host.position.x
        y1 = self.host.position.y
        distance = (D - A*x1 - B*y1)/n.magnitude()
        self.n = n
        return distance
#---------------------------------------
    def update_behaviour_old(self):
        agent = self.host

        self.reset_acceleration()
        self.next_point_attraction()
        #self.detect_agents_in_sector(agent.agent_range, agent.detection_angle)
        self.detect_agents_in_sector(agent.agent_close_range/2, 20)
        if not (self.preceding_node == None):
            self.keep_distance_to_road()

    def update_velocity_old(self):
        agent = self.host


        if (self.is_velocity_negative()):
            agent.velocity = Pvector(0,0)
        else:
            agent.velocity = agent.velocity + agent.acceleration
            agent.velocity.limit_magnitude(agent.v_max)

#---------------------------------------
#New Velocity And Position
#Behaviours of the walkers
    def update_behaviour(self):
        if(self.time > 0):
            self.time = self.time - 1
        else:
            self.time = 0
            self.t = 0
        #self.detect_agents_in_sector(self.u_max,20)

    def update_velocity(self):
        agent = self.host

        u_act = agent.velocity

        #self.check_time()
        self.t = 0 #for now
        self.s = 0.5
        #calc coefficients

        c_act = (1 - self.t)
        c_dest = c_act


        u_dest = self.destination_attraction()
        u_cur = self.curiosities_attraction()
        u_rep = self.walkers_repulsion()

        agent.velocity = u_act.multiply(c_act) + u_dest.multiply(c_dest) + u_cur + u_rep
        agent.velocity.limit_magnitude(self.u_max)

    def update_position(self):
        agent = self.host

        agent.position = agent.position + agent.velocity
        self.update_next_point_vector()

        if(agent.distance_to_next_point < self.approach_error):
            self.pick_next_point()
            self.update_next_point_vector()
            agent.velocity = Pvector.turn_vector(agent.heading, agent.velocity)
            #agent.position.show()


    def destination_attraction(self):
        delta_r = self.next_point - self.host.position
        u_dest = delta_r.multiply(self.u_max / delta_r.magnitude())
        return u_dest

    def curiosities_attraction(self):
        self.visible_curiosities = list()

        for c in self.host.curiosity_list:

            d = c.position - self.host.position
            if d.magnitude() < self.vision_range:
                self.visible_curiosities.append(c)
        u_sum = Pvector(0,0)
        n = 0
        #print(self.visible_curiosities)
        for c in self.visible_curiosities:
            delta_r = c.position - self.host.position
            u_cur = delta_r.multiply(self.u_max / delta_r.magnitude())
            c_cur = delta_r.magnitude()/self.vision_range
            u_cur = u_cur.multiply(c_cur)
            u_sum = u_sum + u_cur
            n = n + 1
        u_sum = u_sum.divide(n)
        #print("visible cur: {}, n:{}, u_sum:{}".format(len(self.visible_curiosities), n, u_sum.magnitude()))
        return u_sum

    def walkers_repulsion(self):
        people_around = list()
        for a in self.host.agent_list:
            if a.agent_type != 'walker':
                continue

            if((a.position - self.host.position).magnitude() < self.vision_range):
                people_around.append(a)

        u_sum = Pvector(0,0)
        n = 0
        for a in people_around:
            ro = -1
            #delta_r = Pvector(0,0)
            delta_r = a.position - self.host.position
            #print(delta_r.magnitude())
            if(delta_r.magnitude() != 0):
                u_rep_i = delta_r.multiply(self.u_max / delta_r.magnitude())
                c_rep_i = ro * math.exp( (-1) * delta_r.magnitude()/self.vision_range )
                #print("c_re {}".format(c_rep_i))
                u_rep_i = u_rep_i.multiply(c_rep_i)
                u_sum = u_sum + u_rep_i
                n = n + 1
        u_sum = u_sum.divide(n)
        #print("people around: {}, n:{}, u_sum:{}".format(len(people_around), n, u_sum.magnitude()))
        return u_sum
