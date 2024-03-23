import java.util.*;

public class Graph {
	private Set<Node> nodes;
	private int numNodes;

	public Graph(int numN, double density) {
		nodes = new HashSet<Node>();
		this.numNodes = numN;

		// Create a random graph with the number of nodes specified
		for (int i = 0; i < numN; i++) {
			Node newNode = new Node();
			nodes.add(newNode);
		}
		
		// Randomly generate edges
		Random rng = new Random();
		/*for (int i = 0; i < numN; i++) {
			for (int j = 0; j < numN; j++) {
				// Do not create edges to itself
				if (i == j) {
					continue;
				}

				// Randomly choose if two edges are connected
				if (rng.nextDouble() < density) {
					Node src = this.getNode(i);
					Node dest = this.getNode(j);
					double influence = rng.nextDouble();

					if (src != null && dest != null) {
						src.addEdge(dest, influence);
					}
				}
			}
		}*/
		Node src = this.getNode(0);
		Node dest = this.getNode(1);
		double influence = rng.nextDouble();

		if (src != null && dest != null) {
			src.addEdge(dest, influence);
		}

		// TODO: Remove this testing loop
		for (Node curr : nodes) {
			System.out.println(curr);
		}
	}

	private Node getNode(int id) {
		for (Node curr : this.nodes) {
			if (curr.getID() == id) {
				return curr;
			}
		}

		return null;
	}
}
