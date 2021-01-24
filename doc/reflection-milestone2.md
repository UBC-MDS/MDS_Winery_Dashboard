This file documentes what this app has been implemented in the dashboard so far, as well as what features have not been done yet.

## Milestone 2 Implementation
- Right now, our dashboard is able to let customers filter the wine data for a single desired US state and a single wine variety, using the left-side dropdown menu. In addition, there are two sliders that will filter the data based on wine price and rating points. This will enable customers to narrow down their selection and compare products within this range.
- The choropleth map of US in the top right, works as a heatmap showing the number off reviews in the selected state. Moreover, we have added an interactive feature that shows the average rating, price, value(price per point) and number of reviews.
- There are two plots. The first is a scatter plot showing all available wines that fall under the filtered criterion. Customers can see the relationship between price and points for all of the available wines. Furthermore, there is a bar chart that displays the average price for the current filtered wine type and origin. Customers are able to browse the names of the wines by interacting with the scatter plot. 
- Finally, a recommendation is given to the customer based on the filtered criterion. The two recommendations are given based on the wine with the highest number of points as well as the wine that is considered to have the best value (number of points given the wine's price)

## Future Implementation and Bugs
- We have not allowed for the selection of multiple wine types. This is because we have not been able to update our recomendation cards based on multiple selections. However, the code can currently filter the graphs based on multiple wine selections (however we have removed this argument for the milestone 2 release as it would have caused our cards to be blank). We will add this functionality properly in milestone 4.
- Multiple states selction has not been implemented, and will be tested further how this can be in effect (similar reason as above).
- The value-ratio scale is not yet connected to our graphs
- The bar chart is currently not displaying the average correctly (due to some missing data)
- Since there is missing data in some states and wine types, the errors keep poping up in dashaborad. This should be better fixed in the future milestones.
- We want to allow the user to select a different function for the bar chart (for example instead of average price, the user can select average points)
- We want to improve the aesthetic of the interface to improve the user's experience
- We need to decrease the scale on the map legend
- The selection of states and wine variety can be sorted alphabetically, so customers can easily find the desired combinations.
- We currently have a second tab that doesn't do anything. We may try to include some instructions and a GIF in this tab if time permits. 

## App Limitations
- So far, some shortcomings of this dashboard are the limitation to the united states only, even though the dataset sampled the global data.
- Furthermore, due to our lack of knowledge the drop down for wine variety is very long. We would have liked to aggregate wine types that are similar to not overwhel the customer with this large range to select from. 
