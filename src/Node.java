import java.util.*;

public class Node {
	private static int nodeCount = 0;
	private int id;
	private Set<Edge> edges;
	private boolean active;

	public Node() {
		id = nodeCount++;
		edges = new HashSet<Edge>();
		active = false;
	}

	public int getID() {
		return id;
	}

	// Add a new edge starting from this node leading to another node "destination"
	public boolean addEdge(Node destination, double weight) {
		Edge proposedEdge = new Edge(this, destination, weight);
		if (!edges.contains(proposedEdge)) {
			edges.add(proposedEdge);
			return true;
		}
		else {
			System.out.println("Edge already in graph");
			return false;
		}
	}

	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("Node " + id);
		if (active) {
			sb.append(" (ACTIVE)\n");
		}
		else {
			sb.append("\n");
		}
		sb.append("Edges: " + "\n");
		for (Edge e : edges) {
			System.out.println("ADDED EDGE" + e);
			sb.append(e.getDestination() + " (" + e.getIP() + "), ");
		}
		sb.delete(sb.length()-2, sb.length());	// Remove the extra comma
		sb.append("\n");

		return sb.toString();
	}
}
