
import math
import time

INF = 10**9  



class Router:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  
        self.table = {}    

    def initialize_table(self):

        self.table[self.name] = (0, self.name)
        for nb, cost in self.neighbors.items():
            self.table[nb] = (cost, nb)

    def prepare_update(self):

        updates = {}
        for nb in self.neighbors:
            adv = {}
            for dest, (cost, nxt) in self.table.items():
                if nxt == nb and dest != nb:
                    adv[dest] = INF  # poison reverse
                else:
                    adv[dest] = cost
            updates[nb] = adv
        return updates

    def process_update(self, from_nb, vector):

        changed = False
        cost_to_nb = self.neighbors[from_nb]

        for dest, nb_cost in vector.items():
            new_cost = cost_to_nb + nb_cost
            cur_cost, cur_next = self.table.get(dest, (INF, None))

         
            if new_cost < cur_cost:
                self.table[dest] = (new_cost, from_nb)
                changed = True

           
            elif cur_next == from_nb and cur_cost != new_cost:
                self.table[dest] = (new_cost, from_nb)
                changed = True

        return changed



class Network:
    def __init__(self, graph):

        self.routers = {name: Router(name) for name in graph}
        for name, neighbors in graph.items():
            self.routers[name].neighbors = neighbors

        self.round = 0
        self.message_count = 0

    def initialize(self):
        for r in self.routers.values():
            r.initialize_table()

    def step(self):
       
        updates = []
        for r in self.routers.values():
            per_nb = r.prepare_update()
            for nb, vec in per_nb.items():
                updates.append((r.name, nb, vec))

        changed_any = False
        for src, dst, vec in updates:
            if dst in self.routers:
                changed = self.routers[dst].process_update(src, vec)
                changed_any = changed_any or changed
                self.message_count += 1

        self.round += 1
        return changed_any

    def run_until_convergence(self, max_rounds=100):
        
        self.initialize()
        for _ in range(max_rounds):
            changed = self.step()
            if not changed:
                break
        return self.round, self.message_count

    def display_tables(self):
       
        print("\nFinal Routing Tables after Convergence:\n")
        for name in sorted(self.routers):
            print(f"Router {name}:")
            print("Destination\tCost\tNext Hop")
            for dest, (cost, nxt) in sorted(self.routers[name].table.items()):
                c = "∞" if cost >= INF else cost
                print(f"{dest}\t\t{c}\t{nxt}")
            print("-" * 30)


if __name__ == "__main__":
   
    topology = {
        "A": {"B": 1, "C": 1},
        "B": {"A": 1, "D": 1},
        "C": {"A": 1, "D": 2, "E": 3},
        "D": {"B": 1, "C": 2, "E": 1},
        "E": {"C": 3, "D": 1, "F": 2},
        "F": {"E": 2}
    }

    
    net = Network(topology)
    rounds, messages = net.run_until_convergence(max_rounds=50)

  
    print("\n--- RIP Simulation Results ---")
    print(f"Total rounds to converge: {rounds}")
    print(f"Total messages exchanged: {messages}")


    net.display_tables()

