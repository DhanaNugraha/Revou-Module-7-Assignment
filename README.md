uv python pin 3.11.11
uv init
uv add flask

close terminal and open again
wait for venv popup
if no popup repeat

to run normally
uv run python main.py

to run flask
uv run -- flask --app main run --debug --reload -p 3000    this works or
uv run -- flask --app main run --debug --reload --port 3000 

keep changing port to mitigate error

when pulling do:
uv add flask

<!--  -->
next version:
uv python pin 3.11.11
uv init
uv add flask
uv add taskipy
(folder management follow this file)

close terminal and open again
wait for venv popup
if no popup repeat

add in bottom of toml
[tool.taskipy.tasks]
fr = "flask --app main run --port 3000 --debug --reload"

use   uv run task fr   to run file


BEFORE YOU START CODING: 
1. make a dummy db with correct format
2. before making each method make sure what format goes in and out
3. dont forget to make code for when data is wrong, unavailable, or already present in db
4. coding flow : db -> main -> router -> view -> repo

delete is 204
get is 200
not found is 404
input not complete is 400
post is 201
failed login 401


<!-- 
uv run main.py
flask --app main run
flask --app main run --debug --reload (to test in) -->




