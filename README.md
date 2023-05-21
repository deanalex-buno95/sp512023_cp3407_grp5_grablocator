# CP3407 (SP51 2023) Group 5 Project – GrabLocator

## Project Description

### Problem
Online delivery services, like Grab, have been extremely popular for delivering items like groceries and food to people’s homes, especially during the pandemic three years ago. However, as the years have gone by, there are a few issues revolving around this service.

The issues are as follows:
- Currently, the Grab service is too expensive.
- A portion of it goes to how much time taken by the driver to move from point A to B and how far points A to B are located.
- However, not every driver has a full understanding of where they are serving, specifically the destination of the area.
- As a result, they get lost and might take the wrong turn, especially in unfavorable circumstances, leading to a longer service and, possibly, ruined orders.
- A good example would be a particular driver from Gojek, a company similar to Grab, when he drove into a swimming pool in a condominium in Bukit Timah after being lost in the heavy rain due to low visibility (Leong, 2023).

As a result, we feel that a website that tackles this issue would be of great benefit for the drivers.


### Goal
The main goal is to make a Grab-based website that helps drivers to smoothly transfer the order from one location to another by tailoring the decision-making of where driver’s would have to drive based on their experiences and preferences of drivers.

We proposed that we would utilize Python and the following tools to create our website:
- APIs such as Google Maps, Foursquare, and OneMap to determine the location addresses.
- SQLite3 for the database.
- Flask for the local web server.

Considering that we are making use of SQLite3, a well-known database engine, along with Flask and the APIs mentioned, we believe that this would be considered as feasible.


## Files List

Here are the list of files used for this assignment:
- Templates:
    - `layout.html` — Base HTML file used for the layout of the whole website.
    - `login.html` — Login form for existing users of the website.
    - `register.html` — Registration form for new users of the website.
    - `index.html` — Main dashboard that shows the two main functions.
    - `orders.html` — A list of orders available and pending.
    - `selectedorder.html` — Main functionality, to accept orders based on age and experience.
    - `history.html` — History page to show which locations you have been.
    - `about.html` — About page.
    - `contact.html` — Contact page.
- CSV:
    - `orders.csv` — CSV file that contains the existing orders.
    - `stations.csv` — CSV file that contains information of orders.
- Python:
    - `app.py` — Main application file.
    - `forms.py` — WTForms file that contains all the necessary forms utilized in the website.


## Timeline

### Sprint 1 (Week 6 to Week 7)
Sprint 1 involves dealing with the login and register forms in `login.html` and `register.html`.
From there, we made use of the WTForms module to create the forms based on the necessary fields that we need to fill in.
With the help of `layout.html`, alongside the CSS, we made two pages that will link to the rest of the website.
To limit who can reach the `index.html` dashboard, we make use of `session` and `redirect` to redirect anyone that has not signed up back to the login and register page.
Lastly, CSS helps to beautify the website.

### Sprint 2 (Week 8 to Week 9)

### Sprint 3 (Week 10)