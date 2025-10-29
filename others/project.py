import random

# Daftar kota
cities = ["Jakarta", "Bandung", "Yogyakarta", "Surabaya", "Bali"]

# Tetapkan titik awal (Surabaya)
START_CITY = "Surabaya"
START_INDEX = cities.index(START_CITY)

# Matriks jarak tetap (base awal)
distance_matrix = [
    [0,   150, 500, 780, 1200],   # Jakarta
    [150,   0, 350, 700, 1150],   # Bandung
    [500, 350,   0, 330, 800],    # Yogyakarta
    [780, 700, 330,   0, 400],    # Surabaya
    [1200,1150,800, 400,   0]     # Bali
]

# Mode perubahan jarak
# "random"     → full random tiap generasi
# "fluctuate"  → fluktuasi kecil tiap generasi
DISTANCE_MODE = "fluctuate"

def generate_distance_matrix():
    """Full random distance matrix"""
    n = len(cities)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dist = random.randint(100, 1200)
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

def fluctuate_distance(matrix, max_change=50):
    """Fluktuasi kecil berdasarkan jarak sebelumnya"""
    n = len(matrix)
    new_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            base = matrix[i][j]
            change = random.randint(-max_change, max_change)
            new_val = max(50, base + change)  # minimal 50 km
            new_matrix[i][j] = new_val
            new_matrix[j][i] = new_val
    return new_matrix

# Parameter GA
POP_SIZE = 10
GENERATIONS = 101
MUTATION_RATE = 0.1

# GA
def route_distance(route):
    dist = 0
    for i in range(len(route) - 1):
        dist += distance_matrix[route[i]][route[i+1]]
    dist += distance_matrix[route[-1]][route[0]]
    return dist

def init_population():
    base = list(range(len(cities)))
    base.remove(START_INDEX)
    population = []
    for _ in range(POP_SIZE):
        route = base[:]
        random.shuffle(route)
        route.insert(0, START_INDEX)
        population.append(route)
    return population

def tournament_selection(population):
    a, b = random.sample(population, 2)
    return a if route_distance(a) < route_distance(b) else b

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(1, size), 2))
    child = [-1] * size
    child[0] = START_INDEX
    child[start:end+1] = parent1[start:end+1]

    pointer = 1
    for gene in parent2:
        if gene not in child:
            while pointer < size and child[pointer] != -1:
                pointer += 1
            if pointer < size:
                child[pointer] = gene
    return child

def mutate(route, gen=None):
    i, j = random.sample(range(1, len(route)), 2)
    before = " → ".join(cities[k] for k in route)
    route[i], route[j] = route[j], route[i]
    after = " → ".join(cities[k] for k in route)
    print(f"Generasi {gen}:")
    print(f"   Sebelum Mutasi: {before}")
    print(f"   Sesudah Mutasi: {after}\n")

def genetic_algorithm():
    global distance_matrix
    population = init_population()
    best_route = None
    best_distance = float("inf")

    for gen in range(GENERATIONS):
        # update jarak tiap generasi
        if DISTANCE_MODE == "random":
            distance_matrix = generate_distance_matrix()
        elif DISTANCE_MODE == "fluctuate":
            distance_matrix = fluctuate_distance(distance_matrix)

        population.sort(key=route_distance)

        current_best = population[0]
        current_dist = route_distance(current_best)
        if current_dist < best_distance:
            best_distance = current_dist
            best_route = current_best[:]

        new_population = [current_best]

        while len(new_population) < POP_SIZE:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            child = crossover(p1, p2)
            new_population.append(child)

        if random.random() < MUTATION_RATE:
            candidate = random.choice(new_population[1:])
            mutate(candidate, gen)
        else:
            print(f"Generasi {gen}: Tidak ada mutasi\n")

        population = new_population

        if gen % 20 == 0:
            print(f"Generasi {gen}: Jarak terbaik = {best_distance}")

    return best_route, best_distance

def print_route(route):
    path = " → ".join(cities[i] for i in route)
    path += " → " + cities[route[0]]
    return path

# Jalankan program
if __name__ == "__main__":
    print("Matriks Jarak Awal:")
    for row in distance_matrix:
        print(row)

    best_route, best_distance = genetic_algorithm()
    print("\nRute terbaik:")
    print(print_route(best_route))
    print("Total jarak:", best_distance, "km")
