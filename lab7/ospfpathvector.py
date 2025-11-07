
class BGPNode:
    def __init__(self, asn):
        self.asn = asn
        self.neighbors = set()
        self.routes = {asn: [asn]} 

    def send_updates(self):
       
        updates = {}
        for dest, path in self.routes.items():
            for nb in self.neighbors:
                # Path advertisement (prepend self ASN)
                if nb not in updates:
                    updates[nb] = []
                updates[nb].append((dest, [self.asn] + path))
        return updates

    def receive_update(self, src, updates):
       
        changed = False
        for dest, path in updates:
            if self.asn in path:
                # Loop prevention: ignore routes containing self
                continue
            if dest not in self.routes or len(path) + 1 < len(self.routes[dest]):
                self.routes[dest] = [self.asn] + path
                changed = True
        return changed


class BGPNetwork:
    def __init__(self, topology):
        self.nodes = {asn: BGPNode(asn) for asn in topology}
        for asn, nbs in topology.items():
            self.nodes[asn].neighbors = set(nbs)

    def run(self, max_rounds=20):
      
        round_no = 0
        while round_no < max_rounds:
            changed_any = False
            all_updates = []
            # Prepare updates
            for node in self.nodes.values():
                upds = node.send_updates()
                for nb, messages in upds.items():
                    all_updates.append((node.asn, nb, messages))
            # Deliver updates
            for src, dst, msgs in all_updates:
                if dst in self.nodes:
                    changed = self.nodes[dst].receive_update(src, msgs)
                    changed_any = changed_any or changed
            if not changed_any:
                break
            round_no += 1
        print(f"\nBGP converged in {round_no} rounds.\n")

    def display_routes(self):
        for asn in sorted(self.nodes):
            node = self.nodes[asn]
            print(f"AS{asn} Routing Table:")
            print("Destination\tAS_PATH")
            for dest, path in sorted(node.routes.items()):
                print(f"AS{dest}\t\t{' → '.join('AS'+str(p) for p in path)}")
            print("-" * 40)


if __name__ == "__main__":
   
    topology = {
        1: {2, 3},
        2: {1, 3, 4},
        3: {1, 2, 5},
        4: {2, 5},
        5: {3, 4}
    }

    net = BGPNetwork(topology)
    net.run()
    net.display_routes()
