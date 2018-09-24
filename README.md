# Battleship API

## Requirements for project:
 - `python3` and `virtualenv`

 or

 - `docker`


## Run

`python3` and `virtualenv`:
```sh
virtualenv venv
source venv/bin/activate
cd battleship-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Or use `docker`:
```sh
cd battleship-api
docker build -t battleship-api .
docker run -t -i -p 8000:8000 battleship-api
```


## API urls
`http://localhost:8000/api/game/game/`

>POST - start new game

Data:
```json
 {
	"name": "Game 1"
 }
```
 - name is optional.

>GET - list of all games

Response:
```json
{
	"id": 1,
	"name": "Game 1",
	"created_at": "2018-09-24T11:31:16",
	"finished_game": false,
	"attacks": [
		{
			"x":  1,
			"y":  10,
			"hit":  false
		}
	]
},
```
---
`http://localhost:8000/api/game/game/{id}/attack/` - {id} is game id

>POST - new attack on field

POST data:
```json
 {
	"x": 5,
	"y": 6
 }
```

Returns:
```json
 {
	"x": 5,
	"y": 6,
	"hit": false,
	"finished_game": false
 }
```


 - `hit` - if ship has been hit or not
 - `finished_game` - if all ships has been hit, game finished
---


### Tests
```sh
python manage.py test
```

Also, there is integration with CircleCI:
https://circleci.com/gh/mirzadelic/battleship-api
