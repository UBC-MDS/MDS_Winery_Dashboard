### Milestone 3 Reflection
*By DSCI532 Group VI* <br><br>
*Feb 06 2021*<br><br>

## Implementation  

- Our app consists of two tabs. One acts an an overview, providing general information about a filtered selection and the best wines based on these selections. The second tab is more specific, showing the individual data based on the filtered selection. 
- Bar plots are linked to the filtered selection and to each other. Users can click the bars to highlight particular varieties. 
- Cards display the recommendations based on the filtered selection. 
- We provide a data table that displays all data that corresponds to the filtered selection. Users have the option to order by specific columns and perform specific filters within this table.
- Their is a scatter plot connected to the filters and 3 additional altair widgets that directly manipulate the view on this plot (hopefully making things less overwhelming). Users can hover over the data points to see the wine names.
- A heatmap that is connected to the filter displaying the distribution of price or points (selected by user via a dropdown).
- A "learn more" button exists to explain the purpose of our app.
- A reset button exists to reset all filters when clicked.
- We removed the value-ratio scale filter from Milestone 2 due to it's ambiguity and redundancy (since value = price/points).

## What is not working?
- Currently altair does not support bi-directional influence on widgets (where the input of one widget is the output of the other, and vice versa). We were trying to have the filtered selections on the first tab always coresponding to the filters on the second tab. We could only make this uni-directional. Changes in the first tab are reflected in the second tab, but changes in the second tab are not reflected in the first tab.

- We struggled to upload an image to the dashboard while conserving the aesthetics of our dashboard.

## Feedback 

[TA and peer feedback](https://github.com/UBC-MDS/MDS_Winery_Dashboard/issues/85) was imperative to the improvement of our app. We received 3 main critiques:

1. Not enough information was being displayed in general.

We addressed this by modifying the bar charts, adding an additional plot and providing a data table. This change gives users the option for a general overview of the filtered selection (via the first tab) and a more in-depth view of their selection (via the second tab).

2. The scatter plot  tended to be overwhelming because of an overflow of data. 

We addressed this in 3 ways. By introducing miniature widgets, we give more flexibility to the user to modify their view of the data on the scatter plot. By introducing a data table we give users direct view of the data. Finally, by implementing a heatmap, users can see the general trends that are present with each wine type. 

3. General aesthetics and ease of use. 

We tried to improve aesthetics in general using nicer colours and making spacing better. Furthermore, we added a reset button that should improve user's quality of life. 

##  R/ggplotly or Python/Altair?

As a team, we find Altair more user friendly (and we have more experience with it). The difficult part of using Altair was the data wrangling, which was already completed in Milestone 2. We also found that it was easier to create a layout and found ggplot objects to be a little 'clunky'.

