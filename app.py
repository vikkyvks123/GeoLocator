from flask import Flask, render_template, request, jsonify
import numpy as np
import folium

app = Flask(__name__)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    distance = R * c
    return distance


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    data = request.json
    lat1 = data['lat1']
    lon1 = data['lon1']
    lat2 = data['lat2']
    lon2 = data['lon2']
    loc1 = data['loc1']
    loc2 = data['loc2']
    distance = haversine(lat1, lon1, lat2, lon2)

    # Calculate the center point
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    center_name = "Midpoint"  # Label for the center point

    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)
    folium.Marker([lat1, lon1], popup=f'Location 1: {loc1}').add_to(m)
    folium.Marker([lat2, lon2], popup=f'Location 2: {loc2}').add_to(m)
    folium.Marker([center_lat, center_lon], popup=center_name).add_to(m)
    folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color='blue').add_to(m)
    map_html = m._repr_html_()

    return jsonify({'distance': distance, 'map': map_html})


if __name__ == '__main__':
    app.run(debug=True)
