**Smart Apartment Pricing Engine**

A modular, data-driven pricing recommendation system for short-term rental hosts.
The application analyzes comparable listings based on geospatial proximity, structural similarity, and qualitative attributes, and generates an optimal nightly price using a weighted similarity model.

**Overview**

This project implements a simplified pricing intelligence engine inspired by real-world short-term rental platforms.

Given a target apartment, the system:

1. Filters comparable listings based on:
   - Geographic radius (Haversine distance)
   - Bedroom count
   - Rating tolerance
   - Minimum review count

2. Computes a similarity score using weighted features:
   - Distance (30%)
   - Amenities similarity (30%)
   - Area similarity (20%)
   - Rating similarity (20%)

3. Generates pricing insights:
   - Median market price
   - Average market price
   - Similarity-weighted recommended price
   - Market positioning (underpriced / competitive / overpriced)

The pricing recommendation prioritizes highly similar listings through weighted averaging.

**Architecture**

The system follows a clean, layered architecture:
domain/ → Core data models,
repository/ → Data loading layer,
service/ → Business logic,
ui/ → Streamlit presentation layer,
data/ → Sample datasets

**Technologies**

- Python 3.9+
- Streamlit
- Object-Oriented Programming
- Geospatial distance computation (Haversine formula)
- Similarity-based recommendation logic
- Basic statistical analysis (median, weighted average)

**How to Run**

Install dependencies:
pip install streamlit

Run the application:
streamlit run main.py

