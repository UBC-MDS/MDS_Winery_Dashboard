# MDS Winery Dashboard

## About this app

The link to the deployed dashboard:
https://winery-mds-2021.herokuapp.com/

This dashboard allows you to explore wine varieties, price and rating information by the winery locations across United States. By comparing the selected wine products, customers are able to make their wise purchase based on informative and interactive bar charts.


## Authors

* **Jianru Deng** -[@jianridine](https://github.com/jianridine)

* **Mo Garoub** -[@mgaroub](https://github.com/mgaroub)

* **Kamal Moravej Jahromi** -[@kmoravej](https://github.com/kmoravej)

* **Neel Phaterpekar** -[@nphaterp](https://github.com/nphaterp)

## Description of the App & Sketch

This dashboard is designed to have three main graphs on the home page. Using the left-side filtering dropdown and scales, users can filter the conditions they desire by indicating one or multiple selections of country, province, wine variety, as well as the range of the review points and corresponding prices. According to the filtered conditions on the side, the choropleth map at the top highlights the relative areas as a heatmap, in which the darker-colored area has a higher volume of reviews with tooltip indicating number of reviews, average review points and prices, etc. On the bottom-left side of the page, a bar chart displays the average price given a selected wine variety. This gives a good comparison on price range and desired wine type for users to base their decision on. The last graph is a scatter plot that shows the relationship between the points and prices given the selected ranges. This  enables users to better understand if the price pays off it's value according to the given points by testers. In the bottom corner, bottle recommendations are made using the highest review points and best value (price per point), respectively.


![](https://media.giphy.com/media/v0C45RM0xAzD1n3Ei8/giphy.gif)


## Requirements
- Python 3

## How to run this app
We suggest you to create a virtual environment for running this app with Python 3. Clone this repository and open your terminal/command prompt in the root folder.<br>

```
git clone https://github.com/UBC-MDS/MDS_Winery_Dashboard
cd MDS_Winery_Dashboard/src
python3 -m virtualenv venv

```


In Unix System:
```
source venv/bin/activate
```

In Windows:

```
venv\Scripts\activate
```

Install all required packages by running:

```
pip install -r requirements.txt
```


Run this app locally with:<br>
```
python app.py
```

## Reference
Thoutt, Z. (2018). [Wine Reviews dataset](https://www.kaggle.com/zynicide/wine-reviews/data).
