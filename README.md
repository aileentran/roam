# Roam 🚀- Beta Version
"All roads lead to Rome." A full-stack Flask application for commuters with multiple modes of transportation. Users can create routes with many stops, choose the mode of transportation, and save it. The application will return accurate travel times based on live traffic information and render both visual and text directions. 

Website: http://alwaysroamin.com/

### About Creator🍵🌸
Roam was created by Aileen Tran, a developer in the Bay Area. Learn more about her on [LinkedIn](https://www.linkedin.com/in/aileentran27/).

## Tech Stack📚
Front end: HTML, CSS, Javascript, jQuery, Bootstrap

Back end:Postgres relational database, Python, Jinja

Google Maps APIs: Places API, Maps Javascript API, Distance Matrix API

## Features✨
![User registration/login](/static/images/readme/registerandlogin.png)
Users can register and login safely thanks to password hashing using werkzeug.security!

![Creating route and choosing mode of transportation and stop order](/static/images/readme/stoporder.png)
Users can create customized routes by adding as many stops as they want and customizing the mode of transportation for each stop. 
For example:
>You're living your best life (because your home is at Fenton's Creamery🍨) and you need to go to Hackbright Academy. <br>
>One of your favorite routes is to: <br>
>(1) Drive to the San Leandro Bart station (first stop) <br>
>(2) Take the Bart in to San Francisco, ultimately getting to Hackbright (second stop)

![Saving route](/static/images/readme/savedroutes.png)
There is a side panel with all of the saved routes.
>Look at all the ways you try to get to Hackbright! Ah, Bay Area commuting life.

![New route added to saved routes](/static/images/readme/newroutesaved.png)
Under Saved Routes, there is the new route that was created!
>Phew! There's the new route you just made.

![Compare travel times](/static/images/readme/comparetraveltimes.png)
After clicking Compare Travel Times, users can see the time estimates for ALL of their customized routes based on LIVE traffic data!
>How is the traffic flow looking this morning? 

![Choosing route](/static/images/readme/choosingroute.png)
User can select any saved route.
>Ah, taking West Oakland Bart might be the fastest way, but based on experience, there's probably no more parking (future feature🔮 to know for sure??). <br>
>Let's go through Lake Merritt instead!

![Selected route](/static/images/readme/hittingdirections.png)
After selecting a route, the user can see all the stops and modes of transportation. 
>Yup, that's the route! And you get there by driving to Lake Merritt and taking public transportation to Hackbright.

![Map directions and text for selected route](/static/images/readme/viewingdirections.png)
After clicking Directions, users can visually see the directions and ordered stops on the map with directions text and travel times.
>Okay! You know how to get there and know exactly how long it will take. No more looking up the routes for every mode of transportation. No remembering each individual travel time. No more guessing. Yay!🤩

<br><br>

## Future Features🔮

- Get live parking information of major public transportation locations
- Alert system customized by the user with accurate departure times - Twilio and Celery APIs

### Note⚠️
This application is currently in Beta Version. Even though the passwords are hashed, please do not include sensitive information such as important passwords or addresses. 
