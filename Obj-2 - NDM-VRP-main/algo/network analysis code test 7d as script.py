import os
import pandas as pd
from qgis.core import QgsVectorLayer, QgsProject, QgsWkbTypes, QgsCoordinateReferenceSystem, QgsField
from qgis.PyQt.QtCore import QVariant
import processing
from itertools import combinations

# Function to create a new vector layer
def create_vector_layer():
    # Create the vector layer
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    layer_name = "Shortest Paths"
    layer = QgsVectorLayer("LineString?crs=epsg:4326", layer_name, "memory")
    
    # Add fields to the layer
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("start_point_id", QVariant.String),
                            QgsField("end_point_id", QVariant.String),
                            QgsField("cost", QVariant.Double)])
    layer.updateFields()
    
    # Add the layer to the project
    #QgsProject.instance().addMapLayer(layer)
    
    return layer

# Create a new vector layer for shortest paths
shortest_paths_layer = create_vector_layer()

# Load points data from CSV
points_data_file = "D:/new points1.csv"
points_data = pd.read_csv(points_data_file)

# Get pairwise combinations of points
point_combinations = combinations(points_data['point_id'], 2)

# Create a list to store travel cost results
travel_cost_results = []

# Iterate over point combinations
for start_point_id, end_point_id in point_combinations:
    start_point = points_data[points_data['point_id'] == start_point_id].iloc[0]
    end_point = points_data[points_data['point_id'] == end_point_id].iloc[0]
    
    start_lat_lon = f"{start_point['longitude']},{start_point['latitude']} [EPSG:4326]"
    end_lat_lon = f"{end_point['longitude']},{end_point['latitude']} [EPSG:4326]"

    # Run the processing algorithm for start to end
    result1 = processing.run("native:shortestpathpointtopoint", {
        'INPUT': 'D:/road layer 2.gpkg|layername=merged',
        'STRATEGY': 0,
        'DIRECTION_FIELD': '',
        'VALUE_FORWARD': '',
        'VALUE_BACKWARD': '',
        'VALUE_BOTH': '',
        'DEFAULT_DIRECTION': 2,
        'SPEED_FIELD': '',
        'DEFAULT_SPEED': 50,
        'TOLERANCE': 0,
        'START_POINT': start_lat_lon,
        'END_POINT': end_lat_lon,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })
    
    # Retrieve the travel cost from the result
    travel_cost1 = result1['TRAVEL_COST']
    
    # Append the travel cost and point IDs to the list
    travel_cost_results.append({
        'start_point_id': start_point_id,
        'end_point_id': end_point_id,
        'travel_cost': travel_cost1
    })

    # Run the processing algorithm for end to start
    result2 = processing.run("native:shortestpathpointtopoint", {
        'INPUT': 'D:/road layer 2.gpkg|layername=merged',
        'STRATEGY': 0,
        'DIRECTION_FIELD': '',
        'VALUE_FORWARD': '',
        'VALUE_BACKWARD': '',
        'VALUE_BOTH': '',
        'DEFAULT_DIRECTION': 2,
        'SPEED_FIELD': '',
        'DEFAULT_SPEED': 50,
        'TOLERANCE': 0,
        'START_POINT': end_lat_lon, # Reverse start and end points
        'END_POINT': start_lat_lon, # Reverse start and end points
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })
    
    # Retrieve the travel cost from the result
    travel_cost2 = result2['TRAVEL_COST']
    
    # Append the travel cost and point IDs to the list
    travel_cost_results.append({
        'start_point_id': end_point_id, # Reverse start and end points
        'end_point_id': start_point_id, # Reverse start and end points
        'travel_cost': travel_cost2
    })

    # Retrieve the output vector layer
    output_layer = result1['OUTPUT'] # You can use either result1 or result2 for the output layer

    # Check if the output layer is valid and add features to the shortest paths layer
    if output_layer.isValid():
        for feature in output_layer.getFeatures():
            shortest_paths_layer.addFeature(feature)

# Save the shortest paths layer to the project
#QgsProject.instance().addMapLayer(shortest_paths_layer)

# Convert the list of travel cost results to a DataFrame
travel_cost_df = pd.DataFrame(travel_cost_results)

# Save the travel cost results to a CSV file
output_csv_file = "D:/travel_cost_results.csv"
travel_cost_df.to_csv(output_csv_file, index=False)
print(f"Travel cost results saved to {output_csv_file}")
