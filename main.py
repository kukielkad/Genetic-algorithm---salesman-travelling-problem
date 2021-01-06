import numpy as np
import pandas as pd
import matplotlib as plt
import random
from scipy.spatial.distance import squareform, pdist
from sklearn.neighbors import DistanceMetric
number_of_cars = 5
car_capacity = 1000
number_of_customers = 30
POPULATION_SIZE = 2

def create_population(cities, population_size):
	population = []
	for i in range(population_size):
		random.shuffle(cities)
		population.append(cities.copy())
	return population

def evaluate_route(route, distance_matrix, cities_demand):
	cities_list = list(CITIES_DEMAND)
	depot = "Krakow"
	total_cost = 0
	while route:
		capacity = 0
		city = route.pop()
		capacity = cities_demand[city]
		total_cost += distance_matrix[cities_list.index(depot)][cities_list.index(city)]
		print(route)
		while True:
			if route:
				if capacity + cities_demand[route[0]] > 1000:
					break
				next_city = route.pop()
				capacity += cities_demand[next_city]
				total_cost += distance_matrix[cities_list.index(city)][cities_list.index(next_city)]
			else:
				break
		total_cost += distance_matrix[cities_list.index(city)][cities_list.index(depot)]
	print(total_cost)
def generate_childs(population):
	random_routes = random.sample(population, 2)
	parent_first = random_routes[0]
	parent_second = random_routes[1]
	cross_length = random.randint(0, len(parent_first))
	print(cross_length)
	child_first = ['']*len(parent_first)
	child_second = ['']*len(parent_first)
	child_first[:cross_length] = parent_second[:cross_length]
	child_second[:cross_length] = parent_first[:cross_length]
	print(parent_first)
	print(parent_second)
	for city in parent_first[cross_length:]:
		if not city in child_first:
			child_first[parent_first.index(city)] = city 
	for city in parent_first:
		if not city in child_first:
			child_first[child_first.index('')] = city
	print(child_first)
	for city in parent_second[cross_length:]:
		if not city in child_second:
			child_second[parent_second.index(city)] = city 
	for city in parent_first:
		if not city in child_second:
			child_second[child_second.index('')] = city
	print(child_second)


CITIES_DEMAND = {"Bialystok":500,"Bielsko_Biala":50,"Chrzanow":400,"Gdansk":200,"Gdynia":100,"Gliwice":40,
"Gromnik":200,"Katowice":300,"Kielce":30,"Krosno":60,"Krynica":50,"Lublin":60,"Lodz":160,"Malbork":100,"Nowy_Targ":120,
"Olsztyn":300,"Poznan":100,"Pulawy":200,"Radom":100,"Rzeszow":60,"Sandomierz":200,
"Szczecin":150,"Szczucin":60,"Szklarska_Poreba":50,"Tarnow":70,"Warszawa":200,
"Wieliczka":90,"Wroclaw":40,"Zakopane":200,"Zamosc":300, "Krakow":0}
position = pd.read_csv('data.csv',sep=';',encoding= 'unicode_escape')
#choose distance metrics
dist = DistanceMetric.get_metric('haversine')
#convert degrees to radian
position['latitude']=np.radians(position['latitude'])
position['longitude']=np.radians(position['longitude'])
#make distance matrix
distance_matrix = dist.pairwise(position[['latitude','longitude']].to_numpy())*6373
print(distance_matrix)
unvisited_cities = [city for city in CITIES_DEMAND]
unvisited_cities.remove('Krakow')
total_cost = sum([CITIES_DEMAND[city] for city in CITIES_DEMAND])
random.shuffle(unvisited_cities)
population = create_population(unvisited_cities, POPULATION_SIZE)
print(population)
print(list(CITIES_DEMAND).index("Krakow"))
evaluate_route(population[0].copy(), distance_matrix, CITIES_DEMAND)
generate_childs(population)