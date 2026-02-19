import math
from domain.listing import Listing


class GeoService:

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Returns distance in kilometers between two lat/lon points.
        """
        R = 6371  # Earth radius in km

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    @staticmethod
    def filter_by_radius(
        listings: list[Listing],
        target_lat: float,
        target_lon: float,
        radius_km: float
    ) -> list[Listing]:

        filtered = []

        for listing in listings:
            distance = GeoService.haversine_distance(
                target_lat,
                target_lon,
                listing.latitude,
                listing.longitude
            )

            if distance <= radius_km:
                filtered.append(listing)

        return filtered
