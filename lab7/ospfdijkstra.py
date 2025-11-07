import heapq

class OSPFRouter:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # neighbor -> link cost
        self.link_state_db = {}  # router -> {neighbor: cost}
        self.routing_table = {}  # destination -> (cost, next_hop)

    def generate_lsa(self):
      
        return {self.name: dict(self.neighbors)}

    def receive_lsa(self, lsa):
      
        for router, links in lsa.items():
            self.link_state_db[router] = links

    def run_dijkstra(self):
       
        graph = self.link_state_db
        dist = {node: float('inf') for node in graph}
        prev = {node: None for node in graph}
        dist[self.name] = 0

        pq = [(0, self.name)]
        while pq:
            current_dist, node = heapq.heappop(pq)
            if current_dist > dist[node]:
                continue
            for neighbor, cost in graph[node].items():
                new_cost = current_dist + cost
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = node
                    heapq.heappush(pq, (new_cost, neighbor))

        # Build routing table (destination, cost, next_hop)
        for dest in graph:
            if dest == self.name:
                self.routing_table[dest] = (0, self.name)
            elif prev[dest]:
                # Find first hop along path
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


class OSPFNetwork:
    def __init__(self, topology):
        self.routers = {r: OSPFRouter(r) for r in topology}
        for r, neighbors in topology.items():
            self.routers[r].neighbors = neighbors

    def simulate_lsa_exchange(self):
        
        for r in self.routers.values():
            for other in self.routers.values():
                other.receive_lsa(r.generate_lsa())

    def compute_routes(self):
       
        for r in self.routers.values():
            r.run_dijkstra()

    def display_all(self):
        for r in sorted(self.routers):
            self.routers[r].display_table()


if __name__ == "__main__":
  
    topology = {
        "A": {"B": 2, "C": 5},
        "B": {"A": 2, "C": 1, "D": 2},
        "C": {"A": 5, "B": 1, "D": 3, "E": 1},
        "D": {"B": 2, "C": 3, "E": 2},
        "E": {"C": 1, "D": 2}
    }

    net = OSPFNetwork(topology)
    net.simulate_lsa_exchange()
    net.compute_routes()
    net.display_all()
