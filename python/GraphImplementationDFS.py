class Node():

    def __init__(self, value):
        self.value = value
        self.adjacent_list = []
        #To check if an element has been visited
        self.visited = False

class Graph():
    
    def DFS(self, node, traversal):
        node.visited = True
        traversal.append(node.value)

        for element in node.adjacent_list:
            if element.visited is False:
                self.DFS(element, traversal)

        return traversal

    

node1 = Node("A")
node2 = Node("B")
node3 = Node("C")
node4 = Node("D")
node5 = Node("E")
node6 = Node("F")
node7 = Node("G")
node8 = Node("H")

node1.adjacent_list.append(node2)
node1.adjacent_list.append(node3)
node1.adjacent_list.append(node4)
node2.adjacent_list.append(node5)
node2.adjacent_list.append(node6)
node4.adjacent_list.append(node7)
node6.adjacent_list.append(node8)

graph = Graph()

print(graph.DFS(node1, []))

