import csv
from domain.listing import Listing


class ListingRepository:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_listings(self) -> list[Listing]:
        listings = []

        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                listing = Listing(
                    name=row["name"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    total_price=float(row["total_price"]),
                    nights=int(row["nights"]),
                    bedrooms=int(row["bedrooms"]),
                    bathrooms=int(row["bathrooms"]),
                    area_m2=float(row["area_m2"]),
                    rating=float(row["rating"]),
                    reviews_count=int(row["reviews_count"]),
                    amenities=set(row["amenities"].split("|"))
                )

                listings.append(listing)

        return listings
