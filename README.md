# Surface Shape Estimator is a program which allows to estimate a shape of the surface based solely on a collection of connections between two points on that surface. Data about a single connection store 3 information: code names of a first and second point and Euclidean distance OR travel time between those points.

> :warning: **If you use a travel time as a measurement**: You have to make sure that the same speed was maintained during all travels and that the connection lines are straight.  
<br>


## Implementation:  
 To solve this problem, the script ```main.py``` was created, which contains a class ```ShapeEstimator```.    
```ShapeEstimator.__init__(self, connections_file_name, duplicate_data=False, point_details_file_name=None, color_definitions_file=None, optimized_points_file=None)```  
<br>
* ```connections_file_name``` - (str) full name of the file which stores data about connections. The file must be in ```.csv``` format. The file must have exactly 3 columns, named as follows: ```departure_point```, ```arrival_point```, ```measurement_value```. The ```flights.csv``` file is a valid example.
 
  ```connections_file``` header:  
  departure_point | arrival_point | measurement_value  
  ----------------|---------------|-------------------
<br>

* ```duplicate_data``` - (bool) duplicate the data from the ```connections_file```. Duplicating the data usually yields better results, especially if you have many points with not many connections and / or you have a low amount of connections overall. Duplicating the data causes a considerable increase of optimization time. Duplication of data shall be discouraged if your collection of connections does not meet the previously mention situations. Default = False  


* ```point_details_file_name``` - (str) full name of the file which stores additional information about points. The file must be in ```.csv``` format. The file may have any number of columns, but must have a column ```point``` which is a point codename from the ```connections file```.  The ```airports.csv``` file is a valid example. Default = None

  ```point_details_file``` header:  
  point | <column_name 1> | ... | <column_name n>
  ------|-----------------|-----|---------------- 
<br>
  
* ```color_definitions_file``` - (str) full name of the file which describes a method to color the points. The file must be in ```.csv``` format. The file must have exactly 2 columns. The first column name must come from the one of the ```points_details_file``` column names. The second column name must be named as ```color```. In each row, you can choose any ```CSS``` color, declared by it's name or hex. Declaring ```color_definitions_file``` has no use if the ```point_details_file``` is not declared. The ```color_definitions.csv``` file is a valid example. Default = None  

  ```color_definitions_file``` header:  
  <column from ```points_detail_file```> | color  
  ---------------------------------------|-------  
<br>

* ```optimized_points_file``` - (str) full name of the file which stores already optimized coordinates (xyz) of each point and some additional information. The file must be in ```.pickle``` format. After each optimization process a new ```.pickle``` file is generated, which saves the results. Passing a ```.pickle``` file as parameter skips the whole optimization process which saves time and allows to load previously calculated results. If a ```.pickle``` file is passed as the parameter, the value of the ```duplicate_data``` parameter is irrelevant, because that value is saved in the file. By default the results will be saved in the ```optimized.pickle``` file. The ```earth.pickle``` file is a valid example. Default = None.


## Optimizer Algorithm:
1. Find a point with the largest number of connections.
2. Create a set of unique points from ```connections_file```.  
3. Place all of the points (from the set) at random on 3-D space. 
4. Calculate errors (cumulative, average, max)
5. i = 0.  
6. Repeat if i < 250:  
&nbsp;7. Shuffle the data from the ```connections_file```.  
&nbsp;8. Make a copy of current points coordinates.  
&nbsp;9. Repeat for each connection in ```connections_file```:   
&nbsp;&nbsp;10. Calculate the current Euclidean distance between two points.    
&nbsp;&nbsp;11. Create a vector joining ```departure_point``` and ```arrival_point```.  
(...)

xx. Save the optimization results into the ```.pickle``` file.  
xx. Show the optimization statistics.  


## Artificial generator:  
(...), the script ```artificial_generator.py``` was created, which contains a class ```ArtificialGenerator```.  
```Artificial_generator.__init__(self, shape_name, points=500, part_of_all_connections=0.05, data_noise_parameter=0.0)```  

* ```shape_name``` - (str) Specifies the shape of the surface. Must be one of the following: 'cube', 'sphere', 'disc', 'cylinder', 'line'  

* ```points``` - (int) Number of points to be generated. It must be a number above or equal 250. Default = 500  

* ```part_of_all_connections``` - (float) Number of all possible connections is expressed by the formula:  
  
   ```(points * (points - 1)) / 2```    
This parameter specifies how large part of the whole we want to generate. It must be a value from the range <0.01; 1>, where 0.05 means 5% of the whole. Default = 0.05  

* ```data_noise_parameter``` - (float) To simulate a real-world data collection, for each connection we can modify the calculated ```measurement_value``` by adding some noise into the data. The actual ```measurement_value``` is randomized by up to +/- (100 * ```data_noise_parameter```)% around the calculated ```measurement_value```. It must be a number from the range <0;1>. Default = 0.0


## Earth example:
In order to estimate a shape of the surface of Earth, at first 634 airports were carefully selected from all around the globe. You can find them in the ```airports.csv``` file. Following this we have to create as many connections as possible from the collected airports. Those data were collected from the site www.wego.com/schedules/ with a help of a web-scrapping script. In total, 9432 (which is around 4.7% of all possible combinations of flights) connections were found and stored in the ```flights.csv``` file.

* Why airports?   
Because we are going to use time measurements between points. In order to do that our routes have to be as straight as possible and roughly the same speed has to be maintained on all routes. Air flights sufficiently enough fulfill those conditions.

* Why did airports were carefully selected? Couldn't we just use all of them?   
Selected airports (...) There are two reasons. First we have to maintain the conditions. We need airports, on which large (roughly similar to each other) airplanes land. Second (...)

* What is an IATA code?   
An IATA (International Air Transport Association) code is a 3 letter geocode which designates airports and metropolitan areas (if a city has more than one airport)
For example:  
  * 'ATL' is a code of: "Hartsfield–Jackson Atlanta International Airport",
  * 'CGK' is a code of: "Soekarno–Hatta International Airport",
  * 'PAR' is a code of the Paris city.
  * 'LON' is a code of the London city.

* Why did you use www.wego.com website?  
This website allows to automatize the process of the web-scrapping. To collect travel time between two airports, the script visited the site: www.wego.com/schedules/XXX/YYY/ (were XXX and YYY are IATA codes) and read a median of the available results.


## Project's origin:  
It was a college project which I done by myself. After some time I created a GitHub account and I decided to add this project as a new repository. However I was not satisfied about a code quality and a visualization method, so I decided to "remaster" that project. I simplified and refactored all the code, changed visualization backend from ```matplotlib``` to ```plotly``` and added additional information about airports in Earth example.


## Technology:   
* ```Python``` 3.8  
* ```numpy``` 1.19.4  
* ```pandas``` 1.1.4 
* ```plotly``` 4.12.0
