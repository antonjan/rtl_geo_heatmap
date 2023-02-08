import pandas as pd
import folium

from folium.plugins import HeatMap
map_obj = folium.Map(location = [38.27312, -98.5821872], zoom_start = 5)
population_data = pd.read_csv(r"rf_geo_data.csv")
#STATE,rfdbm,lat,long
population_data.head()
lats_longs_weight = list(map(list, zip(population_data["lat"],
                          population_data["long"],
                          population_data["rfdbm"]
                         )
               )
           )
lats_longs_weight[:5]
HeatMap(lats_longs_weight).add_to(map_obj)

map_obj
map_obj.save(r"folium_map.html")
