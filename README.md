# LABMON

Labmon is a monster collector browser game, in which players can collect creatures by attempting captures during unique encounters. The encounter generation and rarity of the encounter is time-based, rewarding the player’s patience with better monsters. Players can earn in-game currency by catching monsters, completing collections, and sharding duplicates.
Our aim with the app is to encourage users to work from their laptop while also taking time to rest from their activities. Less interaction means better rewards in terms of monster rarity, while still having something to look forward to when taking a break.

## Project Setup

Docker (or podman) is required to run this project.

First, change directory to ```source```.

```sh
cd source
```

To run the project.

```sh
docker compose up
```

To connect PGAdmin to the PostgreSQL db, you can use the port number, db name and credentials stated below.

## Listening ports

- **Labmon App:** The webserver is running at http://localhost:5005
- **PGAdmin:** http://localhost:5050
- **DB:** Port: 5432 | Name: db
- **RabbitMQ:** Management interface at http://localhost:15672

## Default Admin Credentials

- **Labmon App:** Username: admin | Password: password
- **PGAdmin:** Username: admin@admin.com | Password: admin
- **PostgreSQL:** Username: user | Password: password
- **RabbitMQ:** Username: user | Password: password
