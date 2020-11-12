# Surface Shape Estimator is a program which allows to estimate a shape of the surface based solely on a collection of connections between two points on that surface. Data about a single connection store 3 informations: code names of a first and second point and Euclidean distance OR travel time between those points.

## Important: If you use travel time, you have to make sure that the same speed was maintained during all travels and that the connection lines are straight.

## Implementation: To solve this problem the script ```main.py``` was created, which contains a class ```ShapeEstimator```.  
```__init__(self, connections_file_name, duplicate_data=False, point_details_file_name=None, color_definitions_file=None, optimized_points_file=None)```

* ```connections_file_name``` - (str) full name of the file which stores data about connections. The file must be in ```.csv``` format. The file must have exactly 3 columns, named as follows: 
 
departure_point | arrival_point | measurement_value  
----------------|---------------|-------------------

* ```duplicate_data``` - (bool) (...) .Default = False  

* ```point_details_file_name``` - (str) full name of the file which stores additional informations about points. The file must be in ```.csv``` format. The file may have any number of columns, but must have a column ```point``` which is a point codename from the ```connections file```. Default = None  

* ```color_definitions_file``` - (str) full name of the file which describes a method to color the points. The file must be in ```.csv``` format. The file must have exactly 2 columns. The first column name must come from the one of the ```points_details_file``` column names. The second column name must be named as ```color```. In each row, you can choose any ```CSS``` color, declared by it's name or hex. Declaring ```color_definitions_file``` has no use if the ```point_details_file``` is not declared. Default = None  

* ```optimized_points_file``` - (str) full name of the file which . The file must be in ```.pickle``` format. Default = None. (...)  

## Earth example:
In order to estimate a shape of the surface of Earth, at first 634 airports were carefully selected from all around the globe. 
Following this we have to create as many connections as possible from the collected airports. 

* Why airports? 
Because we are going to use time measurements between points. In order to do that our routes have to be as straight as possible and roughly the same speed has to be maintained on all routes. Air flights sufficiently enough fullfill our conditions.

* Why did airports were carefully selected? Couldn't we just use all of them?
There are two reasons. First we have to maintain the conditions.(.....)

* What is an IATA code?
An IATA (International Air Transport Association) code is a 3 letter geocode which designates airports and metropolitan areas (if a city has more than one airport)
For example:
  * 'ATL' is a code of: "Hartsfield–Jackson Atlanta International Airport",
  * 'CGK' is a code of: "Soekarno–Hatta International Airport",
  * 'PAR' is a code of the Paris city.
  * 'LON' is a code of the London city.
