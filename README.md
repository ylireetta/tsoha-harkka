# How to run
The app cannot be used in production as of now, so please follow these instructions to test:
1. Clone this repository to your computer and navigate to the project root directory.
2. Create a file called ```.env``` with the following contents:
```
DATABASE_URL=<local-address-for-database>
SECRET_KEY=<secret-key-for-app>
```
3. Run the following commands to activate the virtual environment and install requirements:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
4. Run the following command to define the database schema:
```
psql < schema.sql
```
5. Run the following command to start the app:
```
flask run
```
6. Navigate to the url shown on the command line to use the app.

# TSOHA Trainer's App
The main point of TSOHA Trainer's App is to enable users to keep record of their workouts. They can also add new moves to the database if their desired move has yet to be added by someone else. Existing moves can be used to create training templates, which, in turn, can be used to quickly add predefined moves to a new workout session.

No web application is complete without some sort of social aspect, so TSOHA Trainer's App users can also follow each other, as well as like and comment each other's workouts!

## Registration and login
New users can register with a _unique_ username. As of now, passwords can be whatever - there are no complexity requirements. If the selected username is already taken, or the two password fields do not match, the system informs the user about the problem. If the registration is successful, the new user is logged in automatically and redirected to the index page.

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/usernametaken.png "Username taken")
![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/passworderror.png "Password fields mismatch")
![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/registrationsuccess.png "Registered successfully")


## Move database
Users can add new moves to the database if their desired move is not already added (i.e. move names need to be unique). The database can be queried by providing a search phrase and specifying if the user wants to see only moves they themselves have added. When a move is "deleted" from the system, the name can be used again when adding a new move.

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/7fa2aa56bd6716d9639f194cc7f1a9fa780aba8f/documentation/movenametaken.png "Move name already taken")
![alt text](https://github.com/ylireetta/tsoha-harkka/blob/7fa2aa56bd6716d9639f194cc7f1a9fa780aba8f/documentation/newmoveadded.png "New move added")
<hr>

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/7fa2aa56bd6716d9639f194cc7f1a9fa780aba8f/documentation/moveslibrary.png "Moves library")


## User database
Users can inspect the list of all users in the system. If the listed users have specified that others should be allowed to follow their workout activity, the logged in user can choose to follow or unfollow the user in question, based on their current following status.

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/usertable.png "User database")

## User profile
Users can create new workout templates on their profile page. They can also specify if they want other users to be able to follow their workout activity in the system.

### Training templates
Users can create training templates on their profile page. At least one move from the moves database must be selected, and the number of sets per each selected move can be further defined, if necessary. The default number of sets per move is one.

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/userstemplates.png "Existing templates")
<hr>

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/createnewtemplate.png "Creating a new template")

## Training data
### Adding a new workout
Users can add new workout records by adding moves, reps and used weights individually, or by selecting a workout template and using the data derived from the template. If the template includes multiple sets of the same move, a new table row for each set is added to the training data table. The system will prefill reps and weights for the selected moves if the user has previously logged workouts that include those selected moves.

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/createnewsession.png "Adding a new training session")


### Current user's workout history
Users can inspect their own workout history by clicking individual training session links on the Training Data page.


### Followed users' workout history
If the currently logged in user is following other users, and followed users have recorded workouts in the system, followed users' workout data is displayed on the index page. The workout data can be filtered by creation date. The logged in user can like and comment individual sessions, and a notification related to each action is shown to the session owner when they navigate to the index page. Users can also remove likes and comments that they have added.

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/filteredfollowing.png "Filtered workout sessions by followed users")
<hr>

![alt text](https://github.com/ylireetta/tsoha-harkka/blob/693c8d6d84d331965a57c9d21f81a3289d3e8d05/documentation/trainingsessioncomment.png "Individual training session page where the current user has liked and commented")
