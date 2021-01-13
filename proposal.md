### Section 1: Motivation and Purpose

Our role: Data Science Team Hired at Vancouver Winery

Target audience: Customers Coming for Wine Tasting

There is a diverse array of available wines that exist in North America. The variety alone is enough to overwhelm the common consumer of wine products; there needs to be a way to convey key information about these wines to help customers make informed selections during their wine tasting events. To do this, we will build a dashboard to help customers visualize the intricacies that disintguish different wines in North America particularily in terms of quality, price, origin and flavour. Our app will show the distribution of these factors by filtering and re-ordering on different characteristics to make direct comparisions between different types of wine. 

### Section 1:Description of the data

In this project, we are using the [Wine Reviews](https://www.kaggle.com/zynicide/wine-reviews) Kaggle data set that contains 130k wine reviews with variety, location, winery, price, and description. The data scraped from WineEnthusiast on November 22nd, 2017, and it only contains wines with a review score higher than 80 between 1999 and 2017. For this project, we use the 54,762 instances of wine reviews from North America. 

Each review consists of 13 explanatory variables that describe the wine in terms of origin (country, province, designation, region, winery), bottle information and reviews (description, points/ rating, price, title, variety), and information about the reviewers (taster name, taster Twitter handle). We are likely to select `country`, `description`, `points`,  `price`, `province`, and `variety` variables for our dashboard.

### Section 3: 

Joel is a fantastic instructor and an Olympics enthusiast but knows nothing about wine. One day, he decided to visit the MDS winery to try a variety of wines to ….
. 
He wants the experience to be very smooth and easy. To do so, MDS Winery hired us to create a dashboard for customers such as Joel to let them individually explore their interests in various wine selections. When Joel starts exploring the dashboard, he will see an overview of the wine menu. From there, he will be able to filter by wine variety, origin, price, and professional score. 

Joel is interested in expensive white wine and he also heard that California is known for their Chardonnay. From the wine variety he’ll pick Chardonnay and filter for California. Finally, he will adjust the price based on his budget. From the generated list, Joel can add multiple wines to his tasting experience.
