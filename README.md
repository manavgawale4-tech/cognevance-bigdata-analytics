# E-Commerce Customer Analytics & Predictive Intelligence

## Project Overview

This project analyzes the Olist Brazilian E-Commerce Public Dataset to understand sales trends, customer purchasing behavior, product category performance, payment preferences, and delivery performance.

The project combines Python, SQL, PySpark, Machine Learning, and Streamlit to generate business insights and build a baseline model for delivery-time prediction.

An interactive dashboard helps users explore key performance indicators and analytical results.

## Project Objectives

* Analyze monthly and yearly sales trends.
* Identify high-revenue product categories.
* Understand customer purchasing and repeat-order behavior.
* Analyze payment methods and customer reviews.
* Evaluate delivery time and delivery performance.
* Develop a machine learning model to estimate delivery time.
* Use SQL and PySpark for data analysis and aggregation.
* Present insights through an interactive dashboard.
* Generate business recommendations from analytical results.

## Dataset

**Dataset:** Olist Brazilian E-Commerce Public Dataset
**Source:** Kaggle

**Dataset Link:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains multiple CSV files covering orders, customers, products, sellers, payments, reviews, order items, and geolocation.

These related datasets are used to analyze different aspects of e-commerce operations.

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Plotly
* SQL
* MySQL
* PySpark
* Scikit-learn
* Random Forest Regression
* Jupyter Notebook
* Streamlit
* Joblib
* Visual Studio Code

## Project Structure

```text
cognevance_bigDataAnalytics/
│
├── dataset/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
│
├── notebooks/
│   └── ecommerce_sales_analysis.ipynb
│
├── sql/
│   └── ecommerce_analysis.sql
│
├── src/
│   ├── import_csv_to_mysql.py
│   └── pyspark_analysis.py
│
├── models/
│   └── delivery_time_model.pkl
│
├── dashboards/
│   └── app.py
│
├── outputs/
│   └── pyspark/
│       ├── monthly_sales.csv
│       ├── category_revenue.csv
│       ├── customer_behavior.csv
│       ├── delivery_summary.csv
│       ├── yearly_sales.csv
│       └── delivery_performance.csv
│
├── report/
│   └── Ecommerce_Customer_Analytics_Report.md
│
├── requirements.txt
└── README.md
```

*Note: This structure represents the intended organization of the project. Confirm that each listed file exists in the repository before submitting.*

## Key Business Metrics

The following metrics were generated during the PySpark analysis:

| Metric                                      |            Result |
| ------------------------------------------- | ----------------: |
| Total Orders                                |            99,441 |
| Unique Customers                            |            96,096 |
| Delivered Orders                            |            96,478 |
| Delivered Product Revenue                   | BRL 13,221,498.11 |
| Average Product Revenue per Delivered Order |        BRL 137.04 |
| Customers with Delivered Orders             |            93,358 |
| Repeat Customers                            |             2,801 |
| Repeat Customer Rate                        |             3.00% |
| Average Delivery Time                       |        12.56 days |
| On-Time or Early Deliveries                 |            88,644 |
| Late Deliveries                             |             7,826 |
| On-Time or Early Delivery Rate              |            91.89% |

**Revenue definition:** Delivered product revenue is calculated using product item prices for delivered orders. Freight charges are excluded.

**Delivery-rate definition:** The on-time or early delivery rate is calculated using orders with valid delivery dates and estimated delivery dates.

## Analysis Performed

### 1. Sales Analysis

* Monthly sales trends.
* Yearly revenue comparisons.
* Identification of peak sales periods.

### 2. Product Category Analysis

* Revenue by product category.
* Identification of high-revenue categories.
* Comparison of category revenue and item counts.

### 3. Customer Analytics

* Unique customer analysis.
* Single-order and repeat-customer analysis.
* Customer purchasing behavior.

### 4. Payment Analysis

* Analysis of payment methods.
* Comparison of payment values across payment types.

### 5. Delivery Analysis

* Average delivery time.
* On-time, early, and late delivery analysis.
* Identification of delivery-performance trends.

### 6. SQL Analytics

SQL queries were used to analyze orders, customers, payments, product categories, revenue, and delivery performance.

### 7. Big Data Analytics

PySpark was used to load datasets, process related tables, calculate aggregations, and export analytical results as CSV files.

## Machine Learning Model

A Random Forest Regressor was developed as a baseline model to estimate delivery time.

### Model Configuration

* Algorithm: Random Forest Regression
* Number of estimators: 100
* Maximum depth: 15
* Random state: 42

### Model Evaluation

Previously recorded development results:

| Evaluation Metric              |    Result |
| ------------------------------ | --------: |
| Mean Absolute Error (MAE)      | 5.03 days |
| Root Mean Squared Error (RMSE) | 8.03 days |
| R² Score                       |    0.2613 |

The recorded results indicate that the baseline model has limited predictive performance. Further feature engineering, model comparison, and validation are required to improve reliability.

**Model file:** `models/delivery_time_model.pkl`

The model should be evaluated using the final executed notebook results before these metrics are treated as final.

## Interactive Dashboard

The project includes a Streamlit dashboard located at:

`dashboards/app.py`

The dashboard provides:

* Date-range filters.
* Product-category filters.
* Key performance indicators.
* Monthly revenue trends.
* Product category analysis.
* Customer behavior insights.
* Payment method analysis.
* Delivery performance analysis.

The dashboard supports interactive exploration of the analyzed data.

## How to Run the Project

### Prerequisites

Install the following software as required by the components you want to run:

* Python
* MySQL Server, for SQL analysis and database import
* Java Development Kit (JDK), for PySpark
* Git, for version control

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd cognevance_bigDataAnalytics
```

Replace `<your-github-repository-url>` with the actual repository URL.

### 2. Install Dependencies

Ensure that `requirements.txt` exists in the project root directory.

```bash
python -m pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard

From the project root directory, execute:

```bash
python -m streamlit run dashboards/app.py
```

Open the local address displayed in the terminal. Streamlit commonly uses:

`http://localhost:8501`

### 4. Run the PySpark Analysis

Configure Java and the required environment variables for your system, then run:

```bash
python src/pyspark_analysis.py
```

The generated analytical CSV files are saved under `outputs/pyspark/`.

### 5. Run the SQL Analysis

Ensure MySQL Server is running and the required database and tables have been created.

Execute the SQL queries in:

`sql/ecommerce_analysis.sql`

The database connection details and table names must match your local MySQL configuration.

## Limitations

* The dataset contains historical transactions rather than live e-commerce activity.
* Missing values and incomplete delivery records require careful handling.
* The baseline delivery-time prediction model has limited predictive performance.
* Customer repeat-purchase analysis depends on the selected customer identifier and order filters.
* Results can vary when different filters, date conditions, or revenue definitions are used.
* The project demonstrates analytical processing but is not a deployed production system.

## Future Improvements

* Improve delivery-time prediction through feature engineering and model tuning.
* Compare Random Forest with additional regression models.
* Add further customer segmentation analysis.
* Improve dashboard interactivity and reporting.
* Validate all KPIs across SQL, Pandas, PySpark, and Streamlit.
* Automate the data-processing workflow.
* Add dashboard screenshots and a system architecture diagram.
* Deploy the dashboard for wider access.

## Conclusion

This project demonstrates how SQL, Python, PySpark, machine learning, and interactive visualization can be combined to analyze e-commerce data.

It generates insights into sales performance, product categories, customer purchasing behavior, payment preferences, and delivery operations. The project also provides a baseline approach to delivery-time prediction and a dashboard for exploring business metrics.

The analysis provides a foundation for further predictive modeling and data-driven business decision-making.
