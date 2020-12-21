import numpy as np
import pandas as pd
import matplotlib as plt
from scipy.spatial.distance import squareform, pdist
from sklearn.neighbors import DistanceMetric
number_of_cars = 5
car_capacity = 1000
number_of_customers = 30
main_dict = {"Bialystok":500,"Bielsko_Biala":50,"Chrzanow":400,"Gdansk":200,"Gdynia":100,"Gliwice":40,
"Gromnik":200,"Katowice":300,"Kielce":30,"Krosno":60,"Krynica":50,"Lublin":60,"Lodz":160,"Malbork":100,"Nowy_Targ":120,
"Olsztyn":300,"Poznan":100,"Pulawy":200,"Radom":100,"Rzeszow":60,"Sandomierz":200,
"Szczecin":150,"Szczucin":60,"Szklarska_Poreba":50,"Tarnow":70,"Warszawa":200,
"Wieliczka":90,"Wroclaw":40,"Zakopane":200,"Zamosc":300}
position = pd.read_csv('data.csv',sep=';',encoding= 'unicode_escape')
#choose distance metrics
dist = DistanceMetric.get_metric('haversine')
#convert degrees to radian
position['latitude']=np.radians(position['latitude'])
position['longitude']=np.radians(position['longitude'])
#make distance matrix
distance_matrix = dist.pairwise(position[['lat','lon']].to_numpy())*6373
print(distance_matrix)