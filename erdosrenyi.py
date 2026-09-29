import random
import statistics
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx

#PARAMETERS
N_NODES = 400
P_EDGE = 1.5 / N_NODES
N_RUNS = 400


def analyze_single_graph(n_nodes, p_edge):
    """Generates an Erdos-Renyi graph and extracts basic structural metrics."""
    G = nx.erdos_renyi_graph(n_nodes, p_edge)
    degrees = [deg for _, deg in G.degree()]
    components = list(nx.connected_components(G))
    comp_sizes = [len(c) for c in components]

    #Map each component to a unique color index
    component_color_map = {}
    for idx, comp in enumerate(components):
        for node in comp:
            component_color_map[node] = idx

    return G, degrees, components, comp_sizes, component_color_map


def run_monte_carlo_experiments(n_nodes, p_edge, n_runs):
    """Runs multiple graph generations to obtain empirical size distributions."""
    aggregated_sizes = []
    component_counts = []

    for _ in range(n_runs):
        G_iter = nx.erdos_renyi_graph(n_nodes, p_edge)
        comps = list(nx.connected_components(G_iter))
        aggregated_sizes.extend([len(c) for c in comps])
        component_counts.append(len(comps))

    return aggregated_sizes, component_counts


def main():
    G, degrees, components, comp_sizes, comp_colors = analyze_single_graph(
        N_NODES, P_EDGE
    )
    all_sizes, all_counts = run_monte_carlo_experiments(
        N_NODES, P_EDGE, N_RUNS
    )

    pos = nx.spring_layout(G, seed=42)
    deg_labels = {node: str(deg) for node, deg in G.degree()}
    deg_counts = Counter(degrees)
    comp_size_counts = Counter(comp_sizes)
    mc_size_counts = Counter(all_sizes)

    mean_comp_size = sum(all_sizes) / len(all_sizes)
    median_comp_size = statistics.median(all_sizes)
    try:
        mode_comp_size = statistics.mode(all_sizes)
    except statistics.StatisticsError:
        mode_comp_size = "No unique mode"

    #PLOTTING DASHBOARD 
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    #1. Graph colored by connected component
    node_colors_comp = [comp_colors[node] for node in G.nodes()]
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color=node_colors_comp,
        cmap=plt.cm.tab20,
        node_size=250,
        edge_color="gray",
        ax=axes[0, 0],
    )
    nx.draw_networkx_labels(
        G, pos, labels=deg_labels, font_size=7, font_color="black", ax=axes[0, 0]
    )
    axes[0, 0].set_title(f"Single Realization ({len(components)} Components)")

    #2. Degree distribution
    axes[0, 1].bar(
        deg_counts.keys(),
        deg_counts.values(),
        color="skyblue",
        edgecolor="black",
    )
    axes[0, 1].set_xlabel("Degree (k)")
    axes[0, 1].set_ylabel("Node Frequency")
    axes[0, 1].set_title("Degree Distribution")
    axes[0, 1].set_xticks(range(max(deg_counts.keys()) + 1))

    #3. Component size distribution (Single Run)
    axes[0, 2].bar(
        comp_size_counts.keys(),
        comp_size_counts.values(),
        color="orange",
        edgecolor="black",
    )
    axes[0, 2].set_xlabel("Component Size")
    axes[0, 2].set_ylabel("Count")
    axes[0, 2].set_title("Component Size Distribution (1 Run)")

    #4. Aggregated Component Size Distribution (Monte Carlo)
    axes[1, 0].bar(
        mc_size_counts.keys(),
        mc_size_counts.values(),
        color="lightgreen",
        edgecolor="black",
    )
    axes[1, 0].axvline(
        mean_comp_size,
        color="red",
        linestyle="--",
        label=f"Mean = {mean_comp_size:.2f}",
    )
    axes[1, 0].set_xlabel("Component Size")
    axes[1, 0].set_ylabel("Frequency")
    axes[1, 0].set_title(f"Component Sizes ({N_RUNS} Realizations)")
    axes[1, 0].legend()

    #5. Graph colored by node degree
    node_colors_deg = [G.degree(node) for node in G.nodes()]
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color=node_colors_deg,
        cmap=plt.cm.plasma,
        node_size=250,
        edge_color="gray",
        ax=axes[1, 1],
    )
    nx.draw_networkx_labels(
        G, pos, labels=deg_labels, font_size=7, font_color="white", ax=axes[1, 1]
    )
    axes[1, 1].set_title("Graph (Node Degree Colormap)")

    #6. Statistical Summary Box
    axes[1, 2].axis("off")
    summary_text = (
        f"Network Parameters:\n"
        f"  - Nodes (N): {N_NODES}\n"
        f"  - Edge Probability (p): {P_EDGE:.4f} (1/N)\n\n"
        f"Single Run Metrics:\n"
        f"  - Giant Component Size: {max(comp_sizes)}\n"
        f"  - Average Degree: {sum(degrees) / len(degrees):.2f}\n"
        f"  - Maximum Degree: {max(degrees)}\n\n"
        f"Monte Carlo ({N_RUNS} Runs):\n"
        f"  - Mean Component Count: {sum(all_counts)/len(all_counts):.2f}\n"
        f"  - Median Component Size: {median_comp_size}\n"
        f"  - Mode Component Size: {mode_comp_size}"
    )
    axes[1, 2].text(
        0.05,
        0.95,
        summary_text,
        fontsize=11,
        va="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="whitesmoke", alpha=0.8),
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()