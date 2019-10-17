import folium
import backend
import webbrowser


database = backend.Database_user()
result = database.map_markers()
map = folium.Map(location=[55.79, 49.12], zoom_start=14, tiles="openstreetmap")
fgroup = folium.FeatureGroup(name="Университеты Казани")
for item in result:
    fgroup.add_child(folium.CircleMarker(location=[float(item[0]), float(item[1])], radius=6, popup=item[2], fill_color='blue', fill=True, color="grey", fill_opacity=0.7))

map.add_child(fgroup)
map.add_child(folium.LayerControl())
map.save("templates/map.html")
webbrowser.open_new_tab("file:///D:/Python%20projects/Testing2/templates/map.html")
