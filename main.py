import os
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
CAR_CAPACITY = 1000
number_of_customers = 30
POPULATION_SIZE = int(input("Population size: "))
ITERATION_COUNT = int(input("Iteration count: "))
MUTATION_PROBABILITY = float(input("Mutation probability (0, 1): "))
TOURNAMENT_SIZE = int(input("Group size for tournament selection: "))
ELITISM = int(input("Parents quantity in new generation: "))
SHAKE_AFTER = int(input("Shake population every ??? iterations (0 to disable shaking): "))
COLORS = ["#BD202D", "#00A14B", "#3B96D1", "#F16521", "#9F6EAF"]

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

def evaluate_route(route, distance_matrix, cities_demand):
	#print(route)
	cities_list = list(CITIES_DEMAND)
	depot = "Krakow"
	depot_index = cities_list.index(depot)
	total_cost = 0
	while route:
		capacity = 0
		city = route.pop()
		capacity = cities_demand[city]
		city_index = cities_list.index(city)
		total_cost += distance_matrix[depot_index][city_index]
		while True:
			if route:
				if capacity + cities_demand[route[-1]] > CAR_CAPACITY:
					break
				next_city = route.pop()
				next_city_index = cities_list.index(next_city)
				capacity += cities_demand[next_city]
				total_cost += distance_matrix[next_city_index][city_index]
				city = next_city
				city_index = cities_list.index(city)
			else:
				break
		total_cost += distance_matrix[city_index][depot_index]
	return total_cost

# def evaluate_route(route, distance_matrix, cities_demand):
# 	cities_list = list(CITIES_DEMAND)
# 	depot = "Krakow"
# 	depot_index = cities_list.index(depot)
# 	total_cost = 0
# 	capacity = 0
# 	city = route.pop()
# 	capacity = cities_demand[city]
# 	city_index = cities_list.index(city)
# 	total_cost += distance_matrix[depot_index][city_index]
# 	while route:
# 		next_city = route.pop()
# 		next_city_index = cities_list.index(next_city)
# 		capacity += cities_demand[next_city]
# 		total_cost += distance_matrix[next_city_index][city_index]
# 		city = next_city
# 		city_index = cities_list.index(city)
# 	total_cost += distance_matrix[city_index][depot_index]
# 	return total_cost

def create_population(cities, population_size):
	population = []
	for i in range(population_size):
		random.shuffle(cities)
		route = Route()
		route.set_route(cities)
		population.append(copy.deepcopy(route))
	return population


def generate_child(parent_first, parent_second):
	child = []
	cross_first = random.randint(0, len(parent_first.get_route()))
	cross_second = random.randint(0, len(parent_first.get_route()))
	for x in range(0,len(parent_first.get_route())):
		child.append(None)

	if cross_first > cross_second:
		cross_first, cross_second = cross_second, cross_first

	# child = copy.deepcopy(parent_first.get_route())	
	# for i in range(cross_first, cross_second):
	# 	child[i], child[parent_first.get_route().index(parent_second.get_route()[i])] = child[parent_first.get_route().index(parent_second.get_route()[i])], child[i]
	for i in range(cross_first,cross_second):
		child[i] = parent_first.get_route()[i]

	for i in range(len(parent_second.get_route())):
		if not parent_second.get_route()[i] in child:
			child[child.index(None)] = parent_second.get_route()[i]
	return copy.deepcopy(child)

def mutate(result):
	mutation_first = random.randint(0, len(result) -1)
	mutation_second = random.randint(0, len(result) -1)
	result[mutation_first], result[mutation_second] = result[mutation_second], result[mutation_first]
	return copy.deepcopy(result)


os.system("cls")
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
border_position = pd.read_csv('border.csv',sep=',',encoding= 'unicode_escape')
#choose distance metrics
dist = DistanceMetric.get_metric('haversine')
#convert degrees to radian
border_position['latitude']=np.radians(border_position['latitude'])
border_position['longitude']=np.radians(border_position['longitude'])
#make distance matrix
print(border_position)
#print(distance_matrix)
#print(distance_matrix[3][30])
unvisited_cities = [city for city in CITIES_DEMAND]
unvisited_cities.remove('Krakow')
total_cost = sum([CITIES_DEMAND[city] for city in CITIES_DEMAND])
population = create_population(copy.deepcopy(unvisited_cities), POPULATION_SIZE)
best_route = Route()
best_route.set_total_cost(float("inf"))
pygame.init()
display = pygame.display.set_mode((800,800))
for result in population:
	result.set_total_cost(evaluate_route(copy.deepcopy(result.get_route()), distance_matrix, CITIES_DEMAND))
for i in range(ITERATION_COUNT):
	new_population = []
	population.sort()
	for i in range(ELITISM):
	 	new_population.append(copy.deepcopy(population[i]))
	for j in range(POPULATION_SIZE - ELITISM):
		#print("Iteracja: " + str(i))
		parent_first = min([route for route in random.sample(population, TOURNAMENT_SIZE)])
		parent_second = min([route for route in random.sample(population, TOURNAMENT_SIZE)])
		#print(parent_first.get_total_cost())
		#print(parent_second.get_total_cost())
		child = Route()
		child.set_route(generate_child(parent_first, parent_second))
		if random.random() < MUTATION_PROBABILITY:
			child.set_route(mutate(child.get_route()))
		#print(i)
		#print(list(range(100, 6000, 100)))
		if ITERATION_COUNT != 0:
			if i in list(range(100, ITERATION_COUNT, 200)):
				for g in range(30):
					if random.random() < MUTATION_PROBABILITY * 6:
						child.set_route(mutate(child.get_route()))
		#("Dziecko: " + str(child.get_route()))
		#print("\n")
		child.set_total_cost(evaluate_route(copy.deepcopy(child.get_route()), distance_matrix, CITIES_DEMAND))
		#print(child.get_total_cost())
		new_population.append(copy.deepcopy(child))
		#print("\n")
	#new_population.sort()
	#print("Nowa populacja: ")
	same_result = 0
	# for i in range(POPULATION_SIZE - 1):
	# 	print(new_population[i].get_total_cost())
	# 	if (new_population[i].get_route() == new_population[0].get_route()):
	# 		same_result += 1
	# 	else:
	# 		print(new_population[i].get_route())
	#print("\n")
	best_result_in_population = min(new_population)
	os.system("cls")
	print("This iteration [" + str(i + 1) + "] best solution cost: ")
	print(best_result_in_population.get_total_cost())
	print("So far best solution cost: ")
	print(best_route.get_total_cost())
	if best_result_in_population < best_route:
		display.fill((0,0,0))
		best_route = copy.deepcopy(best_result_in_population)
		min_lat = min(border_position['latitude'])
		max_lat = max(border_position['latitude'])
		min_long = min(border_position['longitude'])
		max_long = max(border_position['longitude'])
		for i in range(len(CITIES_DEMAND)):
			pos_lat = (position['latitude'][i]-min_lat)/(max_lat-min_lat)*700+50
			pos_long = (position['longitude'][i]-min_long)/(max_long-min_long)*700+50
			pygame.draw.circle(display, (255, 255, 255), (pos_long, 800-pos_lat), 4)
		route = copy.deepcopy(best_route.get_route())

		for i in range(18):
			border_one_lat = (border_position['latitude'][i]-min_lat)/(max_lat-min_lat)*700+50
			border_one_long = (border_position['longitude'][i]-min_long)/(max_long-min_long)*700+50
			border_second_lat = (border_position['latitude'][i + 1]-min_lat)/(max_lat-min_lat)*700+50
			border_second_long = (border_position['longitude'][i + 1]-min_long)/(max_long-min_long)*700+50
			pygame.draw.line(display, (255, 255, 255), (border_one_long, 800-border_one_lat), (border_second_long, 800-border_second_lat),1)
		border_one_lat = (border_position['latitude'][18]-min_lat)/(max_lat-min_lat)*700+50
		border_one_long = (border_position['longitude'][18]-min_long)/(max_long-min_long)*700+50
		border_second_lat = (border_position['latitude'][0]-min_lat)/(max_lat-min_lat)*700+50
		border_second_long = (border_position['longitude'][0]-min_long)/(max_long-min_long)*700+50
		pygame.draw.line(display, (255, 255, 255), (border_one_long, 800-border_one_lat), (border_second_long, 800-border_second_lat),1)
		colors_copied = copy.deepcopy(COLORS)
		while route:
			capacity = 0
			main_city = "Krakow"
			main_city_lat = (position['latitude'][30]-min_lat)/(max_lat-min_lat)*700+50
			main_city_long = (position['longitude'][30]-min_long)/(max_long-min_long)*700+50
			city = route.pop()
			capacity = CITIES_DEMAND[city]
			city_lat = (position['latitude'][unvisited_cities.index(city)]-min_lat)/(max_lat-min_lat)*700+50
			city_long = (position['longitude'][unvisited_cities.index(city)]-min_long)/(max_long-min_long)*700+50
			if not colors_copied:
				color = pygame.Color('#' +''.join([random.choice('89ABCDEF') for j in range(6)]))
			else:
				color = pygame.Color(colors_copied.pop())
			pygame.draw.line(display, color, (city_long, 800-city_lat), (main_city_long, 800-main_city_lat),1)
			while True:
				if route:
					if capacity + CITIES_DEMAND[route[-1]] > CAR_CAPACITY:
						break
					next_city = route.pop()
					capacity += CITIES_DEMAND[next_city]
					next_city_lat = (position['latitude'][unvisited_cities.index(next_city)]-min_lat)/(max_lat-min_lat)*700+50
					next_city_long = (position['longitude'][unvisited_cities.index(next_city)]-min_long)/(max_long-min_long)*700+50
					pygame.draw.line(display, color, (city_long, 800-city_lat), (next_city_long, 800-next_city_lat),1)
					city = next_city
					city_lat = (position['latitude'][unvisited_cities.index(city)]-min_lat)/(max_lat-min_lat)*700+50
					city_long = (position['longitude'][unvisited_cities.index(city)]-min_long)/(max_long-min_long)*700+50
				else:
					break
			pygame.draw.line(display, color, (city_long, 800-city_lat), (main_city_long,800-main_city_lat),1)
		pygame.display.update()
	#print(len(new_population))
	population = copy.deepcopy(new_population)
route = best_route.get_route()
os.system("cls")
print("Best solution cost: " + str(best_route.get_total_cost()))
print("Best solution routes: ")
while route:
	one_car_route = []
	capacity = 0
	main_city = "Krakow"
	city = route.pop()
	capacity = CITIES_DEMAND[city]
	one_car_route.append(city)
	while True:
		if route:
			if capacity + CITIES_DEMAND[route[-1]] > CAR_CAPACITY:
				break
			next_city = route.pop()
			capacity += CITIES_DEMAND[next_city]
			city = next_city
			one_car_route.append(city)
		else:
			break
	print(one_car_route)
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
		if event.type == KEYDOWN:
			break

