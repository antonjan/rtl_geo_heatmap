import folium

from folium.plugins import HeatMap

map_obj = folium.Map(location = [38.27312, -98.5821872], zoom_start = 5)


lats_longs = [
                [38.27312, -98.5821872, 0.5], # Kansas
                [34.395342, -111.763275,0.2], # Arizona
                [37.5726028, -85.1551411, 0.7], # Kentucky
                [32.3293809, -83.1137366,0.9], # Georgia
                [40.0796606, -89.4337288,0.1], # Illinois
            ]


HeatMap(lats_longs).add_to(map_obj)

map_obj
map_obj.save(r"folium_map.html")
