import numpy as np
import pandas as pd
import matplotlib as plt
import random
import copy
import pygame
from scipy.spatial.distance import squareform, pdist
from sklearn.neighbors import DistanceMetric
number_of_cars = 5
car_capacity = 1000
number_of_customers = 30
POPULATION_SIZE = 10000

class Route:
	def __init__(self):
		self.route = []
		self.total_cost = 0
	
	def set_route(self, route):
		self.route = route

	def get_route(self):
		return self.route

	def get_total_cost(self):
		return self.total_cost

	def set_total_cost(self, total_cost):
		self.total_cost = total_cost

	def __lt__(self, other_route):
		return self.get_total_cost() < other_route.get_total_cost()


def evaluate_route(route, distance_matrix, cities_demand):
	cities_list = list(CITIES_DEMAND)
	depot = "Krakow"
	total_cost = 0
	while route:
		capacity = 0
		city = route.pop()
		capacity = cities_demand[city]
		total_cost += distance_matrix[cities_list.index(depot)][cities_list.index(city)]
		while True:
			if route:
				if capacity + cities_demand[route[0]] > 1000:
					break
				next_city = route.pop()
				capacity += cities_demand[next_city]
				total_cost += distance_matrix[cities_list.index(city)][cities_list.index(next_city)]
				city = next_city
			else:
				break
		total_cost += distance_matrix[cities_list.index(city)][cities_list.index(depot)]
	return total_cost


def create_population(cities, population_size):
	population = []
	for i in range(population_size):
		random.shuffle(cities)
		route = Route()
		route.set_route(cities)
		population.append(copy.deepcopy(route))
	return population


def generate_childs(population):
	childs = []
	for i in range(int(POPULATION_SIZE/2)):
		random_routes = random.sample(population, 2)
		parent_first = random_routes[0]
		population.remove(parent_first)
		parent_second = random_routes[1]
		population.remove(parent_second)
		cross_length = random.randint(1, len(parent_first.get_route()) - 1)
		child_first = ['']*len(parent_first.get_route())
		child_second = ['']*len(parent_first.get_route())
		child_first[:cross_length] = parent_second.get_route()[:cross_length]
		child_second[:cross_length] = parent_first.get_route()[:cross_length]
		for city in parent_first.get_route()[cross_length:]:
			if not city in child_first:
				child_first[parent_first.get_route().index(city)] = city 
		for city in parent_first.get_route():
			if not city in child_first:
				child_first[child_first.index('')] = city
		for city in parent_second.get_route()[cross_length:]:
			if not city in child_second:
				child_second[parent_second.get_route().index(city)] = city 
		for city in parent_first.get_route():
			if not city in child_second:
				child_second[child_second.index('')] = city
		childs.append(child_first.copy())
		#print(parent_first.get_route())
		#print(parent_second.get_route())
		#print(cross_length)
		#print(child_first)
		childs.append(child_second.copy())
	return childs

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

evaluate_route(population[0].get_route().copy(), distance_matrix, CITIES_DEMAND)
pygame.init()
display = pygame.display.set_mode((800,600))
for i in range(1):
	childs = generate_childs(copy.deepcopy(population))
	childs_population = []
	for child in childs:
		route = Route()
		route.set_route(child)
		childs_population.append(copy.deepcopy(route))
	population += childs_population
	for result in population:
		result.set_total_cost(evaluate_route(copy.deepcopy(result.get_route()), distance_matrix, CITIES_DEMAND))
	population.sort()
	print(min(population).get_total_cost())
	population = population[:POPULATION_SIZE]
min_lat = min(position['latitude'])
max_lat = max(position['latitude'])
min_long = min(position['longitude'])
max_long = max(position['longitude'])
for i in range(len(CITIES_DEMAND)):
	pos_lat = (position['latitude'][i]-min_lat)/(max_lat-min_lat)*600
	pos_long = (position['longitude'][i]-min_long)/(max_long-min_long)*800
	pygame.draw.circle(display, (255, 255, 255), (pos_long, pos_lat), 4)
route = min(population).get_route()
while route:
	capacity = 0
	main_city = "Krakow"
	main_city_lat = (position['latitude'][30]-min_lat)/(max_lat-min_lat)*600
	main_city_long = (position['longitude'][30]-min_long)/(max_long-min_long)*800
	city = route.pop()
	capacity = CITIES_DEMAND[city]
	city_lat = (position['latitude'][unvisited_cities.index(city)]-min_lat)/(max_lat-min_lat)*600
	city_long = (position['longitude'][unvisited_cities.index(city)]-min_long)/(max_long-min_long)*800
	color = pygame.Color('#' +''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
	pygame.draw.line(display, color, (city_long, city_lat), (main_city_long, main_city_lat),1)
	while True:
		if route:
			if capacity + CITIES_DEMAND[route[0]] > 1000:
				pygame.draw.line(display, color, (city_long, city_lat), (main_city_long, main_city_lat),1)
				break
			next_city = route.pop()
			capacity += CITIES_DEMAND[next_city]
			next_city_lat = (position['latitude'][unvisited_cities.index(next_city)]-min_lat)/(max_lat-min_lat)*600
			next_city_long = (position['longitude'][unvisited_cities.index(next_city)]-min_long)/(max_long-min_long)*800
			pygame.draw.line(display, color, (city_long, city_lat), (next_city_long, next_city_lat),1)
			city = next_city
			city_lat = (position['latitude'][unvisited_cities.index(city)]-min_lat)/(max_lat-min_lat)*600
			city_long = (position['longitude'][unvisited_cities.index(city)]-min_long)/(max_long-min_long)*800
		else:
			break
	color = pygame.Color('#' +''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
pygame.display.update()
input("Press Enter to continue...")

