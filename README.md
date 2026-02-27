# Smart Apartment Pricing Engine

A pricing system that combines similarity-based market analysis with machine learning to recommend optimal nightly prices for short-term rental properties.

---

## Overview

This project implements a hybrid pricing strategy that integrates:

1. Market-based similarity scoring  
2. Machine learning regression models  
3. Explainable AI techniques  

The application allows users to select a property location on an interactive map and generate pricing insights based on comparable listings within a selected radius.

---

## Core Features

### Market-Based Pricing
- Geographic filtering (radius-based)
- Structural filtering (bedrooms, rating, review count)
- Weighted similarity scoring
- Recommended price based on comparable listings
- Median and average market benchmarks
- Percentile-based market positioning

### Machine Learning Pricing
- Model comparison:
  - Linear Regression
  - Random Forest Regressor
- Automatic best model selection based on R²
- SHAP-based feature impact explanations

### System Architecture
- Domain layer (Listing model)
- Repository layer (data loading)
- Service layer (geo, filtering, similarity, pricing, ML)
- Streamlit UI layer
---

## Machine Learning Approach

Features used:
- Distance to target location
- Bedrooms
- Bathrooms
- Area (m²)
- Rating
- Amenities count

Training strategy:
- Top-N comparable listings
- 70/30 train-test split
- Model performance comparison
- Best model selected dynamically

---

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- SHAP
- Folium
- Pandas
- NumPy

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run main.py
```
