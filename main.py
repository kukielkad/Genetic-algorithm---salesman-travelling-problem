import numpy as np
import pandas as pd
import matplotlib as plt
import random
import copy
import pygame
from pygame.locals import *
from scipy.spatial.distance import squareform, pdist
from sklearn.neighbors import DistanceMetric
number_of_cars = 5
CAR_CAPACITY = 10000
number_of_customers = 30
POPULATION_SIZE = 1000

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

	def __eq__(self, other_route):
		return self.get_total_cost() == other_route.get_total_cost()

# def evaluate_route(route, distance_matrix, cities_demand):
# 	cities_list = list(CITIES_DEMAND)
# 	depot = "Krakow"
# 	depot_index = cities_list.index(depot)
# 	total_cost = 0
# 	while route:
# 		capacity = 0
# 		city = route.pop()
# 		capacity = cities_demand[city]
# 		city_index = cities_list.index(city)
# 		total_cost += distance_matrix[depot_index][city_index]
# 		while True:
# 			if route:
# 				if capacity + cities_demand[route[0]] > CAR_CAPACITY:
# 					break
# 				next_city = route.pop()
# 				next_city_index = cities_list.index(next_city)
# 				capacity += cities_demand[next_city]
# 				total_cost += distance_matrix[next_city_index][city_index]
# 				city = next_city
# 			else:
# 				break
# 		total_cost += distance_matrix[city_index][depot_index]
# 	return total_cost

def evaluate_route(route, distance_matrix, cities_demand):
	cities_list = list(CITIES_DEMAND)
	depot = "Krakow"
	depot_index = cities_list.index(depot)
	total_cost = 0
	capacity = 0
	city = route.pop()
	capacity = cities_demand[city]
	city_index = cities_list.index(city)
	total_cost += distance_matrix[depot_index][city_index]
	while route:
		next_city = route.pop()
		next_city_index = cities_list.index(next_city)
		capacity += cities_demand[next_city]
		total_cost += distance_matrix[next_city_index][city_index]
		city = next_city
		city_index = cities_list.index(city)
	total_cost += distance_matrix[city_index][depot_index]
	return total_cost

def create_population(cities, population_size):
	population = []
	for i in range(population_size):
		random.shuffle(cities)
		route = Route()
		route.set_route(cities)
		population.append(copy.deepcopy(route))
	return population


def generate_child(parent_first, parent_second):
	cross_first = random.randint(0, len(parent_first.get_route()))
	cross_second = random.randint(0, len(parent_first.get_route()))
	if cross_first > cross_second:
		cross_first, cross_second = cross_second, cross_first
	child = copy.deepcopy(parent_first.get_route())
	for i in range(cross_first, cross_second):
		child[i], child[parent_first.get_route().index(parent_second.get_route()[i])] = child[parent_first.get_route().index(parent_second.get_route()[i])], child[i]
	return copy.deepcopy(child)

def mutate(result):
	mutation_first = random.randint(0, len(result) -1)
	mutation_second = random.randint(0, len(result) -1)
	result[mutation_first], result[mutation_second] = result[mutation_second], result[mutation_first]
	return copy.deepcopy(result)

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
#print(distance_matrix)
#print(distance_matrix[3][30])
unvisited_cities = [city for city in CITIES_DEMAND]
unvisited_cities.remove('Krakow')
total_cost = sum([CITIES_DEMAND[city] for city in CITIES_DEMAND])
random.shuffle(unvisited_cities)
population = create_population(unvisited_cities, POPULATION_SIZE)
for result in population:
	result.set_total_cost(evaluate_route(copy.deepcopy(result.get_route()), distance_matrix, CITIES_DEMAND))
pygame.init()
display = pygame.display.set_mode((800,600))
for i in range(1000):
	new_population = []
	population.sort()
	new_population.append(copy.deepcopy(population[0]))
	for i in range(POPULATION_SIZE -1 ):
		parent_first = min([route for route in random.sample(population, 30)])
		population.remove(parent_first)
		parent_second = min([route for route in random.sample(population, 30)])
		population.append(parent_first)
		child = Route()
		child.set_route(generate_child(parent_first, parent_second))
		if random.random() < 0.9:
			child.set_route(mutate(child.get_route()))
		#print("\n")
		#("Dziecko: " + str(child.get_route()))
		#print("\n")
		child.set_total_cost(evaluate_route(copy.deepcopy(child.get_route()), distance_matrix, CITIES_DEMAND))
		new_population.append(copy.deepcopy(child))
	#new_population.sort()
	#print("\n")
	#for i in new_population:
		#print(str(i.get_total_cost()))
	#print("\n")
	print(min(new_population).get_total_cost())
	population = copy.deepcopy(new_population)

min_lat = min(position['latitude'])
max_lat = max(position['latitude'])
min_long = min(position['longitude'])
max_long = max(position['longitude'])
for i in range(len(CITIES_DEMAND)):
	pos_lat = (position['latitude'][i]-min_lat)/(max_lat-min_lat)*600
	pos_long = (position['longitude'][i]-min_long)/(max_long-min_long)*800
	pygame.draw.circle(display, (255, 255, 255), (pos_long, pos_lat), 4)
route = min(population).get_route()
print(route)
print(evaluate_route(copy.deepcopy(route), distance_matrix, CITIES_DEMAND))
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
			if capacity + CITIES_DEMAND[route[0]] > CAR_CAPACITY:
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
	pygame.draw.line(display, color, (city_long, city_lat), (main_city_long, main_city_lat),1)
	color = pygame.Color('#' +''.join([random.choice('56789ABCDEF') for j in range(6)]))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            break

