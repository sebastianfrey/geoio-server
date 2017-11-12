"""All algorithms used by geoio-server"""
import math
import functools

import geojson

def angle(point1, point2):
    """calculates the angle between two points in radians"""
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

def convex_hull(collection):
    """Calculates the convex hull of an geojson feature collection."""

    features_or_geometries = []

    if collection["type"] == "GeometryCollection":
        features_or_geometries = collection["geometries"]
    elif collection["type"] == "FeatureCollection":
        features_or_geometries = collection["features"]

    if features_or_geometries is None or len(features_or_geometries) == 0:
        raise Exception("No features or geometries where found")

    features_or_geometries_mapper = lambda feature_or_geometry: list(geojson.utils.coords(feature_or_geometry))
    coordinates_reducer = lambda a, b: a + b

    coordinates_list = list(map(features_or_geometries_mapper, features_or_geometries))
    points = list(functools.reduce(coordinates_reducer, coordinates_list))

    unique_points = list(set(points))

    sorted_points = sorted(unique_points, key=lambda point: (point[1], point[0]))

    point0 = sorted_points.pop(0)

    sorted_points_with_angle = list(map(lambda point: [point[0], point[1], angle(point0, point)], sorted_points));

    sorted_points = sorted(sorted_points_with_angle, key=lambda point: point[2])


    return {'points': sorted_points}
