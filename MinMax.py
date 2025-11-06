import random
from collections import deque

# === Clasa Nodului din arbore ===
class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# === Construiește arbore binar complet dintr-o listă de frunze ===
def build_tree(leaves):
    nodes = [Node(value=v) for v in leaves]
    while len(nodes) > 1:
        new_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1]
            new_level.append(Node(None, left, right))
        nodes = new_level
    return nodes[0]  # rădăcina

# === Afișare arbore pe nivele ===
def print_tree(root, title="Structura arborelui"):
    if not root:
        print("(Arbore gol)")
        return

    queue = deque([(root, 0)])
    current_level = 0
    level_nodes = []

    print(f"\n{title}:")
    while queue:
        node, level = queue.popleft()

        if level != current_level:
            print(f"Nivel {current_level}: {level_nodes}")
            level_nodes = []
            current_level = level

        level_nodes.append(node.value if node.value is not None else "None")

        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))

    print(f"Nivel {current_level}: {level_nodes}")

def get_final_tree_values(root):
    if not root:
        return

    queue = deque([(root, 0)])
    current_level = 0
    level_nodes = []

    while queue:
        node, level = queue.popleft()

        if level != current_level:
            level_nodes = []
            current_level = level

        level_nodes.append(node.value if node.value is not None else "None")

        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))

    return level_nodes

# === Funcția Minimax cu Alpha-Beta și completarea valorilor pentru noduri tăiate ===
def minimax(node, depth, alpha, beta, maximizing_player, counter):
    # Caz frunză
    if node.left is None and node.right is None:
        counter[0] += 1
        return node.value

    if maximizing_player:
        max_eval = float('-inf')
        # stânga
        val_left = minimax(node.left, depth+1, alpha, beta, False, counter)
        max_eval = max(max_eval, val_left)
        alpha = max(alpha, max_eval)

        # dreapta
        if node.right:
            if beta > alpha:
                val_right = minimax(node.right, depth+1, alpha, beta, False, counter)
                max_eval = max(max_eval, val_right)
            else:
                # Ramura tăiată → setăm valoarea copilului drept = valoarea curentă a nodului
                node.right.value = max_eval

        node.value = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        # stânga
        val_left = minimax(node.left, depth+1, alpha, beta, True, counter)
        min_eval = min(min_eval, val_left)
        beta = min(beta, min_eval)

        # dreapta
        if node.right:
            if beta > alpha:
                val_right = minimax(node.right, depth+1, alpha, beta, True, counter)
                min_eval = min(min_eval, val_right)
            else:
                # Ramura tăiată → setăm valoarea copilului drept = valoarea curentă a nodului
                node.right.value = min_eval

        node.value = min_eval
        return min_eval

# === Funcție pentru afișarea arborelui final ===
def print_final_tree(root):
    print_tree(root, title="Arborele final după aplicarea strategiei Minimax")

