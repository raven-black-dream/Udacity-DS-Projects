
# Data Visualization Project

## Data Set:
I used the Global Terrorism Database for my data set.
I pared down the data set to remove incidents with a month or day value of 0,
I removed a fair number of the collumns that I would not be using, in order to 
make the size of the file more managable. 

## Initial Design Decisions

### Narrative
In my initial exploration of this dataset I was struck by the likley correlation between geographical area and attack type.
I used this project to explore that correlation as well as to follow the evolution of terrorist activity over the last few decades.
On a smaller scale I also wanted to show the distribution of terrorist attacks within a country's geography as well.

### Design
I decided to plot the most common incident types by county on a map, in order to show what I felt would be a strong correlation
between where a country is in the world and what sort of terrorist attacks are prevalent. I decided to plot the change over time,
because I noticed in my initial exploration of the data that there has been an evolution away from what I would consider more personal
forms of Terrorism (Kidnappings, Assassinations, Armed Assaults on Facilities) in favour of less personal attacks (bombings). 
I then decided that it would also be interesting to plot each incident within the country that it occurred in. I thought that this
further show the correlation between geographical location, as well as provide an interesting way to look at the change in attacks
over time. I was hoping to show that there was an increase over time, subsequently I have found that the countries which the trend
is most obvious in are over plotted to begin with, and that the change over time doesn't show well. Initially I animated the change
over time, after selecting a country, thinking that it would provide an interesting way to explore the data. 

## Feedback:

### D Wood:

* Scale the circles as you zoom ()
* Mousewheel zoom feature (done)
* Clarification of what the colors mean(done)
* Perhaps change the map projection ()

### S Eastman:

* "Add news paper clippings" - Would be great if reasonably accessable, would definitely consider doing this if it were a product
* If possible add a link to more information about each group involved - No reliable data available.
* Make tooltip background more opaque - done

### D Grossman-Laskin:

* Suggested grouping similar attack types with similar colours - Decided not to do this because there I wanted to draw more attention to the various types of attacks, independent of what similarities they may share with other attack types.
* Suggested putting the average number of attacks per year on each country - Again this was not in line with the narrative that I wanted to tell.
* Asked why I was displaying the range of years and not individual years - I told her that I wanted to communicate the change over time of the type of attacks that prevail in different parts of the world.

###Project Reviewer
* Animating from the start is confusing (added a start button)
* Animating the data points being added to the country 
makes it difficult to tell what it going on 
* Use Markdown in Readme (done)
* Comment certain code blocks (done)
* Formatting changes for code (done)


##References:
* http://giscollective.org/d3-basemap-with-top/
* http://bost.ocks.org/mike/map/
* http://bl.ocks.org/mbostock/6408735
* http://stackoverflow.com/questions/14492284/center-a-map-in-d3-given-a-geojson-object
* http://h3manth.com/content/javascript-referenceerror-invalid-left-hand-side-assignment
* https://coderwall.com/p/psogia/simplest-way-to-add-zoom-pan-on-d3-js
* http://sujeetsr.github.io/d3.slider/
