from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

center_products = {
    "C1": ["A", "B", "C"],
    "C2": ["D", "E", "F"],
    "C3": ["G", "H", "I"]
}

costs = {
    ("C1", "L1"): 10,
    ("C2", "L1"): 20,
    ("C3", "L1"): 30,
    ("C1", "C2"): 15,
    ("C1", "C3"): 25,
    ("C2", "C1"): 15,
    ("C2", "C3"): 10,
    ("C3", "C1"): 25,
    ("C3", "C2"): 10,
}

def get_centers_for_order(order):
    needed_centers = set()
    for center, products in center_products.items():
        for item in order:
            if order[item] > 0 and item in products:
                needed_centers.add(center)
    return list(needed_centers)

def calculate_min_cost(order):
    centers = get_centers_for_order(order)
    min_cost = float('inf')
    
    for start in centers:
        for perm in permutations([c for c in centers if c != start]):
            route = [start] + list(perm)
            cost = 0
            visited = set()
            current = start
            for c in route:
                if c != current:
                    cost += costs[(current, c)]
                    current = c
                if c not in visited:
                    cost += costs[(c, "L1")]
                    visited.add(c)
            if cost < min_cost:
                min_cost = cost
    return min_cost

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    order = request.get_json()
    if not order:
        return jsonify({"error": "Invalid input"}), 400
    cost = calculate_min_cost(order)
    return jsonify({"minimum_cost": cost})

if __name__ == '__main__':
    app.run()
