# 🛍️ Shopify Customer Review Explorer

This project is a complete pipeline for cleaning, analyzing, and exploring customer reviews from a Shopify store. It allows stakeholders or non-technical users to query review data using natural language, view insights, and apply filters (e.g., country, rating range, product category).

---

## 📁 Dataset Description

The original dataset contains messy raw reviews with the following columns:

- `Review ID`
- `Product Name`
- `Rating` (1–5, with some invalid or missing)
- `Review Content` (unstructured text)
- `Timestamp`
- `Customer Email`
- `Product Category` (inconsistent naming)
- `Order Value`
- `Fulfillment Status`
- `Shipping Country`

---

## ✅ Cleaning Steps Performed

All data cleaning steps are done in Python using `pandas`:

### 1. **Standardize Timestamps**
- Parsed all timestamp fields to a consistent `datetime` format using `pd.to_datetime`.

### 2. **Fix Inconsistent Product/Category Names**
- Merged similar/typo entries (e.g., `"Promdrsses"` ➝ `"Prom Dresses"`).

### 3. **Remove Blank/Invalid Reviews**
- Dropped rows with empty `Review Content` or those containing only filler/non-informative text.

### 4. **Normalize Ratings**
- Removed invalid values.
- Missing ratings (0 or NaN) are imputed with the **average rating** of the dataset.

---

## 🤖 Chatbot-Powered Insights

### Built With:
- **Streamlit** for a simple web interface
- **Gemini 2.0 (Flash)** from Google (via `google.generativeai`)
- **Pandas** for filtering data

### Features:
- Users can type natural language questions like:
  - “Which product categories have the most 1-star reviews in Canada?”
  - “Do higher order values correlate with lower ratings?”
  - “What are the top complaints and compliments?”
- Real-time answers powered by Gemini AI
- Sidebar filters:
  - Country
  - Rating Range
  - Product Category

---

## ✨ Prompt Design (for Gemini API)

Custom prompts are used to ensure focused, concise, and context-specific responses from the model. For example:

