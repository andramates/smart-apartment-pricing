import streamlit as st

from repository.listing_repository import ListingRepository
from service.geo_service import GeoService
from service.filter_service import FilterService
from service.similarity_service import SimilarityService
from service.pricing_service import PricingService
from domain.listing import Listing


def run_app():

    st.set_page_config(page_title="Smart Apartment Pricing", layout="wide")

    st.title("🏠 Smart Apartment Pricing Engine")
    st.markdown("Find optimal nightly price based on similar listings.")

    # -------------------------
    # Dataset selection
    # -------------------------

    dataset_option = st.selectbox(
        "Select dataset",
        ["Weekend (2 nights)", "Full Week (7 nights)"]
    )

    if dataset_option == "Weekend (2 nights)":
        file_path = "data/data_weekend.csv"
        nights = 2
    else:
        file_path = "data/data_week.csv"
        nights = 7

    repo = ListingRepository(file_path)
    listings = repo.load_listings()

    # -------------------------
    # Sidebar Inputs
    # -------------------------

    st.sidebar.header("Your Apartment Details")


    latitude = st.sidebar.number_input("Latitude", value=46.7717142, format="%.7f")
    longitude = st.sidebar.number_input("Longitude", value=23.6313795, format="%.7f")

    bedrooms = st.sidebar.number_input("Bedrooms", min_value=1, value=1)
    bathrooms = st.sidebar.number_input("Bathrooms", min_value=1, value=1)

    area = st.sidebar.number_input("Area (m²)", min_value=20, value=40)
    rating = st.sidebar.slider("Your Rating", 8.0, 10.0, 9.5)

    radius = st.sidebar.slider("Search Radius (km)", 1, 5, 3)

    amenities_input = st.sidebar.multiselect(
        "Amenities",
        ["wifi", "parking", "balcony", "elevator", "ac", "kitchen", "washing_machine"],
        default=["wifi", "parking", "balcony"]
    )

    current_price = st.sidebar.number_input("Your Current Price (per night)", min_value=0, value=200)

    # -------------------------
    # Build Target
    # -------------------------

    target = Listing(
        name="My Apartment",
        latitude=latitude,
        longitude=longitude,
        total_price=0,
        nights=nights,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area_m2=area,
        rating=rating,
        reviews_count=0,
        amenities=set(amenities_input)
    )

    # -------------------------
    # Run Analysis
    # -------------------------

    if st.button("Analyze Market"):

        geo_filtered = GeoService.filter_by_radius(
            listings,
            target.latitude,
            target.longitude,
            radius
        )

        geo_filtered = FilterService.filter_by_bedrooms(geo_filtered, bedrooms)
        geo_filtered = FilterService.filter_by_rating_range(geo_filtered, rating, tolerance=1)
        geo_filtered = FilterService.filter_by_min_reviews(geo_filtered, 20)

        ranked = SimilarityService.rank_by_similarity(target, geo_filtered, radius)

        pricing = PricingService.recommend_price(ranked, top_n=10)

        st.subheader("📊 Pricing Insights")

        if pricing["recommended_price"] is None:
            st.warning("No comparable listings found.")
            return

        col1, col2, col3 = st.columns(3)

        col1.metric("Recommended Price", f"{pricing['recommended_price']} lei")
        col2.metric("Median Market Price", f"{pricing['median_price']} lei")
        col3.metric("Average Market Price", f"{pricing['average_price']} lei")

        position = PricingService.price_positioning(
            current_price,
            ranked,
            top_n=10
        )

        st.markdown(f"### 📍 Market Position: {position}")

        st.subheader("Top Similar Listings")

        for listing, score in ranked[:10]:
            st.write(
                f"**{listing.name}** | "
                f"{listing.price_per_night:.2f} lei/night | "
                f"Similarity: {score:.2f}"
            )
