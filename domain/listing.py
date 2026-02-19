class Listing:

    def __init__(self, name, latitude, longitude, total_price, nights,
                 bedrooms, bathrooms, area_m2, rating, reviews_count, amenities):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.total_price = total_price
        self.nights = nights
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area_m2 = area_m2
        self.rating = rating
        self.reviews_count = reviews_count
        self.amenities = amenities

    @property
    def price_per_night(self):
        return self.total_price / self.nights

    def __repr__(self):
        return (
            f"{self.name} | "
            f"{self.price_per_night:.2f} lei/night | "
            f"Rating: {self.rating} | "
            f"Reviews: {self.reviews_count}"
        )
