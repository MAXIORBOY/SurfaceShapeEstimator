from main import ShapeEstimator

if __name__ == '__main__':
    ShapeEstimator('flights.csv', point_details_file_name='airports.csv', color_definitions_file='color_definitions.csv', optimized_points_file='earth.pickle').draw_plot()
