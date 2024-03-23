import java.util.*;

public class Edge {
	private Node source, destination;
	private double influenceProbability;

	public Edge(Node src, Node dest, double ip) {
		this.source = src;
		this.destination = dest;
		this.influenceProbability = ip;
	}

	public Node getSource() {
		return source;
	}

	public Node getDestination() {
		return destination;
	}

	public double getIP() {
		return influenceProbability;
	}

	public boolean equals(Edge e) {
		if (this.getSource().equals(e.getSource()) && this.getDestination().equals(e.getDestination())) {
			return true;
		}
		else {
			return false;
		}
	}

	public String toString() {
		return "" + source.getID() + " " + destination.getID() + " (" + influenceProbability + ")";
	}
}
