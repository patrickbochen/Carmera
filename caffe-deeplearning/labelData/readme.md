hotnot.py README.md

Local web app to help expedite the process of manually labeling images. Uses a Flask framework to create the python web application. Flask uses Jinja2 as an easy templating language. Flask employs RESTful (REST - Representational State Transfer) requests dispatching to exchange data.

Templates folder contain varying templates defining pages in the web app.

All of the python code is in hotnot.py and some javascript and html in the templates since it is a fairly simple program.

Web App Functionality:
Displays current labeled images in the form of image id and tag.
Labeling randomly selected images from Carmera image database.
Saves tags to text files (will seperate into testing and training data)


Notes:
Still using Euclid as a way of accessing Carmeras SDK. Update this to production API key for further use. Also because production uses a different set of image_ids need to make a new database. 

Relabeling modularity and the entire program's modularity is bad.

Fairly slow and boring way to label images. Need to actually add to web rather than local if you want multiple people helping label.

