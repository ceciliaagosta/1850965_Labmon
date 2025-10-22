# SYSTEM DESCRIPTION:

The project is a browser monster collector game web application. Players can collect creatures by attempting captures during unique encounters. Players can only generate encounters by waiting a minimum amount of time, and rarity of the encountered creature depends on time passed between encounters. To have a better chance at capturing the creatures, players are able to use items. Items can be bought from an in-game shop using an in-game currency. This currency can only be earned by playing the game and “sharding” duplicate creatures, to also encourage the capture of duplicates. Players can view their collection and be awarded with in-game currency for completing one collection. Admins can manage the set of available creatures and items, using a dedicated section of the web app, being able to also create new collections for future longevity. Authentication is managed using JWT tokens, and a distinction exists between the admin and player role, to ensure players cannot cheat the game by accessing parts of the app outside of their boundary. The goal of the system is to be a productivity app, encouraging users to work from their laptop and taking periodic pauses from their activities to interact with the game. Less interaction means better rewards in terms of monster rarity, while still having something to look forward to when taking a break.

# USER STORIES:

1. As a Player, I want to register in the site, so that I can access the system  
2. As a Player, I want to login in the site, so that I can use the system  
3. As a Player, I want to not put my credentials in the site every time a reload the site, so that I can use the site  
4. As a Player, I want to logout, so that no one else can use my account  
5. As a Player, I want to access my account, so that I can edit my personal information  
6. As a Player, I want to access my account, so that I can delete my personal information  
7. As a Player, I want to generate an encounter with a monster, so that I can try to catch it  
8. As a Player, I want to try to catch a monster, so that I can add it to my collection  
9. As a Player, I want to buy items with in-game currency, so that I can use them in an encounter  
10. As a Player, I want to use my items in an encounter, so that I can increase my chances of capturing the monster  
11. As a Player, I want to sell (shard) monsters, so that I can gain in-game currency  
12. As a Player, I want to view my collection of monsters, so that I can track my progress  
13. As a Player, I want to view my inventory, so that I can see what items I own  
14. As a Player, I want to see how much time has passed from the last encounter, so that I can choose the best moment to trigger a rare encounter  
15. As a Player, I want to see which creatures I’m missing in a collection, so that I know what to aim for  
16. As a Player, I want to receive a reward (in-game currency) for completing a collection, so that my effort feels meaningful  
17. As a Player, I want duplicates to be clearly marked in my collection, so that I know what can be safely “sharded”  
18. As a Player, I want the game to track capture statistics, so that I feel motivated to improve  
19. As an Admin, I want to login in the site, so that I can manage the system  
20. As an Admin, I want to not put my credentials in the site every time a reload the site, so that I can use the site  
21. As an Admin, I want to logout, so that no one else can use my account  
22. As an Admin, I want to access my account, so that I can edit my personal information  
23. As an Admin, I want to access my account, so that I can delete my personal information  
24. As an Admin, I want a secure dashboard, so that only authorized admins can manage content  
25. As an Admin, I want to see all users' accounts, so that I can have a clear view of the people in the system  
26. As an Admin, I want to edit users' accounts, so that I can help users in managing their personal information  
27. As an Admin, I want to delete users' accounts, so that I can remove malicious users from the system  
28. As an Admin, I want to create new users, so that I can add new admins or users to the system  
29. As an Admin, I want to access monsters' information, so that I can have a clear view of monsters in the system  
30. As an Admin, I want to edit monsters' information, so that I can better balance the game  
31. As an Admin, I want to delete monsters' information, so that I can remove obsolete creatures from the system  
32. As an Admin, I want to create new monsters, so that I can add more creatures for the players  
33. As an Admin, I want to access items' information, so that I can have a clear view of items in the system  
34. As an Admin, I want to edit items' information, so that I can better balance the game  
35. As an Admin, I want to delete items' information, so that I can remove obsolete items from the system  
36. As an Admin, I want to create new items, so that I can add more items for the players 


# CONTAINERS:

## 1
## CONTAINER_NAME: labmon_auth_api

### DESCRIPTION:
Manages all functionalities related to registration, login, and session persistence for players and administrators. Handles operations related to all users, like viewing personal information and storing profile related data.

### USER STORIES:

1. As a Player, I want to register in the site, so that I can access the system  
2. As a Player, I want to login in the site, so that I can use the system  
3. As a Player, I want to not put my credentials in the site every time a reload the site, so that I can use the site  
4. As a Player, I want to logout, so that no one else can use my account 
5. As a Player, I want to access my account, so that I can edit my personal information  
6. As a Player, I want to access my account, so that I can delete my personal information  
19. As an Admin, I want to login in the site, so that I can manage the system  
20. As an Admin, I want to not put my credentials in the site every time a reload the site, so that I can use the site 
21. As an Admin, I want to logout, so that no one else can use my account 
22. As an Admin, I want to access my account, so that I can edit my personal information  
23. As an Admin, I want to access my account, so that I can delete my personal information  
24. As an Admin, I want a secure dashboard, so that only authorized admins can manage content  
25. As an Admin, I want to see all users' accounts, so that I can have a clear view of the people in the system  
26. As an Admin, I want to edit users' accounts, so that I can help users in managing their personal information  
27. As an Admin, I want to delete users' accounts, so that I can remove malicious users from the system  
28. As an Admin, I want to create new users, so that I can add new admins or users to the system  

### PORTS: 
"5001:5000"

### DESCRIPTION:
The Authentication container is responsible for managing all the security-related functionalities that involve registration, login, and session persistence. It also handles operations related to the management of user profiles on the platform.

### PERSISTANCE EVALUATION
The Authentication API requires persistent storage to manage registered users and their credentials.
It stores information such as usernames, encrypted passwords, and roles (player/admin) inside the PostgreSQL database.
While JWT tokens themselves are stateless, the system depends on the database for user verification and management.

### EXTERNAL SERVICES CONNECTIONS
The Authentication container does not connect to external services.

### MICROSERVICES:

#### MICROSERVICE: auth_api
- TYPE: backend
- DESCRIPTION: Manages the creation and verification of tokens. Handles the creation, viewing, and updating of personal information for clients. It also enables administrators to view and retrieve detailed user profiles to analyze platform activity and manage user data.
- PORTS: 5001
- TECHNOLOGICAL SPECIFICATION:
The microservice is developed in Python and uses Flask, a lightweight Python web framework.
It uses the following libraries and technologies:
    - JWT (PyJWT): The microservice handles JSON Web Tokens (JWT), commonly used for secure token-based authentication.
    - Flask-Bcrypt and bcrypt: These packages are used for secure encryption and cryptographic operations.
    - Flask-SQLAlchemy  and SQLAlchemy : Provide ORM-based interaction with the PostgreSQL database.
    - pika : Used to communicate with RabbitMQ message broker for asynchronous events

- SERVICE ARCHITECTURE:
    - A main controller manages routes, request handling, and responses, implementing the authentication and authorization logic.
    - A models directory defines the SQLAlchemy classes representing users, roles, and tokens.
    - A utilities module provides helper functions for password hashing and JWT generation/verification. Also RabbitMQ credentials.
    - A config module stores database connection parameters and environment variables.
    - The service interacts with a PostgreSQL database for user persistence and exposes endpoints for login, registration, logout, and token validation.

- ENDPOINTS:
	| HTTP METHOD | URL | Description | User Stories |
	| ----------- | --- | ----------- | ------------ |
    | POST | /users/register | Create and add a new user to db. Creates and sends out a JWT token | 1, 3, 21 |
    | POST | /users/login | Verifies encrypted password and creates and sends out a JWT token | 2, 20, 25|
    | GET | /users | Returns all the users in the database, that can be done only by the admin | 25, 26 |
    | POST | /users | Inserts a new user in the database | 29 |
    | GET | /users/{id} | Returns the user information | 5, 21, 23 |
    | PUT | /users/{id} | Edits user information | 5, 21, 23 |
    | DELETE | /users/{id} | Deletes the user | 6, 24, 28 |

- DB STRUCTURE:
    **_User_** :	| **_id_** | name | email | password | role |


## 2
## CONTAINER_NAME: labmon_monsters_api

### DESCRIPTION:
Manages monsters’ data and collections. It handles monster creation, modification, and deletion for admins only and retrieves monster data for players.

### USER STORIES:

29. As an Admin, I want to access monsters' information, so that I can have a clear view of monsters in the system  
30. As an Admin, I want to edit monsters' information, so that I can better balance the game  
31. As an Admin, I want to delete monsters' information, so that I can remove obsolete creatures from the system  
32. As an Admin, I want to create new monsters, so that I can add more creatures for the players  

### PORTS: 
"5002:5000"

### DESCRIPTION:
The  container is designed to manage all operations related to monsters. The container provides essential capabilities for the site administrator that include adding, modifying, or deleting monsters, as well as retrieving monsters' details both for admin and players.

### PERSISTANCE EVALUATION
The  container requires persistent storage to manage the monster information effectively. This container depends on a database of monsters that includes details like monster name, rarity, catch rate, collection and sprite.

### EXTERNAL SERVICES CONNECTIONS
The Monster container does not connect to external services.

### MICROSERVICES:

#### MICROSERVICE: monsters_api
- TYPE: backend
- DESCRIPTION: Manages all backend functionalities such as adding, modifying, and removing monsters from the collection. 
- PORTS: 5002
- TECHNOLOGICAL SPECIFICATION:
The microservice is developed in Python 3, using Flask (3.0.3) as the main web framework.
It manages all backend operations related to monsters. 
The service allows both administrators and players to interact with the monster database — admins can create, edit, or delete monsters, while players can view locked collections.
It integrates with PostgreSQL for persistent data storage and uses RabbitMQ for inter-service communication.
Key components and libraries used: 
   - Flask-Cors : Enables communication between frontend clients and backend APIs across origins.
   - Flask-Cors (5.0.0): Enables communication between frontend clients and backend APIs across origins.
   - Flask-SQLAlchemy and SQLAlchemy : ORM layer for interacting with the PostgreSQL database.
   - pika : Integrates the service with RabbitMQ for asynchronous communication.
   - PyJWT : Used for verifying player and admin tokens when accessing protected endpoints, only admins can add, edit, or delete monsters

- SERVICE ARCHITECTURE:
   - A main controller manages routes for CRUD operations on monsters, enabling admins to create, update, and delete monster data.
   - A models directory defines SQLAlchemy classes representing monsters and their attributes.
   - A utilities module provides helper functions for data validation and integrity checks.
   - A config module stores database configuration parameters and environment variables.
   - The service connects to a PostgreSQL database for monster data persistence and interacts with the Game API to synchronize available creatures used during encounters.

- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
	| ----------- | --- | ----------- | ------------ |
    | GET | /monsters | Returns all the monsters in the database |  30 |
    | POST | /monsters | Inserts a new monster in the database | 33 |
    | GET | /monsters/{id} | Returns the monster's information | 30 |
    | PUT | /monsters/{id} | Edits the monster's information | 31 |
    | DELETE | /monsters/{id} | Deletes the monster's information | 32 |

- DB STRUCTURE:
    **_Monster_** :	| **_id_** | name | rarity | catch_rate | collection_n | sprite |


## 3
## CONTAINER_NAME: labmon_items_api

### DESCRIPTION:
Manages items’ data and inventory. It handles item creation, modification, and deletion for admins only and retrieves item data for players.

### USER STORIES:

33. As an Admin, I want to access items' information, so that I can have a clear view of items in the system  
34. As an Admin, I want to edit items' information, so that I can better balance the game  
35. As an Admin, I want to delete items' information, so that I can remove obsolete items from the system  
36. As an Admin, I want to create new items, so that I can add more items for the players 

### PORTS: 
"5003:5000"

### DESCRIPTION:
The  container is designed to manage all operations related to items. The container provides essential capabilities for the site administrator that include adding, modifying, or deleting items, as well as retrieving items details both for admin and players.

### PERSISTANCE EVALUATION
The  container requires persistent storage to manage the item information effectively. This container depends on a database of item that includes details like item name, price, description, effect and sprite.

### EXTERNAL SERVICES CONNECTIONS
The Item container does not connect to external services.

### MICROSERVICES:

#### MICROSERVICE: items_api
- TYPE: backend
- DESCRIPTION: Manages all backend functionalities such as adding, modifying, and removing items from the collection. 
- PORTS: 5003
- TECHNOLOGICAL SPECIFICATION:
The microservice is developed in Python 3, using Flask (3.0.3) as the main web framework.
It manages all backend operations related to items.
The service allows both administrators and players to interact with the item database — admins can create, edit, or delete items, while players can only view what they have bougth.
It integrates with PostgreSQL for persistent data storage and uses RabbitMQ for inter-service communication.
Key components and libraries used: 
   - Flask-Cors : Enables communication between frontend clients and backend APIs across origins.
   - Flask-Cors (5.0.0): Enables communication between frontend clients and backend APIs across origins.
   - Flask-SQLAlchemy and SQLAlchemy : ORM layer for interacting with the PostgreSQL database.
   - pika : Integrates the service with RabbitMQ for asynchronous communication.
   - PyJWT : Used for verifying player and admin tokens when accessing protected endpoints, infact only admin can edit or delete items

- SERVICE ARCHITECTURE:
   - A main controller manages routes for CRUD operations on items, handling both admin and player requests.
   - A models directory defines SQLAlchemy entities representing in-game items and their properties.
   - A utilities module includes helper functions for data validation and business logic related to item bonuses.
   - A config module contains environment and database settings.
   - The service connects to a PostgreSQL database for item persistence and communicates with the Game API to synchronize item effects during encounters.

- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
	| ----------- | --- | ----------- | ------------ |
    | GET | /items | Returns all the items in the database | 12, 15, 30 |
    | POST | /items | Inserts a new item in the database | 33 |
    | GET | /items/{id} | Returns the item's information | 30 |
    | PUT | /items/{id} | Edits the item's information | 31 |
    | DELETE | /items/{id} | Deletes the item's information | 32 |

- DB STRUCTURE:
    **_Item_** :	| **_id_** | name | price | description | effect | sprite |


## 4
## CONTAINER_NAME: labmon_game_api

### DESCRIPTION:
The Game API microservice is responsible for orchestrating the core gameplay dynamics of the system.
It manages the generation of encounters based on the elapsed time since the previous one, using rarity calculation algorithms that determine the likelihood of finding rare monsters.
During encounters, the service handles monster capture attempts, taking into account item bonuses to modify the probability of success.
When a player decides to “shard” or sell duplicate monsters, the Game API processes this logic and rewards the player with in-game currency accordingly.

## USER STORIES
7. As a Player, I want to generate an encounter with a monster, so that I can try to catch it  
8. As a Player, I want to try to catch a monster, so that I can add it to my collection  
9. As a Player, I want to buy items with in-game currency, so that I can use them in an encounter  
10. As a Player, I want to use my items in an encounter, so that I can increase my chances of capturing the monster  
11. As a Player, I want to sell (shard) monsters, so that I can gain in-game currency  
12. As a Player, I want to view my collection of monsters, so that I can track my progress  
13. As a Player, I want to view my inventory, so that I can see what items I own 
14. As a Player, I want to see how much time has passed from the last encounter, so that I can choose the best moment to trigger a rare encounter  
15. As a Player, I want to see which creatures I’m missing in a collection, so that I know what to aim for
16. As a Player, I want to receive a reward (in-game currency) for completing a collection, so that my effort feels meaningful  
17. As a Player, I want duplicates to be clearly marked in my collection, so that I know what can be safely “sharded” 

### PORTS: 
"5004:5000"

### DESCRIPTION:
The Game API is the microservice responsible for managing core gameplay mechanics. It handles monster encounter generation based on elapsed time and rarity probabilities, oversees capture attempts including item bonuses, and processes the selling or “sharding” of duplicate monsters with corresponding in-game rewards. It evaluates collection progress, and grants rewards in real time. The service publishes gameplay events to RabbitMQ for asynchronous updates and verifies user identity and permissions via JWT through the Authentication API.

### PERSISTANCE EVALUATION
The container depends on a database to manage players, monsters, items and encounters effectively. 

### EXTERNAL SERVICES CONNECTIONS
The Game container does not connect to external services.

### MICROSERVICES:

#### MICROSERVICE: game_api
- TYPE: backend
- DESCRIPTION: Manages all backend functionalities for managing an encouter and sharding monsters.
- PORTS: 5003
- TECHNOLOGICAL SPECIFICATION:
The microservice is developed in Python 3, using Flask (3.0.3) as the main web framework.
It manages all backend operations related to game logic.
It integrates with PostgreSQL for persistent data storage and uses RabbitMQ for inter-service communication.
Key components and libraries used: 
   - Flask-Cors : Enables communication between frontend clients and backend APIs across origins.
   - Flask-Cors (5.0.0): Enables communication between frontend clients and backend APIs across origins.
   - Flask-SQLAlchemy and SQLAlchemy : ORM layer for interacting with the PostgreSQL database.
   - pika : Integrates the service with RabbitMQ for asynchronous communication.
   - PyJWT : Used for verifying player and admin tokens when accessing protected endpoints, infact only admin can edit or delete items

- SERVICE ARCHITECTURE:
   - A main controller defines the routes that handle gameplay operations such as encounters, captures, and monster sharding.
   - A models directory contains SQLAlchemy classes representing monsters, encounters, collections.
   - A utilities module provides helper functions for rarity calculation, capture probability, and RabbitMQ event publishing.
   - A config module manages database configurations.
   - The service interacts with the Authentication API for JWT validation, communicates asynchronously via RabbitMQ, and stores gameplay data in a PostgreSQL database.

- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
	| ----------- | --- | ----------- | ------------ |
    | GET | /game/encounters | Returns all the encounters in the database |  |
    | POST | /game/encounters | Create a new encounter in the database | 7 |
    | GET | /game/encounters/{encounter_id} | Returns the encounter informations |  |
    | DELETE | /game/encounters/{encounter_id} | Deletes the encounter's information if the player runs away|  |
    | POST | /game/encounters/{encounter_id}/catch | Tries to catch a monster in an encounter | 8 |
    | POST | /game/timer | Signal start of timer for encounter generation | 14 |
    | GET | /game/collection | Returns player's collection | 12, 15 |
    | PUT | /game/collection/{monster_id}/shard | Shards a monster | 11 |
    | POST | /game/collection/claim | Claims a reward when a collection is completed | 16 |



- DB STRUCTURE:
    **_Encounter_** :	| **_id_** | player_id | monster_id | isCaught | timestamp |
    **_Player_** :	| **_player_id_** | currency | timestamp | lastEncounter_id | collectionCompleted |
    **_Collection_** :	| **_player_id_** | **_monster_id_** | quantity |
    **_Inventory_** :	| **_player_id_** | **_item_id_** | quantity |
    **_MonsterStats_** :	| **_id_** | rarity | catch_rate | collection_n |
    **_ItemStats_** :	| **_id_** | price | effect | 

## 5
## CONTAINER_NAME: labmon_app

### DESCRIPTION: 
Provides the User Interface for the whole Labmon game.

### USER-STORIES:

### PORTS: 
5005:5000

### DESCRIPTION:
The labmon_app container serves a frontend for the game.

### PERSISTANCE EVALUATION
The labmon_app container does not include a database.

### EXTERNAL SERVICES CONNECTIONS
The labmon_app container does not connect to external services.

### MICROSERVICES:

#### MICROSERVICE: labmon_app
- TYPE: frontend
- DESCRIPTION: This microservice serves the main user interface for the game.
- PORTS: 5005
 

## 6
## CONTAINER_NAME: labmon_statistics_api

## USER STORIES
18. As a Player, I want the game to track capture statistics, so that I feel motivated to improve  

    











