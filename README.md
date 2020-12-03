# Surface Shape Estimator is a program which allows to estimate a shape of the surface based solely on a collection of connections between two points on that surface. Data about a single connection store 3 information: code names of a first and second point and an Euclidean distance or a travel time between those points.

> :warning: **If you use a travel time as a measurement**: You have to make sure that the same speed was maintained during all measurements and that the connection lines were straight.  

## Menu:
* [Implementation](#implementation)
* [Optimization algorithm](#optimization-algorithm)
   * [Optimization parameters](#optimization-parameters)
   * [Algorithm](#algorithm)
* [Artificial generator](#artificial-generator)
* [Earth example](#earth-example)
   * [FAQ](#faq)
* [Launch](#launch)
* [Project's origin](#projects-origin)
* [Technology](#technology)

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

* ```optimized_points_file``` - (str) full name of the file which stores already optimized coordinates (xyz) of each point and some additional information. The file must be in ```.pickle``` format. After each optimization process a new ```.pickle``` file is generated, which saves the results. Passing a ```.pickle``` file as a parameter skips the whole optimization process which saves time and allows to load previously calculated results. If a ```.pickle``` file is passed as the parameter, the value of the ```duplicate_data``` parameter is irrelevant, because that value is saved in the file. By default the results will be saved in the ```optimized.pickle``` file. The ```earth.pickle``` file is a valid example. Default = None.


## Optimization algorithm:
Keep in mind that the optimization process may take up to several minutes, depending on how many connections the ```connection_file``` contains.  

### Optimization parameters:   
* ```mod``` - (float) a modifier, which regulates by how much the points coordinates may be adjusted. Set to 0.5.  
* ```iterations``` - (int) a maximum number of iterations. Set to 250.  
* ```tol``` - (float) a tolerance value. If the ```mod``` value falls below the ```tol``` value, the optimization process will stop. Set to 0.001.  
* ```optimized_points_file_name``` - (str) a name of the ```.pickle``` file which will be created after the optimization. It will contain the optimized data (and some additional information). Set to 'optimized_points.pickle'  

### Algorithm:  
1. Find a point with the largest number of connections.
2. Create a set of unique points from the ```connections_file```.  
3. Place all of the points (from the set) at random on 3-D space. 
4. Calculate errors (cumulative, average, max)
5. i = 0.  
6. Repeat if i < ```iterations```:  
6.1. Shuffle the data from the ```connections_file```.  
6.2. Make a copy of current points coordinates.  
6.3. Repeat for each connection in ```connections_file```:    
&nbsp;&nbsp;&nbsp;6.3.1. Calculate the current Euclidean distance between two points.       
&nbsp;&nbsp;&nbsp;6.3.2. Create a vector joining ```departure_point``` and ```arrival_point```.   
&nbsp;&nbsp;&nbsp;6.3.3. Choose which point will have its coordinates changed.  
&nbsp;&nbsp;&nbsp; * If both of the points are not the point with the largest number of connections, pick a point at random.  
&nbsp;&nbsp;&nbsp; * Else if one of the point is the point with the largest number of connections, always pick the other one.   
&nbsp;&nbsp;&nbsp;6.3.4. If the calculated distance between points is longer than the expected one:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.4.1. If the first point was chosen in step 6.3.3:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.4.1.1. Modify point's coordinates (x, y, z) by adding to the coordinates: ```mod``` * calculated vector (from the step 6.3.2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.4.2. If the second point was chosen in step 6.3.3:    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.4.2.1. Modify point's coordinates (x, y, z) by adding to the coordinates: -```mod``` * calculated vector (from the step 6.3.2)  
&nbsp;&nbsp;&nbsp;6.3.5. If the calculated distance between points is shorter than the expected one:    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.5.1. If the first point was chosen in step 6.3.3:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.5.1.1. Modify point's coordinates (x, y, z) by adding to the coordinates: -```mod``` * calculated vector (from the step 6.3.2)    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.5.2. If the second point was chosen in step 6.3.3:    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3.5.2.1. Modify point's coordinates (x, y, z) by adding to the coordinates: ```mod``` * calculated vector (from the step 6.3.2)      
6.4. Calculate errors (cumulative, average, max)  
6.5. If the current cumulative error is bigger than the previous one:   
&nbsp;&nbsp;&nbsp;6.5.1. Reduce the ```mod``` value by 5% and restore the previously saved points coordinates (from the step 6.2).   
&nbsp;&nbsp;&nbsp;6.5.2. If the ```mod``` value is below the ```tol``` value:    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.5.2.1. Stop the optimization process (Skip to the point 7).     
6.6. i += 1.   
7. Save the optimization results into the ```optimized_points_file``` file.  
8. Show the optimization statistics.  


## Artificial generator:  
In order to test the ```ShapeEstimator``` class, a new script ```artificial_generator.py``` was created, which contains a class ```ArtificialGenerator```. The purpose of this class is to see what ```ShapeEstimator``` will estimate when we know, which surface shape shall be expected, based on amount and quality of data we will provide.  
```Artificial_generator.__init__(self, shape_name, points=500, part_of_all_connections=0.05, data_noise_parameter=0.0)```  

* ```shape_name``` - (str) specifies the shape of the surface. Must be one of the following: 'cube', 'sphere', 'disc', 'cylinder', 'line'  

* ```points``` - (int) number of points to be generated. It must be a number above or equal 250. Default = 500  

* ```part_of_all_connections``` - (float) number of all possible connections is expressed by the formula:  
  
   ```(points * (points - 1)) / 2```    
This parameter specifies how large part of the whole we want to generate. It must be a value from the range <0.01; 1>, where 0.05 means 5% of the whole. Default = 0.05  

* ```data_noise_parameter``` - (float) to simulate a real-world data collection, for each connection we can modify the calculated ```measurement_value``` by adding some noise into the data. The actual ```measurement_value``` is randomized by up to +/- (100 * ```data_noise_parameter```)% around the calculated ```measurement_value```. It must be a number from the range <0;1>. Default = 0.0


## Earth example:
In order to estimate a shape of the surface of Earth, at first 634 airports were carefully selected from all around the globe. You can find them in the ```airports.csv``` file. The next step is to create as many connections as possible from the collected airports. Those data were collected from the site www.wego.com/schedules/ with a help of a web-scrapping script. In total, 9432 (which is around 4.7% of all possible combinations of flights) connections were found and stored in the ```flights.csv``` file. If you want to see the results, include the files: ```flights.csv```, ```airports.csv```, ```color_definitions.csv``` and ```earth.pickle``` as the ```ShapeEstimator``` class parameters.  

### FAQ:  
* Why airports?   
Because we are going to use time measurements between points. In order to do that our routes have to be as straight as possible and roughly the same speed has to be maintained on all routes. Air flights sufficiently enough fulfill those conditions.

* Why did airports were carefully selected? Couldn't we just use all of them?   
Selected airports are in a significant majority the international airports. This type of the airports gives the biggest chances of fulfilling the previously mentioned conditions. First, large (roughly similar to each other) planes land on those airports. Second, this type of airports offers a large number of connections, which significantly improves the data quality. Of course in this data set, there are smaller, more local airports. They come from low population density areas such as: Oceania, southern part of the South America, north Canada or north Russia.

* What is an IATA code?   
An IATA (International Air Transport Association) code is a 3 letter geocode which designates airports and metropolitan areas (if a city has more than one airport)
For example:  
  * 'ATL' is a code of: "Hartsfield–Jackson Atlanta International Airport",
  * 'CGK' is a code of: "Soekarno–Hatta International Airport",
  * 'PAR' is a code of the Paris city.
  * 'LON' is a code of the London city.

* Why did you use www.wego.com website?  
This website allows to automatize the process of the web-scrapping. To collect travel time between two airports, the script visited the site: www.wego.com/schedules/XXX/YYY/ (were XXX and YYY are IATA codes) and read a median of the available results.

* I started the optimization process by myself, but the results are clearly different from those presented in the ```earth.pickle``` file. Why is that?  
It is not the fault of the optimizer but the data itself. Collected number of flights (9432) may seem adequate, but in the reality it is just passable. There is a considerable number of points with a very low number of connections (3+), which leads to an ambiguity (especially in the Oceania). Don't forget, that we're dealing with real data, so there is some level of noise. According to my tests, the "proper" result generates itself in around 40% of cases, with the ```duplicate_data``` parameter set to True. The data in the ```earth.pickle``` file are one of those cases, which almost perfectly represents the surface of Earth.

## Launch:  
* To see the results calculated by the optimizer (from the ```ShapeEstimator``` class) launch the ```draw_plot``` method.  
* To generate artificial data (from the ```ArtificialGenerator``` class) launch the ```generate_connections``` method.  

## Project's origin:  
It was a university project which I done by myself. After some time I created a GitHub account and I decided to add this project as a new repository. However I was not satisfied about a code quality and a visualization method, so I decided to "remaster" that project. I simplified and refactored all the code, changed visualization backend from ```matplotlib``` to ```plotly``` and added additional information about airports in Earth example, in order to distinguish the continents.


## Technology:   
* ```Python``` 3.8  
* ```numpy``` 1.19.4  
* ```pandas``` 1.1.4 
* ```plotly``` 4.12.0
