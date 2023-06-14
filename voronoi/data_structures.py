
class FortuneEvent:
    def __init__(self, point, event_type, arc=None, circle_event=None) -> None:
        self.point = point
        self.event_type = event_type
        self.arc = arc
        self.circle_event = circle_event
    
    def __lt__(self, other):
        return self.point[0] < other.point[0]
    
    def __repr__(self) -> str:
        return f"Event({self.point}, {self.event_type})"

class PriorityQueue:
    def __init__(self) -> None:
        self.heap = []
    
    def push(self, item):
        self.heap.append(item)
        self._bubble_up(len(self.heap) - 1)
    
    def pop(self):
        if len(self.heap) == 0:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._bubble_down(0)
        return item

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _bubble_up(self, i):
        parent = (i - 1) // 2
        if parent >= 0 and self.heap[parent] > self.heap[i]:
            self._swap(parent, i)
            self._bubble_up(parent)
    
    def _bubble_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != i:
            self._swap(smallest, i)
            self._bubble_down(smallest)
    
    def __len__(self):
        return len(self.heap)
    

class BinarySearchTree:

    def __init__(self) -> None:
        self.root = None
    
    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)
    
    def _insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = Node(key, value)
            else:
                self._insert(node.left, key, value)
        else:
            if node.right is None:
                node.right = Node(key, value)
            else:
                self._insert(node.right, key, value)
    
    def find(self, key):
        return self._find(self.root, key)

    def _find(self, node, key):
        if node is None:
            return None
        if node.key == key:
            return node.value
        if key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)
        
    def delete(self, key):
        self.root = self._delete(self.root, key)
    
    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._find_min(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self._delete(node.right, successor.key)
        return node
    
    def _find_min(self, node):
        if node.left is None:
            return node
        return self._find_min(node.left)
    

class Node:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
        self.left = None
        self.right = None
    
    def __repr__(self) -> str:
        return f"Node({self.key}, {self.value})"