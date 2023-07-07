import folium

lcord = [52.376111375557294, 4.927876776449689]

m = folium.Map(
    location = [52.37613757431285, 4.927801674596649], 
    zoom_start=12
    )

folium.Marker(
    location=lcord, 
    popup='<h1>1</h1>', tooltip='No Idea', 
    # icon=folium.Icon(icon='heart')
    ).add_to(m)

folium.Circle(
    location=lcord,
    radius=800,
    color='blue',
    popup='info',
    fill=True,
    fill_color='blue'
).add_to(m)

m.save('map.html')