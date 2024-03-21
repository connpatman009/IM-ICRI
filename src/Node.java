import java.util.*;

public class Node {
	private static int nodeCount = 0;
	private int id;
	private Set<Edge> edges;

	public Node() {
		id = nodeCount++;
		edges = new HashSet<Edge>();
	}
}
