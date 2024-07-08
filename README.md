# ChartPatterns - Automate the detection of chart patterns with Python

Make it easy to detect well-known chart patterns such as ascending triangles, head and shoulders, flag, etc with the `chart_patterns` python
library.  Like Thomas Bulkowski says in his book, `Encyclopedia of Chart Patterns`, "To knowledgeable investors, chart patterns are not squiggles on a price chart; they are the footprints of the smart money." This python package hopefully helps in this regard.

Table of Contents
=================

* [Available Chart Patterns](#available-chart-patterns)
* [Installation](#installation)
* [Getting Started](#getting-started)
   * [Doubles](#doubles)
   * [Flag](#flag)
   * [Head and Shoulders](#head-and-shoulders)
   * [Inverse Head and Shoulders](#inverse-head-and-shoulders)
   * [Triangles](#triangles) 
   * [Pennant](#pennant)
* [Resources](#resources)


## Available Chart Patterns

Here is a list of currently available and soon to be available chart patterns:

- [x] Doubles

- [x] Flag

- [x] Head and Shoulders

- [x] Inverse Head and Shoulders

- [x] Triangles

- [x] Pennant

- Rounding bottom and top

- Triples

- Wedge

## Installation

Install the `chart_patterns` package by cloning this repo. Place the folder in your working directory.

> git clone https://github.com/zeta-zetra/chart_patterns

Make sure to install the required packages using the requirements.txt file. 

> pip install -r requirements.txt

## Getting Started

Once you have installed the package, then you can get started. We provide detailed examples of each of the available chart patterns in the package.

### Doubles

```
 import pandas as pd
 from chart_patterns.chart_patterns.doubles import find_doubles_pattern
 from chart_patterns.chart_patterns.plotting import display_chart_pattern



 # read in your ohlc data 
 ohlc = pd.read_csv("eurusd-4h.csv")  #headers include - open, high, low, close

 # Find the double bottom pattern
 ohlc = find_doubles_pattern(ohlc, double="bottoms")

 # Find the double tops pattern
 ohlc = find_doubles_pattern(ohlc, double="tops")
 

 # Plot the results 
 display_chart_pattern(ohlc, pattern="double") # If multiple patterns were found, then plots will saved inside a folder named images/double  

```

In the `find_doubles_pattern` function one can change the following:
 - The maximum ratio between the peak points in the tops chart pattern. See the `tops_max_ratio` parameter.
 - The minimum ratio between the trough points in the bottoms chart pattern. See the `bottoms_min_ratio` parameter.

### Flag

```
 import pandas as pd
 from chart_patterns.chart_patterns.flag import find_flag_pattern
 from chart_patterns.chart_patterns.plotting import display_chart_pattern

 # read in your ohlc data 
 ohlc = pd.read_csv("eurusd-4h.csv")  #headers include - open, high, low, close

 # Plot the results 
 display_chart_pattern(ohlc, pattern="flag") # If multiple patterns were found, then plots will saved inside a folder named images/flag  
 
```

### Head and Shoulders

```
 import pandas as pd
 from chart_patterns.chart_patterns.head_and_shoulders import find_head_and_shoulders
 from chart_patterns.chart_patterns.plotting import display_chart_pattern

 # read in your ohlc data 
 ohlc = pd.read_csv("eurusd-4h.csv")  # headers must include - open, high, low, close

 # Find the head and shoulers pattern
 ohlc = find_head_and_shoulders(ohlc)

 # Plot the results 
 display_chart_pattern(ohlc, pattern="hs") # If multiple patterns were found, then plots will saved inside a folder named images/hs  


```


### Inverse Head and Shoulders

```
 import pandas as pd
 from chart_patterns.chart_patterns.inverse_head_and_shoulders import find_inverse_head_and_shoulders
 from chart_patterns.chart_patterns.plotting import display_chart_pattern

 # read in your ohlc data 
 ohlc = pd.read_csv("eurusd-4h.csv")  # headers must include - open, high, low, close

 # Find inversr head and shoulders
 ohlc = find_inverse_head_and_shoulders(ohlc)

 # Plot the results 
 display_chart_pattern(ohlc, pattern="ihs") # If multiple patterns were found, then plots will saved inside a folder named images/ihs  
```


### Triangles

```
 import pandas as pd
 from chart_patterns.chart_patterns.triangles import find_triangle_pattern
 from chart_patterns.chart_patterns.plotting import display_chart_pattern

 # read in your ohlc data 
 ohlc = pd.read_csv("eurusd-4h.csv")  # headers must include - open, high, low, close

 # Find the ascending triangle
 ohlc = find_triangle_pattern(ohlc)

 # Find the descending triangle
 ohlc = find_triangle_pattern(ohlc, triangle_type="descending")

 # Find the symmetrical triangle 
 ohlc = find_triangle_pattern(ohlc, triangle_type="symmetrical")

 # Plot the results 
 display_chart_pattern(ohlc, pattern="triangle") # If multiple patterns were found, then plots will saved inside a folder named images/triangle  

```


### Pennant

```
import pandas as pd
from chart_patterns.chart_patterns.pennant import find_pennant
from chart_patterns.chart_patterns.plotting import display_chart_pattern

# read in your ohlc data 
ohlc = pd.read_csv("eurusd-4h.csv")  # headers must include - open, high, low, close

# Find the head and shoulers pattern
ohlc = find_pennant(ohlc, progress=True)


# Plot the results 
display_chart_pattern(ohlc, pattern="pennant")

```


## Resources

We have a [YouTube channel](https://www.youtube.com/@zetratrading/featured) where we go through the code of the chart patterns. In addition, we have a git [repo](https://github.com/zeta-zetra/code#automate-chart-patterns) with extra code covering other trading related material. 