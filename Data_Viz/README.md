
#Data Visualization Project

##Data Set:
I used the Global Terrorism Database for my data set.
I pared down the data set to remove incidents with a month or day value of 0,
I removed a fair number of the collumns that I would not be using, in order to 
make the size of the file more managable. 

##Feedback:

###D Wood:

* Scale the circles as you zoom ()
* Mousewheel zoom feature (done)
* Clarification of what the colors mean(done)
* Perhaps change the map projection ()
=======
Data Set:
I used the Global Terrorism Database for my data set. I pared down the data set to remove incidents with a month or day value of 0,
I removed a fair number of the collumns that I would not be using, in order to make the size of the file more managable. This still left a data file which is over 10mb. 

The Visualization:

This visualization takes the viewer on a brief tour of the terrorist attacks found in the last 20 years, according to the Global Terrorism Database released by the University of Maryland. The first section animates the most commonly found terrorist attack type in each country, across the time span. The viewer is then able to take a look at specific spans of time within the total span. If the viewer selects a country it zooms to the country and plots each terrorist attack, and allows the viewer to take a look at specific years.

Feedback:

D Wood:

* Mousewheel zoom feature - Done
* Clarification of what the colors mean - Done
* Perhaps change the map projection - Changed the detail level from 10m resolution to 50m

S Eastman:

* "Add news paper clippings" - Would be great if reasonably accessable, would definitely consider doing this if it were a product
* If possible add a link to more information about each group involved - No reliable data available.
* Make tooltip background more opaque - done

D Grossman-Laskin:

* Suggested grouping similar attack types with similar colours - Decided not to do this because there I wanted to draw more attention to the various types of attacks, independent of what similarities they may share with other attack types.

* Suggested putting the average number of attacks per year on each country - Again this was not in line with the narrative that I wanted to tell.

* Asked why I was displaying the range of years and not individual years - I told her that I wanted to communicate the change over time of the type of attacks that prevail in different parts of the world.
>>>>>>> origin/master

###S Eastman:

* "Add news paper clippings/ summary information"()
* If possible add a link to more information about each group involved()
* Make tooltip background more opaque(done)

###Project Reviewer
* Animating from the start is confusing (added a start button)
* Animating the data points being added to the country 
makes it difficult to tell what it going on
* Use Markdown in Readme (done)
* Comment certain code blocks (done)
* Formatting changes for code (done)

<<<<<<< HEAD
##References:
http://giscollective.org/d3-basemap-with-top/
http://bost.ocks.org/mike/map/
http://bl.ocks.org/mbostock/6408735
http://stackoverflow.com/questions/14492284/center-a-map-in-d3-given-a-geojson-object
http://h3manth.com/content/javascript-referenceerror-invalid-left-hand-side-assignment
https://coderwall.com/p/psogia/simplest-way-to-add-zoom-pan-on-d3-js
=======
References:
* http://giscollective.org/d3-basemap-with-top/
* http://bost.ocks.org/mike/map/
* http://stackoverflow.com/questions/14492284/center-a-map-in-d3-given-a-geojson-object
* http://h3manth.com/content/javascript-referenceerror-invalid-left-hand-side-assignment
* https://coderwall.com/p/psogia/simplest-way-to-add-zoom-pan-on-d3-js
* http://sujeetsr.github.io/d3.slider/

>>>>>>> origin/master
