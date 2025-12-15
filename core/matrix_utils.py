import googlemaps
import numpy as np
import pandas as pd
import time

def get_coordinates(locations_df, api_key):
    gmaps = googlemaps.Client(key=api_key)

    def get_lat_lon(address):
        try:
            geocode_result = gmaps.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return location['lat'], location['lng']
        except Exception:
            return None, None

    locations_df[['latitude', 'longitude']] = locations_df['Address'].apply(
        lambda x: pd.Series(get_lat_lon(x))
    )
    return locations_df

def get_distance_matrix(locations_df, api_key):
    gmaps = googlemaps.Client(key=api_key)
    addresses = locations_df['Address'].tolist()
    N = len(addresses)
    distance_matrix = np.zeros((N, N))
    MAX_ELEMENTS = 10

    for i in range(N):
        origins = [addresses[i]]
        for j_start in range(0, N, MAX_ELEMENTS):
            destinations = addresses[j_start:j_start + MAX_ELEMENTS]
            try:
                matrix_result = gmaps.distance_matrix(origins, destinations, mode="driving")
            except Exception:
                return None

            if 'rows' in matrix_result:
                elements = matrix_result['rows'][0]['elements']
                for k in range(len(elements)):
                    j = j_start + k
                    if elements[k]['status'] == 'OK':
                        # Mesafeyi (metre) alır ve KM'ye çevirir
                        distance_matrix[i, j] = elements[k]['distance']['value'] / 1000.0
                    else:
                        distance_matrix[i, j] = 99999999.0
        time.sleep(0.05)

    np.fill_diagonal(distance_matrix, 0)
    return distance_matrix
