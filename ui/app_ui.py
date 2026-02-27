import streamlit as st
import folium
from streamlit_folium import st_folium

from repository.listing_repository import ListingRepository
from service.geo_service import GeoService
from service.filter_service import FilterService
from service.similarity_service import SimilarityService
from service.pricing_service import PricingService
from service.ml_pricing_service import MLPricingService
from domain.listing import Listing


def run_app():

    st.set_page_config(page_title="Smart Apartment Pricing", layout="wide")

    st.title("🏠 Smart Apartment Pricing Engine")
    st.markdown("Find optimal nightly price based on similar listings.")

    if "selected_location" not in st.session_state:
        st.session_state.selected_location = None

    if "map_center" not in st.session_state:
        st.session_state.map_center = [46.7717142, 23.6313795]

    if "map_zoom" not in st.session_state:
        st.session_state.map_zoom = 13

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

    st.subheader("📍 Select Apartment Location")

    map_center = [46.7717142, 23.6313795]

    m = folium.Map(location=st.session_state.map_center,
    zoom_start=st.session_state.map_zoom)


    if st.session_state.selected_location is not None:
        folium.Marker(
            location=st.session_state.selected_location,
            tooltip="Your Apartment",
            icon=folium.Icon(color="red", icon="home")
        ).add_to(m)

    map_data = st_folium(m, width=700, height=500)



    if map_data and map_data.get("last_clicked"):
        if map_data.get("center"):
            st.session_state.map_center = [
                map_data["center"]["lat"],
                map_data["center"]["lng"]
            ]

        if map_data.get("zoom"):
            st.session_state.map_zoom = map_data["zoom"]
        clicked = map_data["last_clicked"]
        new_location = [clicked["lat"], clicked["lng"]]

        if st.session_state.selected_location != new_location:
            st.session_state.selected_location = new_location

    if st.session_state.selected_location is not None:
        latitude, longitude = st.session_state.selected_location
        st.success(f"Selected Location: {latitude:.7f}, {longitude:.7f}")
    else:
        st.info("Click on the map to select your apartment location.")

    if st.session_state.selected_location is None:
        st.warning("Please select a location on the map.")
        return

    latitude = st.session_state.selected_location[0]
    longitude = st.session_state.selected_location[1]

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

        ml_service = MLPricingService()
        trained = ml_service.train(ranked, target, top_n = 30)


        st.subheader("📊 Pricing Insights")


        if pricing["recommended_price"] is None:
            st.warning("No comparable listings found.")
            return

        col1, col2, col3 = st.columns(3)

        col1.metric("Recommended Price", f"{pricing['recommended_price']} lei")
        col2.metric("Median Market Price", f"{pricing['median_price']} lei")
        col3.metric("Average Market Price", f"{pricing['average_price']} lei")

        if trained:

            predicted_price = ml_service.predict(target, target)
            metrics = ml_service.get_metrics()

            st.subheader("👽 AI Model Performance")

            col1, col2, col3 = st.columns(3)

            col1.metric("Best Model", metrics["best_model"])
            col2.metric("Best R² (test)", f"{metrics['best_r2']:.2f}")
            col3.metric("Best MAE (test)", f"{metrics['best_mae']:.2f} lei")

            st.write("Linear Regression R²:", f"{metrics['linear_r2']:.2f}")
            st.write("Random Forest R²:", f"{metrics['rf_r2']:.2f}")

            st.metric("AI Predicted Price", f"{predicted_price:.2f} lei")

            if ml_service.best_model_name == "Random Forest":
                explanation = ml_service.explain(target, target)

                st.subheader("🔎 SHAP Explanation")

                for feature, impact in explanation.items():
                    st.write(f"{feature}: {impact:.2f} lei impact")


        else:
            st.warning("Not enough data to train AI model.")



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
