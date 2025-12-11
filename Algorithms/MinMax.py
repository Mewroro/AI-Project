import random

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

class MinMax:
    def __init__(self, depth, leaf_values):
        self.depth = depth

        self.leaf_values = leaf_values
        self.leaf_count = len(leaf_values)

        self.evaluated_leaves = 0
        self.root_value = None

        self.tree = self.build_random_tree()

    def build_random_tree(self):
        leaves = [Node(value=v) for v in self.leaf_values]
        if self.depth == 0:
            return leaves[0]

        current_level = leaves
        for _ in range(self.depth):
            next_level = []
            i = 0

            while i < len(current_level):
                child_count = random.randint(1, min(4, len(current_level) - i))
                children = current_level[i:i + child_count]

                parent = Node()
                parent.children = children
                next_level.append(parent)

                i += child_count

            if not next_level:
                break

            current_level = next_level

            if len(current_level) == 1:
                break

        if current_level:
            return current_level[0]
        else:
            return Node()

    def minimax(self, node, alpha, beta, maximizing):
        if len(node.children) == 0:
            self.evaluated_leaves += 1
            return node.value

        if maximizing:
            best = float("-inf")
            for child in node.children:
                val = self.minimax(child, alpha, beta, False)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            node.value = best
            return best
        else:
            best = float("inf")
            for child in node.children:
                val = self.minimax(child, alpha, beta, True)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            node.value = best
            return best

    def get_depth_of_value(self, value):
        return self.dfs_depth(self.tree, value, 0)

    def dfs_depth(self, node, value, depth):
        if node is None:
            return -1
        if node.value == value:
            return depth
        for child in node.children:
            result = self.dfs_depth(child, value, depth + 1)
            if result != -1:
                return result
        return -1


    def run_minmax(self):
        self.evaluated_leaves = 0
        self.root_value = self.minimax(self.tree, float("-inf"), float("inf"), True)
        return self.root_value
