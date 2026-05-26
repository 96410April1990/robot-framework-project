class Node():

    def __init__(self, value):
        self.value = value
        self.adjacent_list = []
        #To check if an element has been visited
        self.visited = False

class Graph():
    
    def BFS(self, node):

        queue = []
        queue.append(node)
        node.visited = True

        traversal = []

        while queue:
            actualNode = queue.pop(0)
            traversal.append(actualNode.value)

            for element in actualNode.adjacent_list:
                if element.visited is False:
                    queue.append(element)
                    element.visited = True
                
        return traversal

node1 = Node("A")
node2 = Node("B")
node3 = Node("C")
node4 = Node("D")
node5 = Node("E")
node6 = Node("F")
node7 = Node("G")

node1.adjacent_list.append(node2)
node1.adjacent_list.append(node3)
node1.adjacent_list.append(node4)

node2.adjacent_list.append(node5)
node2.adjacent_list.append(node6)

node4.adjacent_list.append(node7)

graph = Graph()

print(graph.BFS(node1))

