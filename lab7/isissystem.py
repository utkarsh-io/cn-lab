import heapq

class ISISRouter:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}     
        self.lsdb = {}          
        self.routing_table = {} 

    def generate_lsp(self):
       
        return {self.name: dict(self.neighbors)}

    def receive_lsp(self, lsp):
        for router, links in lsp.items():
            if router not in self.lsdb or self.lsdb[router] != links:
                self.lsdb[router] = links

    def run_dijkstra(self):
     
        graph = self.lsdb
        dist = {node: float('inf') for node in graph}
        prev = {node: None for node in graph}
        dist[self.name] = 0

        pq = [(0, self.name)]
        while pq:
            current_dist, node = heapq.heappop(pq)
            if current_dist > dist[node]:
                continue
            for neighbor, cost in graph.get(node, {}).items():
                new_cost = current_dist + cost
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = node
                    heapq.heappush(pq, (new_cost, neighbor))

        
        for dest in graph:
            if dest == self.name:
                self.routing_table[dest] = (0, self.name)
            elif prev[dest]:
                # Trace first hop
                nxt = dest
                while prev[nxt] != self.name:
                    nxt = prev[nxt]
                    if nxt is None:
                        break
                if nxt:
                    self.routing_table[dest] = (dist[dest], nxt)

    def display_table(self):
       
        print(f"\nRouter {self.name} Routing Table:")
        print("Destination\tCost\tNext Hop")
        for dest, (cost, nxt) in sorted(self.routing_table.items()):
            print(f"{dest}\t\t{cost}\t{nxt}")
        print("-" * 30)


class ISISNetwork:
    def __init__(self, topology):
        
        self.routers = {r: ISISRouter(r) for r in topology}
        for r, neighbors in topology.items():
            self.routers[r].neighbors = neighbors

    def flood_link_states(self):
        
        for r in self.routers.values():
            for other in self.routers.values():
                other.receive_lsp(r.generate_lsp())

    def compute_routes(self):
        
        for r in self.routers.values():
            r.run_dijkstra()

    def display_all(self):
       
        for r in sorted(self.routers):
            self.routers[r].display_table()


if __name__ == "__main__":
    
    topology = {
        "R1": {"R2": 1, "R3": 4},
        "R2": {"R1": 1, "R3": 2, "R4": 7},
        "R3": {"R1": 4, "R2": 2, "R4": 3, "R5": 5},
        "R4": {"R2": 7, "R3": 3, "R5": 1},
        "R5": {"R3": 5, "R4": 1}
    }

    net = ISISNetwork(topology)
    net.flood_link_states()
    net.compute_routes()
    net.display_all()
