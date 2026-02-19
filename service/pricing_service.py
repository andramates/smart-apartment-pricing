import statistics
from domain.listing import Listing


class PricingService:

    @staticmethod
    def recommend_price(
        ranked_listings: list[tuple[Listing, float]],
        top_n: int = 10
    ) -> dict:
        """
        Returns pricing insights based on top similar listings.
        """

        if not ranked_listings:
            return {
                "recommended_price": None,
                "median_price": None,
                "average_price": None,
                "message": "No comparable listings found."
            }

        top = ranked_listings[:top_n]

        prices = [listing.price_per_night for listing, _ in top]
        weights = [score for _, score in top]

        # --- Median ---
        median_price = statistics.median(prices)

        # --- Average ---
        average_price = sum(prices) / len(prices)

        # --- Weighted Average ---
        if sum(weights) == 0:
            weighted_price = average_price
        else:
            weighted_price = sum(
                price * weight for price, weight in zip(prices, weights)
            ) / sum(weights)

        # Recommended = weighted (mai smart decât median simplu)
        recommended_price = round(weighted_price, 2)

        return {
            "recommended_price": recommended_price,
            "median_price": round(median_price, 2),
            "average_price": round(average_price, 2),
            "comparables_used": len(top)
        }

    @staticmethod
    def price_positioning(
        my_price: float,
        ranked_listings: list[tuple[Listing, float]],
        top_n: int = 10
    ) -> str:

        if not ranked_listings:
            return "No market data."

        top = ranked_listings[:top_n]
        prices = sorted([listing.price_per_night for listing, _ in top])

        below = len([p for p in prices if p < my_price])
        percentile = (below / len(prices)) * 100

        if percentile < 30:
            return f"Underpriced (below {percentile:.0f}th percentile)"
        elif percentile > 70:
            return f"Overpriced (above {percentile:.0f}th percentile)"
        else:
            return f"Competitively priced ({percentile:.0f}th percentile)"
