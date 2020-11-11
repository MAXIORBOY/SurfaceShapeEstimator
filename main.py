import pandas as pd
import numpy as np
import random
import plotly.express as px
import pickle


class ShapeEstimator:
    def __init__(self, file_name, duplicate_data=False, point_details_file_name=None, color_definitions_file=None, optimized_points_file=None):
        self.data = self.load_data(file_name)
        self.duplicate_data = duplicate_data
        if self.duplicate_data:
            self.data = self.data_duplicator()

        self.point_details_data = None
        self.color_dictionary = {}
        self.color_definition_column = None
        if point_details_file_name is not None:
            self.point_details_data = self.load_data(point_details_file_name)
            if color_definitions_file is not None:
                self.color_definitions_data = self.load_data(color_definitions_file)
                self.color_definition_column = self.color_definitions_data.columns[0]
                self.color_dictionary = self.create_color_dictionary()

        if optimized_points_file is not None:
            self.load_data_from_optimization_file(optimized_points_file)

        self.unique_points = self.get_all_unique_points_codes()
        self.connections_count = self.points_connections_counter()
        self.best_point_hub_name = self.connections_count.head(1)['point_name'].item()

        if optimized_points_file is None:
            self.points_dictionary = self.create_points_dictionary()
            self.optimize()

        self.values, self.labels = self.split_points_dictionary()
        self.normalize_values()
        self.data_frame = self.create_dataframe_from_points_dictionary()
        self.calculate_average_points_distance_from_the_center()

    def load_data_from_optimization_file(self, optimized_points_file):
        pickle_in = open(optimized_points_file, 'rb')
        self.points_dictionary, cumulative_errors, max_errors, self.duplicate_data = pickle.load(pickle_in)
        if self.duplicate_data:
            self.data = self.data_duplicator()
        self.show_optimization_stats(cumulative_errors, max_errors)

    def data_duplicator(self):
        return self.data.append(self.data, ignore_index=True)

    @staticmethod
    def load_data(file_name):
        return pd.read_csv(file_name, sep=',')

    def get_all_unique_points_codes(self):
        return pd.unique(np.array(self.data[['departure_point', 'arrival_point']]).flatten())

    def create_points_dictionary(self):
        points_dictionary = {}
        for point_name in self.unique_points:
            points_dictionary[point_name] = [(random.random() - 0.5) * 2, (random.random() - 0.5) * 2, (random.random() - 0.5) * 2]

        return points_dictionary

    def create_color_dictionary(self):
        def get_values_from_columns(index):
            return [self.color_definitions_data.iloc[i, index] for i in range(len(self.color_definitions_data.iloc[:, index]))]

        keys = get_values_from_columns(0)
        values = get_values_from_columns(1)

        return dict(zip(keys, values))

    def calculate_errors(self):
        cumulative_error = 0
        max_error = 0
        for index, row in self.data.iterrows():
            error = abs(self.calculate_euclidean_distance_between_two_points(self.points_dictionary[row['departure_point']], self.points_dictionary[row['arrival_point']]) - row['measurement_value'])
            cumulative_error += error
            if max_error < error:
                max_error = error

        return cumulative_error, max_error

    def points_connections_counter(self):
        connections_dictionary = dict(zip(self.unique_points, [0] * len(self.unique_points)))
        for index, row in self.data.iterrows():
            points = [row['departure_point'], row['arrival_point']]
            for point in points:
                connections_dictionary[point] += 1

        connections_count = pd.DataFrame(columns=['point_name', 'count'])
        for point_name in connections_dictionary.keys():
            row = pd.DataFrame({'point_name': [point_name], 'count': [connections_dictionary[point_name]]})
            connections_count = connections_count.append(row, ignore_index=True)

        return connections_count.sort_values('count', ascending=False)

    def get_point_connections_count(self, point_name):
        return self.connections_count.loc[self.connections_count['point_name'] == point_name]['count'].item()

    def optimize(self, mod=0.5, iterations=250, tol=0.001, optimized_points_file_name='optimized_points.pickle'):
        cumulative_errors, max_errors = [], []
        cumulative_error, max_error = self.calculate_errors()
        cumulative_errors.append(cumulative_error)
        max_errors.append(max_error)

        for i in range(iterations):
            data = self.data.sample(frac=1)
            previous_points_dictionary = dict(self.points_dictionary.copy())
            for index, row in data.iterrows():
                distance = self.calculate_euclidean_distance_between_two_points(self.points_dictionary[row['departure_point']], self.points_dictionary[row['arrival_point']])
                vector = self.calculate_vector_between_two_points(self.points_dictionary[row['departure_point']], self.points_dictionary[row['arrival_point']])
                if row['departure_point'] != self.best_point_hub_name and row['arrival_point'] != self.best_point_hub_name:
                    point_to_move = random.choice([0, 1])
                elif row['departure_point'] == self.best_point_hub_name:
                    point_to_move = 1
                else:
                    point_to_move = 0

                if distance > row['measurement_value']:
                    if point_to_move == 0:
                        for j in range(3):
                            self.points_dictionary[row['departure_point']][j] += mod * vector[j]
                    else:
                        for j in range(3):
                            self.points_dictionary[row['arrival_point']][j] -= mod * vector[j]

                elif distance < row['measurement_value']:
                    if point_to_move == 0:
                        for j in range(3):
                            self.points_dictionary[row['departure_point']][j] -= mod * vector[j]
                    else:
                        for j in range(3):
                            self.points_dictionary[row['arrival_point']][j] += mod * vector[j]

            cumulative_error, max_error = self.calculate_errors()
            if cumulative_error > cumulative_errors[-1]:
                self.points_dictionary = previous_points_dictionary
                mod /= 1.05
                if mod < tol:
                    break
            else:
                cumulative_errors.append(cumulative_error)
                max_errors.append(max_error)

        with open(optimized_points_file_name, 'wb') as f:
            pickle.dump((self.points_dictionary, cumulative_errors, max_errors, self.duplicate_data), f)

        self.show_optimization_stats(cumulative_errors, max_errors)

    def show_optimization_stats(self, cumulative_errors, max_errors):
        print(f'Cumulative error: {cumulative_errors[-1]}')
        print(f'Average error: {cumulative_errors[-1] / len(self.data)}')
        print(f'Max error: {max_errors[-1]}')
        print(f'Data duplicated: {self.duplicate_data}')

    def split_points_dictionary(self):
        values, labels = [], []
        for point_name in self.points_dictionary:
            values.append(self.points_dictionary[point_name])
            labels.append(point_name)

        return np.array(values), labels

    def create_dataframe_from_points_dictionary(self):
        data = pd.DataFrame(columns=['point', 'x', 'y', 'z'])
        for i in range(len(self.labels)):
            point_coords = self.values[i]
            row = pd.DataFrame({'point': [self.labels[i]],
                                'x': [point_coords[0]],
                                'y': [point_coords[1]],
                                'z': [point_coords[2]]})
            data = data.append(row, ignore_index=True)

        return data

    @staticmethod
    def calculate_euclidean_distance_between_two_points(point1, point2):
        value = 0
        for i in range(len(point1)):
            value += (point1[i] - point2[i]) ** 2
        return value ** (1 / 2)

    @staticmethod
    def calculate_vector_between_two_points(point1, point2):
        vector = []
        for i in range(len(point1)):
            vector.append(point2[i] - point1[i])

        return vector

    def normalize_values(self):  # <-1; 1>
        for i in range(3):
            a = min(self.values[:, i])
            b = max(self.values[:, i])
            for j in range(len(self.values)):
                self.values[j, i] = ((2 * (self.values[j, i] - a)) / (b - a)) - 1

    def calculate_average_points_distance_from_the_center(self):
        sum_distances = 0
        for point in self.values:
            sum_distances += sum([point[i] ** 2 for i in range(len(point))])
        print(f'Average points distance from the center: {sum_distances / len(self.values)}')

    def draw_plot(self):
        def merge_data():
            if self.point_details_data is not None:
                data = self.data_frame.join(self.point_details_data.set_index('point'), on='point')
            else:
                data = self.data_frame

            return data

        def get_basic_hover_data_dict():
            return {'x': False, 'y': False, 'z': False, 'point': True}

        def extend_hover_dict(basic_dict):
            for column in self.point_details_data.columns:
                if column != 'point':
                    basic_dict[column] = True

            return basic_dict

        plot_data = merge_data()
        hover_data_dict = get_basic_hover_data_dict()

        if self.point_details_data is not None:
            fig = px.scatter_3d(plot_data, x='x', y='y', z='z', color=self.color_definition_column, hover_data=extend_hover_dict(hover_data_dict), color_discrete_map=self.color_dictionary)
        else:
            fig = px.scatter_3d(plot_data, x='x', y='y', z='z', color=self.color_definition_column, hover_data=hover_data_dict, color_discrete_map=self.color_dictionary)
        fig.update_layout(
            scene=dict(
                xaxis={'showgrid': False, 'zeroline': False, 'showline': False, 'showticklabels': False, 'backgroundcolor': 'rgba(255, 255, 255, 0)', 'visible': False},
                yaxis={'showgrid': False, 'zeroline': False, 'showline': False, 'showticklabels': False, 'backgroundcolor': 'rgba(255, 255, 255, 0)', 'visible': False},
                zaxis={'showgrid': False, 'zeroline': False, 'showline': False, 'showticklabels': False, 'backgroundcolor': 'rgba(255, 255, 255, 0)', 'visible': False}
            )
        )
        fig.show()
