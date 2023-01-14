# TSOHA App

The main point of TSOHA Trainer's App is to enable users to keep record of their workouts. They can also add new moves to the database if their desired move has yet to be added by someone else. Existing moves can be used to create training templates, which, in turn, can be used to quickly add predefined moves to a new workout session.

No web application is complete without some social aspect, so TSOHA Trainer's App users can also follow each other, as well as like and comment each other's workouts!

## Registration and login
New users can register with a _unique_ username. As of now, passwords can be whatever - there are no complexity requirements.


## Move database
Users can add new moves to the database if their desired move is not already added. The database can be queried by providing a search phrase and specifying if the user wants to see only moves they themselves have added.


## User database
Users can inspect the list of all users in the system. If the listed users have specified that others should be allowed to follow their workout activity, the logged in user can choose to follow or unfollow the user in question, based on their current following status.

## Training data
### Adding a new workout
Users can add new workout records by adding moves, reps and used weights individually, or by selecting a workout template and using the data derived from the template. The system will prefill reps and weights for the selected moves if the user has previously logged workouts that include those selected moves.


### Current user's workout history
Users can inspect their own workout history by clicking individual training session links on the Training Data page.


### Followed users' workout history
If the currently logged in user is following other users, and followed users have recorded workouts during the past 7 days in the system, followed users' workout data is displayed on the index page. The logged in user can like and comment individual sessions, and a notification related to each action is displayed to the session owner when they navigate to the index page. Users can also remove likes and comments that they have added.


## User profile
Users can create new workout templates on their profile page. They can also specify if they want other users to be able to follow their workout activity in the system.
