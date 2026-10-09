# E-Commerce Customer Analytics & Predictive Intelligence

**Project:** Big Data Analytics & Predictive Intelligence
**Organization:** Cognevance Technologies
**Dataset:** Olist Brazilian E-Commerce Public Dataset
**Domain:** E-Commerce, Big Data Analytics and Machine Learning

---

## 1. Executive Summary

This project analyzes e-commerce data to identify sales trends, product category performance, customer purchasing behavior, and delivery performance. It combines Python, SQL, PySpark, Machine Learning, and Streamlit to transform raw transaction data into useful business insights.

A Random Forest Regression model was developed to predict delivery time. An interactive Streamlit dashboard presents key business indicators and analytical visualizations.

The main objective is to support data-driven business decisions through descriptive analytics and predictive intelligence.

## 2. Problem Statement

E-commerce platforms generate large amounts of data related to orders, customers, products, payments, and deliveries.

Analyzing this information manually makes it difficult to understand sales trends, identify important product categories, measure customer retention, and monitor delivery performance.

This project addresses these challenges by developing a data analytics workflow and a baseline machine learning model.

## 3. Project Objectives

* Analyze e-commerce transaction data.
* Clean and preprocess datasets.
* Combine related datasets for deeper analysis.
* Perform SQL-based business analysis.
* Use PySpark for large-scale data processing.
* Analyze monthly and yearly sales trends.
* Identify high-revenue product categories.
* Study customer repeat-purchase behavior.
* Analyze delivery performance.
* Develop a Random Forest Regression model for delivery-time prediction.
* Create an interactive dashboard.
* Generate business insights and recommendations.

## 4. Dataset Description

The project uses the Olist Brazilian E-Commerce Public Dataset, which contains information about orders, customers, products, sellers, payments, reviews, and geographical locations.

The main datasets loaded by the PySpark workflow were:

| Dataset               | Number of rows |
| --------------------- | -------------: |
| Orders                |         99,441 |
| Order Items           |        112,650 |
| Products              |         32,951 |
| Customers             |         99,441 |
| Category Translations |             71 |

The datasets were stored as CSV files and processed using Python and PySpark.

## 5. Technologies Used

* **Python:** Main programming language.
* **Pandas:** Data manipulation and CSV processing.
* **NumPy:** Numerical calculations.
* **PySpark:** Data processing and aggregations.
* **SQL/MySQL:** Relational queries and business analysis.
* **Scikit-learn:** Machine learning and model evaluation.
* **Random Forest Regression:** Delivery-time prediction.
* **Joblib:** Saving the trained machine learning model.
* **Streamlit:** Interactive dashboard.
* **Plotly:** Interactive charts.
* **Jupyter Notebook:** Data analysis and model development.
* **Visual Studio Code:** Project development environment.

## 6. Data Cleaning and Preprocessing

The PySpark workflow performs the following preprocessing operations:

1. Loads the required CSV datasets.
2. Removes records without required order and product identifiers.
3. Removes duplicate records using selected identifier columns.
4. Converts purchase and delivery dates into timestamp formats.
5. Converts product prices and freight values into numeric formats.
6. Filters invalid negative or missing product prices from the selected analysis.
7. Joins orders with order items, product information, and category translations.
8. Creates month and year features for trend analysis.
9. Filters delivered orders for delivered-product-revenue calculations.

These operations prepare the data for consistent analysis.

## 7. SQL Analytics

SQL queries were executed using MySQL to analyze the e-commerce data.

The analysis covered:

* Total orders and order statuses.
* Customer counts.
* Payment methods and payment values.
* Product category revenue.
* Monthly delivered-product revenue.
* Delivery duration.
* Customer geographical distribution.

A total of 13 SQL queries were executed during development.

## 8. Business KPIs

The following results were produced by the PySpark analysis:

| KPI                             |            Result |
| ------------------------------- | ----------------: |
| Total Orders                    |            99,441 |
| Unique Customers                |            96,096 |
| Delivered Orders                |            96,478 |
| Delivered Product Revenue       | BRL 13,221,498.11 |
| Average Delivery Time           |        12.56 days |
| Customers with Delivered Orders |            93,358 |
| Repeat Customers                |             2,801 |
| Repeat Customer Rate            |             3.00% |

**Revenue definition:** Delivered product revenue is calculated by summing the product item price for delivered orders. Freight charges are excluded from this measure.

## 9. Monthly and Yearly Sales Analysis

### Monthly Analysis

The highest monthly delivered-product revenue in the available PySpark output occurred in November 2017.

* **Peak month:** November 2017
* **Delivered product revenue:** BRL 987,765.37
* **Delivered orders:** 7,289

Monthly sales analysis helps identify changes in demand and periods that may require additional inventory or operational planning.

### Yearly Analysis

| Year | Delivered Product Revenue (BRL) | Delivered Orders |
| ---- | ------------------------------: | ---------------: |
| 2016 |                       40,470.98 |              267 |
| 2017 |                    5,962,902.01 |           43,428 |
| 2018 |                    7,218,125.12 |           52,783 |

These results are based on the current analysis, which includes delivered orders with valid purchase dates.

## 10. Product Category Analysis

The following categories had the highest delivered-product revenue in the PySpark analysis:

| Product Category          | Revenue (BRL) | Order Item Count |
| ------------------------- | ------------: | ---------------: |
| Health and Beauty         |  1,233,131.72 |            9,465 |
| Watches and Gifts         |  1,166,176.98 |            5,859 |
| Bed, Bath and Table       |  1,023,434.76 |           10,953 |
| Sports and Leisure        |    954,852.55 |            8,431 |
| Computers and Accessories |    888,724.61 |            7,644 |

These categories represent important revenue contributors in the analyzed dataset.

## 11. Customer Purchase Behavior

Customer purchase behavior was analyzed by grouping delivered orders using the unique customer identifier.

The results were:

* Customers with delivered orders: 93,358
* Repeat customers: 2,801
* Single-order customers: 90,557
* Repeat customer rate: 3.00%

The repeat customer rate is based on customers with delivered orders in this analysis. It can help the business assess customer retention and identify opportunities for customer engagement.

## 12. Delivery Performance Analysis

The delivery analysis calculates the time between purchase and actual delivery.

### Average Delivery Time

The average delivery time was **12.56 days** across 96,470 delivered orders with valid purchase and delivery timestamps.

### Delivery Status

| Delivery Status  | Number of Orders |
| ---------------- | ---------------: |
| On Time or Early |           88,644 |
| Late             |            7,826 |

These results are based on orders with valid actual and estimated delivery dates.

Monitoring delivery performance can help identify operational problems and improve customer satisfaction.

## 13. Machine Learning Model

### Model Used

A Random Forest Regression model was developed using Scikit-learn to estimate delivery time.

The model configuration was:

* Algorithm: Random Forest Regression
* Number of trees: 100
* Maximum depth: 15
* Random state: 42
* Parallel processing: Enabled using `n_jobs=-1`

### Training

The model was trained using the training dataset:

`model.fit(X_train, y_train)`

### Prediction

Predictions were generated for the test dataset:

`y_pred = model.predict(X_test)`

### Evaluation Metrics

The model was evaluated using:

* **Mean Absolute Error (MAE):** Average absolute prediction error.
* **Root Mean Squared Error (RMSE):** Measures prediction error while penalizing larger errors more strongly.
* **R-squared (R²):** Indicates how much of the target variation is explained by the model.

Previously recorded development results were:

| Metric | Recorded Result |
| ------ | --------------: |
| MAE    |       5.03 days |
| RMSE   |       8.03 days |
| R²     |          0.2613 |

**Important:** Verify these values against the final executed notebook output before submitting the report. The recorded R² indicates that this baseline model has room for improvement, so predictions should be treated as estimates rather than exact delivery promises.

The trained model is saved as:

`models/delivery_time_model.pkl`

## 14. PySpark Analytics

PySpark was used to process the datasets and generate aggregated business results.

The workflow includes:

* Loading datasets.
* Data cleaning and preprocessing.
* Joining related datasets.
* Calculating business KPIs.
* Monthly sales analysis.
* Yearly sales analysis.
* Product category revenue analysis.
* Customer purchase behavior.
* Delivery-time analysis.
* Delivery-performance analysis.

The generated output files are saved in:

`outputs/pyspark/`

The six exported CSV files are:

1. `monthly_sales.csv`
2. `category_revenue.csv`
3. `customer_behavior.csv`
4. `delivery_summary.csv`
5. `yearly_sales.csv`
6. `delivery_performance.csv`

## 15. Interactive Dashboard

The project includes a Streamlit dashboard located at:

`dashboards/app.py`

The dashboard includes:

* Key performance indicators.
* Date and category filters.
* Monthly sales trends.
* Top product categories.
* Customer purchase behavior.
* Payment method analysis.
* Delivery performance.

The dashboard allows users to explore the data interactively and understand business performance.

## 16. Business Insights and Recommendations

Based on the current analysis, the following recommendations can be considered:

1. **Inventory planning:** Monitor demand for high-revenue categories such as Health and Beauty, Watches and Gifts, and Bed, Bath and Table.
2. **Delivery improvement:** Investigate late deliveries by seller, region, and order period.
3. **Customer retention:** Explore appropriate engagement strategies to encourage satisfied customers to purchase again.
4. **Sales planning:** Use monthly and yearly trends to support stock and operational planning.
5. **Model improvement:** Evaluate additional features and compare the Random Forest model against simpler baseline models.
6. **KPI consistency:** Use consistent definitions across SQL, Python, PySpark, and dashboard outputs.
7. **Performance monitoring:** Track delivery time and late-delivery rates over time to identify operational changes.

These are recommendations derived from the available results; their business impact should be validated before implementation.

## 17. System Workflow

The project workflow is:

**CSV Datasets → Data Cleaning → Data Integration → SQL/Python/PySpark Analysis → KPI Generation → Machine Learning Training and Evaluation → Saved Model → Streamlit Dashboard → Business Insights and Recommendations**

## 18. Limitations and Future Improvements

The project can be improved in the following ways:

* Validate model features and target construction.
* Ensure that model training and testing avoid data leakage.
* Compare the model against baseline regression approaches.
* Improve prediction accuracy through feature engineering and model tuning.
* Add model predictions to the dashboard if required.
* Reconcile KPI definitions across all tools.
* Add dashboard screenshots and an architecture diagram.
* Complete the final project presentation.
* Verify the project setup instructions and dependencies.

## 19. Conclusion

This project combines e-commerce data analysis, SQL, PySpark, machine learning, and interactive visualization to study sales, product categories, customer purchasing behavior, and delivery performance.

The analysis produces business KPIs and exported datasets that can support operational decision-making. The Random Forest model provides a baseline approach to delivery-time prediction, while the Streamlit dashboard enables interactive exploration of business results.

Further model validation, documentation, and final deliverable checks will help prepare the project for submission.

## 20. Final Submission Checklist

* [ ] Verify the final ML evaluation metrics.
* [ ] Document the exact model features and target.
* [ ] Include the SQL analysis script.
* [ ] Include the PySpark source code and exported CSV files.
* [ ] Add screenshots of the working dashboard.
* [ ] Confirm the required dashboard format with the internship instructions.
* [ ] Verify the root-level `requirements.txt` file.
* [ ] Update the README with setup and execution instructions.
* [ ] Prepare the final presentation.
* [ ] Confirm that the GitHub repository contains the intended deliverables.
