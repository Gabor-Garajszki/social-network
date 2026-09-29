import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class AgentBasedNetwork:

    def __init__(
        self,
        nodes=500,
        n_traits=8,
        trait_levels=2,
        alpha=2.0,
        decay=0.995,
        threshold=1e-4,
        random_meet_p=0.1,
        strengthen_amount=1.5,
    ):
        self.nodes = nodes
        self.n_traits = n_traits
        self.trait_levels = trait_levels
        self.alpha = alpha
        self.decay = decay
        self.threshold = threshold
        self.random_meet_p = random_meet_p
        self.amount = strengthen_amount
        self.st_c_p = (1.0 / self.nodes) * 3.0

        self.traits = np.random.randint(
            0, self.trait_levels, size=(self.nodes, self.n_traits)
        )
        self.links = [[] for _ in range(self.nodes)]
        self.weights = [[] for _ in range(self.nodes)]

    def compute_similarity(self, i, j):
        return np.mean(self.traits[i] == self.traits[j])

    def create_initial_links(self):
        for i in range(self.nodes):
            for j in range(i + 1, self.nodes):
                sim = self.compute_similarity(i, j)
                p = self.st_c_p * (1.0 + self.alpha * sim)
                if random.random() < p:
                    w = random.uniform(0.5, 1.5)
                    self.links[i].append(j)
                    self.weights[i].append(w)
                    self.links[j].append(i)
                    self.weights[j].append(w)

    def add_or_strengthen(self, a, b):
        if b in self.links[a]:
            idx_a = self.links[a].index(b)
            self.weights[a][idx_a] += self.amount
            idx_b = self.links[b].index(a)
            self.weights[b][idx_b] += self.amount
        else:
            sim = self.compute_similarity(a, b)
            p = self.st_c_p * (1.0 + self.alpha * sim)
            if random.random() < p:
                w = random.uniform(0.5, 1.5)
                self.links[a].append(b)
                self.weights[a].append(w)
                self.links[j := b].append(a)
                self.weights[j].append(w)

    def step_random_meeting(self):
        if random.random() < self.random_meet_p:
            i = random.randint(0, self.nodes - 1)
            sims = np.array(
                [self.compute_similarity(i, j) for j in range(self.nodes)],
                dtype=float,
            )
            sims[i] = 0.0
            weights = sims**self.alpha
            total_w = weights.sum()
            if total_w > 0:
                j = np.random.choice(range(self.nodes), p=weights / total_w)
                self.add_or_strengthen(i, j)

    def step_triadic_closure(self):
        i = random.randint(0, self.nodes - 1)
        if not self.links[i]:
            return

        w_i = np.array(self.weights[i], dtype=float)
        sim_i = np.array(
            [self.compute_similarity(i, x) for x in self.links[i]], dtype=float
        )
        weights_i = w_i * (1.0 + self.alpha * sim_i)
        if weights_i.sum() == 0:
            return

        j = np.random.choice(self.links[i], p=weights_i / weights_i.sum())
        if not self.links[j]:
            return

        js = self.links[j]
        w_j = np.array(
            [self.weights[j][self.links[j].index(x)] for x in js], dtype=float
        )
        sim_j = np.array(
            [self.compute_similarity(j, x) for x in js], dtype=float
        )
        weights_j = w_j * (1.0 + self.alpha * sim_j)
        if weights_j.sum() == 0:
            return

        k = np.random.choice(js, p=weights_j / weights_j.sum())
        if k == i:
            return

        self.add_or_strengthen(i, j)
        self.add_or_strengthen(j, k)
        self.add_or_strengthen(i, k)

    def step_decay_and_pruning(self):
        edges_to_prune = set()
        for a in range(self.nodes):
            for idx, b in enumerate(self.links[a]):
                new_w = self.weights[a][idx] * self.decay
                if new_w < self.threshold:
                    edges_to_prune.add(tuple(sorted((a, b))))
                self.weights[a][idx] = new_w

        for u, v in edges_to_prune:
            if v in self.links[u]:
                idx = self.links[u].index(v)
                del self.links[u][idx]
                del self.weights[u][idx]
            if u in self.links[v]:
                idx = self.links[v].index(u)
                del self.links[v][idx]
                del self.weights[v][idx]

    def simulate(self, num_events=100):
        self.create_initial_links()
        for _ in range(num_events):
            self.step_random_meeting()
            self.step_triadic_closure()
            self.step_decay_and_pruning()

    def build_networkx_graph(self):
        G = nx.Graph()
        for i in range(self.nodes):
            for idx, j in enumerate(self.links[i]):
                if i < j:
                    G.add_edge(i, j, weight=self.weights[i][idx])
        return G

    def plot_ego_network(self, radius=2):
        G = self.build_networkx_graph()
        if G.number_of_edges() == 0:
            print("Graph is empty.")
            return

        degrees = dict(G.degree(weight="weight"))
        focus_node = max(degrees, key=degrees.get)

        subG = nx.ego_graph(G, focus_node, radius=radius)
        pos = nx.spring_layout(
            subG,
            pos={focus_node: (0, 0)},
            fixed=[focus_node],
            k=0.6,
            iterations=100,
            seed=42,
        )

        strengths = [subG.degree(n, weight="weight") for n in subG.nodes()]
        min_s, max_s = min(strengths), max(strengths)
        if max_s == min_s:
            max_s += 1
        node_sizes = [200 + (s - min_s) / (max_s - min_s) * 800 for s in strengths]

        weights = [subG[u][v]["weight"] for u, v in subG.edges()]
        if weights:
            w_min, w_max = min(weights), max(weights)
            edge_widths = [
                0.5 + (w - w_min) / (w_max - w_min) * 2.5
                if w_max > w_min
                else 1.0
                for w in weights
            ]
        else:
            edge_widths = []

        plt.figure(figsize=(10, 10))
        nx.draw_networkx_edges(
            subG, pos, width=edge_widths, alpha=0.25, edge_color="#444444"
        )

        others = [n for n in subG.nodes() if n != focus_node]
        other_sizes = [node_sizes[list(subG.nodes()).index(n)] for n in others]
        other_colors = [strengths[list(subG.nodes()).index(n)] for n in others]

        nx.draw_networkx_nodes(
            subG,
            pos,
            nodelist=others,
            node_size=other_sizes,
            node_color=other_colors,
            cmap=plt.cm.viridis,
            alpha=0.85,
            edgecolors="white",
        )

        #Highlight focal agent
        nx.draw_networkx_nodes(
            subG,
            pos,
            nodelist=[focus_node],
            node_size=node_sizes[list(subG.nodes()).index(focus_node)] * 1.3,
            node_color="#FF4500",
            edgecolors="black",
            linewidths=2,
        )

        #Label direct neighbors
        labels = {focus_node: str(focus_node)}
        for n in G.neighbors(focus_node):
            if n in subG.nodes():
                labels[n] = str(n)
        nx.draw_networkx_labels(
            subG, pos, labels=labels, font_size=8, font_weight="bold"
        )

        plt.title(
            f"Ego Network of Agent {focus_node} (Weighted Degree: {degrees[focus_node]:.2f})",
            fontsize=13,
        )
        plt.axis("off")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sim = AgentBasedNetwork(nodes=500, n_traits=8)
    sim.simulate(num_events=100)
    sim.plot_ego_network(radius=2)