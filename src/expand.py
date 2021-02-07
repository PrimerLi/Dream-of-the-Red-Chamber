import os

def get_node_weight(string):
    a = string.split(":")
    if len(a) == 1:
        return a[0], 1.0
    return a[0], float(a[1])

def expand(hyperedge_file_name, output_file_name):
    assert(os.path.exists(hyperedge_file_name))
    edges = dict()
    reader = open(hyperedge_file_name, "r")
    for (index, string) in enumerate(reader):
        a = string.strip("\n").split(", ")
        for i in range(len(a)):
            for j in range(i+1, len(a)):
                node1, weight1 = get_node_weight(a[i])
                node2, weight2 = get_node_weight(a[j])
                weight = min(weight1, weight2)
                edge = ";".join(sorted([node1, node2]))
                if edge in edges:
                    edges[edge] += weight
                else:
                    edges[edge] = weight
    reader.close()
    writer = open(output_file_name, "w")
    pairs = sorted(edges.iteritems(), key = lambda ele: ele[1], reverse = True)
    for i in range(len(pairs)):
        writer.write(pairs[i][0] + ";" + str(pairs[i][1]) + "\n")
    writer.close()

def main():
    import sys
    if len(sys.argv) != 2:
        print "hyperedge_file_name = sys.argv[1]. "
        return -1

    hyperedge_file_name = sys.argv[1]
    output_file_name = "edges.csv"
    expand(hyperedge_file_name, output_file_name)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
