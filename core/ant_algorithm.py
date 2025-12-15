import numpy as np
from config import ACO_PARAMS

class ACOptimizer:
    def __init__(self, dist_matrix):
        self.dist_matrix = dist_matrix
        self.N = dist_matrix.shape[0]
        self.P = ACO_PARAMS
        self.pheromone_matrix = np.ones((self.N, self.N)) * 0.1
        self.visibility_matrix = 1.0 / (dist_matrix + np.finfo(float).eps)
        np.fill_diagonal(self.visibility_matrix, 0)

        self.best_route = None
        self.best_distance = np.inf
        self.convergence_history = []

    def _calculate_route_distance(self, route):
        distance = 0.0
        for i in range(self.N):
            city_a = route[i]
            city_b = route[(i + 1) % self.N]
            distance += self.dist_matrix[city_a, city_b]
        return distance

    def _select_next_city(self, current_city, unvisited_cities):
        attractiveness = (self.pheromone_matrix[current_city, unvisited_cities] ** self.P['alpha']) * \
                         (self.visibility_matrix[current_city, unvisited_cities] ** self.P['beta'])

        total_attractiveness = np.sum(attractiveness)

        # Orijinal Olasılıklar
        probabilities = attractiveness / (total_attractiveness + np.finfo(float).eps)

        # >>> HATA ÇÖZÜMÜ: Olasılıkları Manuel Olarak Normalize Etme
        # NumPy'nin kayan nokta hassasiyeti hatasını aşmak için.
        probabilities /= probabilities.sum()
        # <<< HATA ÇÖZÜMÜ BİTİŞ

        next_city_index = np.random.choice(len(unvisited_cities), 1, p=probabilities)[0]
        return unvisited_cities[next_city_index]

    def _construct_ant_route(self):
        start_node = 0
        route = [start_node]
        unvisited = list(range(self.N))
        unvisited.remove(start_node)

        while unvisited:
            current_city = route[-1]
            next_city = self._select_next_city(current_city, np.array(unvisited))
            route.append(next_city)
            unvisited.remove(next_city)

        return route, self._calculate_route_distance(route)

    def _update_pheromones(self, ant_routes):
        self.pheromone_matrix *= (1.0 - self.P['rho'])
        Q = self.P['Q']

        for route, distance in ant_routes:
            pheromone_deposit = Q / distance
            for i in range(self.N):
                city_a = route[i]
                city_b = route[(i + 1) % self.N]
                self.pheromone_matrix[city_a, city_b] += pheromone_deposit
                self.pheromone_matrix[city_b, city_a] += pheromone_deposit

    def run(self):
        for iteration in range(self.P['num_iterations']):
            all_ant_routes = []

            for _ in range(self.P['num_ants']):
                route, distance = self._construct_ant_route()
                all_ant_routes.append((route, distance))

                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_route = route

            self._update_pheromones(all_ant_routes)
            self.convergence_history.append(self.best_distance)

            print(f"İterasyon {iteration+1}: En İyi Mesafe = {self.best_distance:.2f} KM")

        return self.best_route, self.best_distance, self.convergence_history
