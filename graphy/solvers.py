from mip import Model, xsum, MAXIMIZE


# Class to solve the water distribution network
class SolverWaterDistribution:
    def __init__(self):
        self.model = None
        self.x = None
        self.y = None

    def create_model(self, network):
        # Getting the origin and destination
        for node, prop in network.nodes.data("node_prop"):
            if prop == "origin":
                origin = node
            elif prop == "dest":
                dest = node
        
        # Create a model
        self.model = Model()  # default is sense MINIMIZE and solver CBC
        
        # Defining the saving variables
        self.x = x = [self.model.add_var(var_type="B")
                      for i in network.nodes]
        self.y = y = {(i, j) : self.model.add_var(var_type="B")
                      for i, j in network.edges}
        
        # Defining the objective function
        self.model.objective = xsum(y_ij for y_ij in y.values())
            
        # Defining the constraints
        self.model += x[origin] == 0
        self.model += x[dest] == 1
        
        for v, w in network.edges:
            self.model += y[v, w] >= x[v] - x[w]
            self.model += y[v, w] >= x[w] - x[v]
            
            if network[v][w]["color"] == "red":
                self.model += y[v, w] == 0
    
    def optimize(self):
        self.model.optimize()

    @property
    def objective_value(self):
        return self.model.objective_value

    @property
    def disconnected_nodes(self):
        return [node for node, var in enumerate(self.x) if var.x]

    @property
    def edges_to_remove(self):
        return [edge for edge, var in self.y.items() if var.x]

# Class to solve the military distribution network
class SolverMilitaryDistribution:
    def __init__(self):
        self.model = None
        self.x = None
        self.y = None

    def create_model(self, network, fire_power=6):
        # Create a model
        self.model = Model(sense=MAXIMIZE)
        
        # Defining the variables
        self.x = x = [None]*network.number_of_nodes()
        self.y = y = [None]*network.number_of_nodes()
        
        for i in network.nodes:
            x[i] = self.model.add_var(var_type="B")
            y[i] = self.model.add_var(var_type="B")
            
            if network.nodes[i]["node_prop"] == "headquarters":
                self.model += x[i] == 0
        
        # Defining the objective function
        self.model.objective = xsum(x_i for x_i in x)
        
        # Defining the constraints
        self.model += xsum(network.nodes[i]["endurance"]*y_i
                           for i, y_i in enumerate(y)) <= fire_power
        
        for v, w in network.edges:
            self.model += y[v] + y[w] >= x[v] - x[w]
            self.model += y[v] + y[w] >= x[w] - x[v]

    def optimize(self):
        self.model.optimize()

    @property
    def objective_value(self):
        return self.model.objective_value

    @property
    def nodes_to_remove(self):
        return [node for node, var in enumerate(self.y) if var.x]
