from domain.listing import Listing
from service.geo_service import GeoService


class SimilarityService:

    @staticmethod
    def calculate_similarity(
        target: Listing,
        candidate: Listing,
        radius_km: float
    ) -> float:

        # --- Distance ---
        distance = GeoService.haversine_distance(
            target.latitude,
            target.longitude,
            candidate.latitude,
            candidate.longitude
        )

        distance_score = max(0, 1 - (distance / radius_km))

        # --- Rating ---
        rating_diff = abs(target.rating - candidate.rating)
        rating_score = max(0, 1 - (rating_diff / 2))

        # --- Area ---
        area_diff = abs(target.area_m2 - candidate.area_m2)
        max_area = max(target.area_m2, candidate.area_m2)
        area_score = max(0, 1 - (area_diff / max_area))

        # --- Amenities (Jaccard) ---
        intersection = target.amenities.intersection(candidate.amenities)
        union = target.amenities.union(candidate.amenities)

        if len(union) == 0:
            amenities_score = 0
        else:
            amenities_score = len(intersection) / len(union)

        # --- Weighted sum ---
        similarity = (
            0.3 * distance_score +
            0.2 * rating_score +
            0.2 * area_score +
            0.3 * amenities_score
        )

        return similarity

    @staticmethod
    def rank_by_similarity(
        target: Listing,
        listings: list[Listing],
        radius_km: float
    ) -> list[tuple[Listing, float]]:

        scored = []

        for listing in listings:
            score = SimilarityService.calculate_similarity(
                target,
                listing,
                radius_km
            )
            scored.append((listing, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        return scored
