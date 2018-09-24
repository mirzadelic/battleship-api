# Battleship API


## Run:
```
virtualenv venv
pip3 install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API urls
`http://localhost:8000/api/game/game/`

>POST - start new game
>GET - list of all games

POST data:
```json
 {
	"name": "Game 1" // optional
 }
```

GET:
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
`http://localhost:8000/api/game/game/{id}/attack/` - {id} = game id

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
	"hit": false, // if ship has been hit
	"finished_game": false // if all ships has been hit, game finished
 }
```
---
