"""All algorithms used by geoio-server"""
import math
import functools

import geojson

def angle(point_1, point_2):
    """calculates the angle between two points in radians"""
    return math.atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])

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

    if len(points) < 3:
        raise Exception("Can not calculate convex hull of less then 3 input points.")

    points = list(set(points))

    points = sorted(points, key=lambda point: (point[1], point[0]))

    point0 = points.pop(0)

    points = list(map(lambda point: (point[0], point[1], angle(point0, point)), points))

    points = list(sorted(points, key=lambda point: point[2]))
    points.insert(0, point0)
    hull = [points[0], (points[1][0], points[1][1])]

    i = 2
    points_count = len(points)

    while i < points_count:
        stack_length = len(hull)
        point_1 = hull[stack_length-1]
        point_2 = hull[stack_length-2]
        point_i = points[i]

        discrimnante = (point_2[0] - point_1[0]) * (point_i[1] - point_1[1]) - (point_i[0] - point_1[0]) * (point_2[1] - point_1[1])
        if discrimnante < 0 or stack_length == 2:
            hull.append((point_i[0], point_i[1]))
            i = i+1
        else:
            hull.pop()


    return geojson.Polygon(hull)
