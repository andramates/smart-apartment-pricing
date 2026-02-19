from domain.listing import Listing


class FilterService:

    @staticmethod
    def filter_by_bedrooms(
        listings: list[Listing],
        target_bedrooms: int
    ) -> list[Listing]:
        return [
            listing
            for listing in listings
            if listing.bedrooms == target_bedrooms
        ]

    @staticmethod
    def filter_by_rating_range(
        listings: list[Listing],
        target_rating: float,
        tolerance: float = 1.0
    ) -> list[Listing]:
        min_rating = target_rating - tolerance
        max_rating = target_rating + tolerance

        return [
            listing
            for listing in listings
            if min_rating <= listing.rating <= max_rating
        ]

    @staticmethod
    def filter_by_min_reviews(
        listings: list[Listing],
        min_reviews: int = 20
    ) -> list[Listing]:
        return [
            listing
            for listing in listings
            if listing.reviews_count >= min_reviews
        ]

    @staticmethod
    def filter_by_area_range(
        listings: list[Listing],
        target_area: float,
        tolerance_percentage: float = 0.3
    ) -> list[Listing]:
        """
        Filters listings within +/- percentage of target area.
        Example: 0.3 = +/-30%
        """

        min_area = target_area * (1 - tolerance_percentage)
        max_area = target_area * (1 + tolerance_percentage)

        return [
            listing
            for listing in listings
            if min_area <= listing.area_m2 <= max_area
        ]
