ciudad('Los Angeles').
ciudad('Sidney').
ciudad('Roma').
ciudad('Pekin').
ciudad('Buenos Aires').
ciudad('San Francisco').
ciudad('Toronto').
ciudad('Moscu').
ciudad('Madrid').
ciudad('Rio de Janeiro').
ciudad('Berlin').
ciudad('Nueva York').
ciudad('Londres').
ciudad('Tokio').
ciudad('Paris').
ciudad('Ciudad de Mexico').
ciudad('Amsterdam').
ciudad('Singapur').
ciudad('Estambul').
ciudad('Dubai').
ciudad('El Cairo').
ciudad('Delhi').
ciudad('Bangkok').
ciudad('Seul').
ciudad('Ciudad del Cabo').
ciudad('Chicago').
ciudad('Miami').
ciudad('Vancouver').
ciudad('Helsinki').
ciudad('Barcelona').
ciudad('Estocolmo').
ciudad('Ciudad de Panama').
ciudad('Praga').
ciudad('Johannesburgo').
ciudad('San Paulo').
ciudad('Montreal').
ciudad('Budapest').
ciudad('Casablanca').
ciudad('Lima').
ciudad('Oslo').
ciudad('Atenas').
ciudad('Varsovia').
ciudad('San Petersburgo').
ciudad('Viena').
ciudad('Mumbai').
ciudad('Bogota').
ciudad('Copenhague').
ciudad('Nairobi').
ciudad('Edimburgo').
ciudad('Quebec').
ciudad('Zagreb').
ciudad('Ciudad del Vaticano').
ciudad('Denver').
ciudad('Bariloche').

ciudad_con_ciudad('Nueva York').
ciudad_con_ciudad('Londres').
ciudad_con_ciudad('Tokio').
ciudad_con_ciudad('Paris').
ciudad_con_ciudad('Ciudad de Mexico').
ciudad_con_ciudad('Los Angeles').
ciudad_con_ciudad('Sidney').
ciudad_con_ciudad('Roma').
ciudad_con_ciudad('Pekin').
ciudad_con_ciudad('Buenos Aires').
ciudad_con_ciudad('San Francisco').
ciudad_con_ciudad('Toronto').
ciudad_con_ciudad('Moscu').
ciudad_con_ciudad('Madrid').
ciudad_con_ciudad('Rio de Janeiro').
ciudad_con_ciudad('Berlin').
ciudad_con_ciudad('Amsterdam').
ciudad_con_ciudad('Singapur').
ciudad_con_ciudad('Estambul').
ciudad_con_ciudad('El Cairo').
ciudad_con_ciudad('Delhi').
ciudad_con_ciudad('Bangkok').
ciudad_con_ciudad('Seul').
ciudad_con_ciudad('Ciudad del Cabo').
ciudad_con_ciudad('Chicago').
ciudad_con_ciudad('Miami').
ciudad_con_ciudad('Vancouver').
ciudad_con_ciudad('Helsinki').
ciudad_con_ciudad('Barcelona').
ciudad_con_ciudad('Estocolmo').
ciudad_con_ciudad('Ciudad de Panama').
ciudad_con_ciudad('Praga').
ciudad_con_ciudad('Johannesburgo').
ciudad_con_ciudad('Amsterdam').
ciudad_con_ciudad('San Pablo').
ciudad_con_ciudad('Montreal').
ciudad_con_ciudad('Dubai').
ciudad_con_ciudad('Budapest').
ciudad_con_ciudad('Casablanca').
ciudad_con_ciudad('Lima').
ciudad_con_ciudad('Oslo').
ciudad_con_ciudad('Atenas').
ciudad_con_ciudad('Varsovia').
ciudad_con_ciudad('San Petersburgo').
ciudad_con_ciudad('Viena').
ciudad_con_ciudad('Mumbai').
ciudad_con_ciudad('Bogota').
ciudad_con_ciudad('Copenhague').
ciudad_con_ciudad('Nairobi').
ciudad_con_ciudad('Edimburgo').
ciudad_con_ciudad('Quebec').
ciudad_con_ciudad('Zagreb').
ciudad_con_ciudad('Ciudad del Vaticano').
ciudad_con_ciudad('Denver').

ciudad_con_playa('Ciudad del Cabo').
ciudad_con_playa('Miami').
ciudad_con_playa('Barcelona').
ciudad_con_playa('Rio de Janeiro').
ciudad_con_playa('Sidney').
ciudad_con_playa('Los Angeles').

ciudad_con_nieve('Tokio').
ciudad_con_nieve('Moscu').
ciudad_con_nieve('Estocolmo').
ciudad_con_nieve('Praga').
ciudad_con_nieve('Oslo').
ciudad_con_nieve('Varsovia').
ciudad_con_nieve('San Petersburgo').
ciudad_con_nieve('Helsinki').
ciudad_con_nieve('Copenhague').
ciudad_con_nieve('Edimburgo').
ciudad_con_nieve('Denver').
ciudad_con_nieve('Bariloche').

ciudad_con_montana('Denver').
ciudad_con_montana('Tokio').
ciudad_con_montana('Lima').
ciudad_con_montana('Bariloche').

ciudad_cerca('Londres','Paris').
ciudad_cerca('Paris','Roma').
ciudad_cerca('Rio de Janeiro','San Pablo').
ciudad_cerca('Berlin','Paris').
ciudad_cerca('Madrid','Paris').
ciudad_cerca('Amsterdam','Berlin').
ciudad_cerca('Amsterdam','Paris').
ciudad_cerca('Chicago','Nueva York').
ciudad_cerca('Helsinki','Estocolmo').
ciudad_cerca('Praga','Berlin').
ciudad_cerca('Praga','Varsovia').
ciudad_cerca('Barcelona','Madrid').
ciudad_cerca('Johannesburgo','Ciudad del Cabo').
ciudad_cerca('Montreal','Toronto').
ciudad_cerca('Casablanca','Madrid').
ciudad_cerca('Oslo','Helsinki').
ciudad_cerca('Oslo','Estocolmo').
ciudad_cerca('Viena','Praga').
ciudad_cerca('Viena','Budapest').
ciudad_cerca('Praga','Budapest').
ciudad_cerca('Viena','Berlin').
ciudad_cerca('Berlin','Varsovia').
ciudad_cerca('Berlin','Copenhague').
ciudad_cerca('Bogota','Lima').
ciudad_cerca('Edimburgo','Londres').
ciudad_cerca('Quebec','Montreal').
ciudad_cerca('Quebec','Toronto').
ciudad_cerca('Zagreb','Viena').
ciudad_cerca('Ciudad del Vaticano','Roma').

ciudades_cercanas(X, Y) :- ciudad_cerca(X, Y); ciudad_cerca(Y, X).
ciudades_con_ciudad(X) :- ciudad_con_ciudad(X).
ciudades_con_playa(X) :- ciudad_con_playa(X).
ciudades_con_nieve(X) :- ciudad_con_nieve(X).
ciudades_con_montana(X) :- ciudad_con_montana(X).