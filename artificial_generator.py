import random
import pandas as pd
import numpy as np


class ArtificialGenerator:
    def __init__(self, shape_name, points=500, part_of_all_connections=0.05, data_noise_parameter=0.0):
        self.shape_name = shape_name
        self.points = points
        self.data_noise_parameter = data_noise_parameter
        self.points_dictionary = self.generate_shape_points()
        self.connections = self.calculate_number_of_connections(part_of_all_connections)
        self.connections_matrix = self.create_connections_matrix()

    def calculate_number_of_connections(self, part_of_all_connections):
        return int(part_of_all_connections * (self.points * (self.points - 1) / 2))

    def create_connections_matrix(self):
        return np.array([[i != j for j in range(self.points)] for i in range(self.points)])

    @staticmethod
    def generate_point_coord_from_the_given_range(a, b):
        return random.random() * (b - a) + a

    @staticmethod
    def calculate_euclidean_distance_between_two_points(point1, point2):
        value = 0
        for i in range(len(point1)):
            value += (point1[i] - point2[i]) ** 2
        return value ** (1 / 2)

    def generate_mid_point(self, a=-10, b=10):
        return [self.generate_point_coord_from_the_given_range(a, b) for _ in range(3)]

    def generate_shape_points(self):
        points_dictionary = {}
        a = self.generate_point_coord_from_the_given_range(1, 10)
        if self.shape_name == 'cube':
            mid_point = self.generate_mid_point()
            for i in range(self.points):
                face = random.randint(1, 6)
                if face != 2 and face != 3:
                    x = self.generate_point_coord_from_the_given_range(mid_point[0] - 0.5 * a, mid_point[0] + 0.5 * a)
                elif face == 2:
                    x = mid_point[0] - 0.5 * a
                else:
                    x = mid_point[0] + 0.5 * a

                if face != 1 and face != 6:
                    y = self.generate_point_coord_from_the_given_range(mid_point[1] - 0.5 * a, mid_point[1] + 0.5 * a)
                elif face == 1:
                    y = mid_point[1] - 0.5 * a
                else:
                    y = mid_point[1] + 0.5 * a

                if face != 4 and face != 5:
                    z = self.generate_point_coord_from_the_given_range(mid_point[2] - 0.5 * a, mid_point[2] + 0.5 * a)
                elif face == 4:
                    z = mid_point[2] - 0.5 * a
                else:
                    z = mid_point[2] + 0.5 * a

                points_dictionary[self.create_point_name_from_index(i)] = [x, y, z]

        elif self.shape_name == 'sphere':
            for i in range(self.points):
                x = self.generate_point_coord_from_the_given_range(-a, a)
                y = self.generate_point_coord_from_the_given_range(-((a ** 2 - x ** 2) ** (1 / 2)), (a ** 2 - x ** 2) ** (1 / 2))
                z = random.choice([(a ** 2 - x ** 2 - y ** 2) ** (1 / 2), -((a ** 2 - x ** 2 - y ** 2) ** (1 / 2))])

                points_dictionary[self.create_point_name_from_index(i)] = [x, y, z]

        elif self.shape_name == 'disc':
            z = self.generate_point_coord_from_the_given_range(-10, 10)
            for i in range(self.points):
                x = self.generate_point_coord_from_the_given_range(-a, a)
                y = self.generate_point_coord_from_the_given_range(-((a ** 2 - x ** 2) ** (1 / 2)), (a ** 2 - x ** 2) ** (1 / 2))

                points_dictionary[self.create_point_name_from_index(i)] = [x, y, z]

        elif self.shape_name == 'cylinder':
            h = self.generate_point_coord_from_the_given_range(1, 10)
            for i in range(self.points):
                x = self.generate_point_coord_from_the_given_range(-a, a)
                y = random.choice([(a ** 2 - x ** 2) ** (1 / 2), -((a ** 2 - x ** 2) ** (1 / 2))])
                z = self.generate_point_coord_from_the_given_range(-h / 2, h / 2)

                points_dictionary[self.create_point_name_from_index(i)] = [x, y, z]

        elif self.shape_name == 'line':
            b = self.generate_point_coord_from_the_given_range(1, 10)
            z = self.generate_point_coord_from_the_given_range(-10, 10)
            for i in range(self.points):
                x = self.generate_point_coord_from_the_given_range(-a, a)
                y = a * x + b

                points_dictionary[self.create_point_name_from_index(i)] = [x, y, z]

        return points_dictionary

    @staticmethod
    def create_point_name_from_index(index):
        return f'P{index + 1}'

    def choose_two_points_to_make_connection(self, override_point1_index=None):
        available_points = [i for i in range(len(self.connections_matrix)) if any(self.connections_matrix[i])]
        if override_point1_index is None:
            point1 = random.choice(available_points)
        else:
            point1 = available_points[override_point1_index]
        point2 = random.choice([i for i in range(len(self.connections_matrix[point1])) if self.connections_matrix[point1, i]])
        self.register_connection(point1, point2)

        return point1, point2

    def register_connection(self, point1, point2):
        self.connections_matrix[point1, point2] = False
        self.connections_matrix[point2, point1] = False

    def data_noise(self):
        return 1 - self.generate_point_coord_from_the_given_range(-self.data_noise_parameter, self.data_noise_parameter)

    def generate_connections(self):
        def create_new_row(p1, p2):
            return pd.DataFrame({'departure_point': [self.create_point_name_from_index(p1)],
                                 'arrival_point': [self.create_point_name_from_index(p2)],
                                 'measurement_value': [self.data_noise() * self.calculate_euclidean_distance_between_two_points(self.points_dictionary[self.create_point_name_from_index(p1)], self.points_dictionary[self.create_point_name_from_index(p2)])]})

        data = pd.DataFrame(columns=['departure_point', 'arrival_point', 'measurement_value'])

        for i in range(self.points):  # make sure that every point has at least one connection
            point1, point2 = self.choose_two_points_to_make_connection(override_point1_index=i)
            row = create_new_row(point1, point2)
            data = data.append(row, ignore_index=True)

        for i in range(self.connections - self.points):
            point1, point2 = self.choose_two_points_to_make_connection()
            row = create_new_row(point1, point2)
            data = data.append(row, ignore_index=True)

        data.to_csv('artificial_connections.csv', index=False)
