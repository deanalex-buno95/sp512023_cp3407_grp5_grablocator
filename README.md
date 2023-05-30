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
    - `add_orders.py` — Add test orders into the DB.
    - `add_stations.py` — Add stations into the DB.


## Timeline

### Sprint 1 (Week 6 to Week 7)
Sprint 1 involves dealing with the login and register forms in `login.html` and `register.html`.
From there, we made use of the WTForms module to create the forms based on the necessary fields that we need to fill in.
With the help of `layout.html`, alongside the CSS, we made two pages that will link to the rest of the website.
To limit who can reach the `index.html` dashboard, we make use of `session` and `redirect` to redirect anyone that has not signed up back to the login and register page.
Lastly, CSS helps to beautify the website.

### Sprint 2 (Week 8 to Week 9)
Sprint 2 involves dealing with the main functionality of the website. 
The pages meant for this are `history.html`, `orders.html`, and `selectedorder.html`, the latter of which was added from the original list.
From the `index.html`, after the creation of the two buttons, we would start of with adding stations (intermediate stops) into the DB using `add_stations.py`.
These will be the intermediate stops that the driver's would be told to go to if he/she meet certain conditions.

The conditions are as follows:
- Age (a driver must be aged 21 to 69, but at age 50, the driver is a senior driver, limited to 1 part of travel [an intra-sector trip has 2, while an inter-sector trip has 3]).
- Years of experience (if you have worked in Grab for 5 years, you will be experienced enough to do two parts of travel, while anyone did for 8 years will do all 3).

All stations would be added to the `ADDRESS`, `DESTINATION`, `PICKUPDEST`, and `FINALDEST` in `grab_locator.db`, denoted by the `ST` prefix.
After we have added the stations utilizing the `stations.csv` CSV file and `add_stations.py` Python script, we would add the test orders in.
It is done in the same way as adding the stations but with `add_orders.py` and `orders.csv`.
Plus, the `GRABORDER` table will also be filled as well as the other 4 tables.

Once we have the needed data added into the DB, we would create the `orders` page that has these two types of orders:
- Available (no driver ID in the `GRABORDER` record, but linked by postal sector)
- Pending (with the user's driver ID)

Then, we created the `selectedorder` page, where depending on which order is the parameter, would display the information and prompts.
Here is a list of information and prompts that it will show:
- From — The pickup destination.
- To — The final destination.
- Stopping Point — The point where the algorithm that takes the age and experience recommends ending the journey at.
- Prompts:
    - Start (available order only) — Accept the job that is available, setting it to pending.
    - Finish (pending order only) — End the job and either reset the pickup destination or remove the order completely.

Lastly, we created the `history` page, where it displays locations that the user has been to during his/her travel.
This is done by accessing the `DRIVERDEST` table in `grab_locator.db` and showing the address and date that the user has been in that destination.

Key things to note is that at this moment, the JavaScript of this project is still within the `layout.html` file that is used to format the pages.
We will add a separate JavaScript file to tidy up the JS code for the next SPRINT.
As for whether the `selectedorder` page will have the map APIs, that remains to be determined provided the limited time.

### Sprint 3 (Week 10 to Study Week 2)
Sprint 3 involves completing the main functionality and uploading the website to PythonAnywhere from GitHub.

From the `selectedorder` page, we added another prompt called "Cancel".
This would remove the driver ID from a pending job, making it available again.

Then, we did some testing with all the necessary features, from the History page, and both orders page.
Considering that we ran out of time, we decide to leave out the map, but the core functionality outside the map is still here.

Lastly, we have uploaded the final result of the website locally into PythonAnywhere.

With the help of the video, we are able to clone this repository into the PythonAnywhere domain:
- Help Video: <a href="https://youtu.be/4sTZN15J33A">https://youtu.be/4sTZN15J33A</a>
- Web Site Domain: <a href="http://shadowmamba95.pythonanywhere.com/">http://shadowmamba95.pythonanywhere.com/</a>