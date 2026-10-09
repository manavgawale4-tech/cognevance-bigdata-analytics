from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = PROJECT_DIR / "dataset"
OUTPUT_DIR = PROJECT_DIR / "outputs" / "pyspark"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Start Spark session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("OlistECommerceAnalytics")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


def export_csv(dataframe, filename):
    """Export a Spark DataFrame to a regular CSV file."""
    output_path = OUTPUT_DIR / filename

    dataframe.toPandas().to_csv(
        output_path,
        index=False
    )

    print(f"CSV saved: {output_path}")


try:

    # --------------------------------------------------
    # 3. Load datasets
    # --------------------------------------------------

    required_files = [
        "olist_orders_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_products_dataset.csv",
        "olist_customers_dataset.csv",
        "product_category_name_translation.csv",
    ]

    missing_files = [
        filename
        for filename in required_files
        if not (DATASET_DIR / filename).exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing dataset files: {missing_files}"
        )

    orders = spark.read.csv(
        str(DATASET_DIR / "olist_orders_dataset.csv"),
        header=True,
        inferSchema=True
    )

    order_items = spark.read.csv(
        str(DATASET_DIR / "olist_order_items_dataset.csv"),
        header=True,
        inferSchema=True
    )

    products = spark.read.csv(
        str(DATASET_DIR / "olist_products_dataset.csv"),
        header=True,
        inferSchema=True
    )

    customers = spark.read.csv(
        str(DATASET_DIR / "olist_customers_dataset.csv"),
        header=True,
        inferSchema=True
    )

    categories = spark.read.csv(
        str(DATASET_DIR / "product_category_name_translation.csv"),
        header=True,
        inferSchema=True
    )

    print("\n========== DATASET ROW COUNTS ==========")

    print("Orders:", orders.count())
    print("Order items:", order_items.count())
    print("Products:", products.count())
    print("Customers:", customers.count())
    print("Categories:", categories.count())

    # --------------------------------------------------
    # 4. Data cleaning and preprocessing
    # --------------------------------------------------

    orders = (
        orders
        .filter(F.col("order_id").isNotNull())
        .dropDuplicates(["order_id"])
        .withColumn(
            "order_purchase_timestamp",
            F.to_timestamp("order_purchase_timestamp")
        )
        .withColumn(
            "order_delivered_customer_date",
            F.to_timestamp("order_delivered_customer_date")
        )
        .withColumn(
            "order_estimated_delivery_date",
            F.to_timestamp("order_estimated_delivery_date")
        )
    )

    order_items = (
        order_items
        .filter(
            F.col("order_id").isNotNull()
            & F.col("product_id").isNotNull()
        )
        .withColumn("price", F.col("price").cast("double"))
        .withColumn(
            "freight_value",
            F.col("freight_value").cast("double")
        )
        .filter(
            F.col("price").isNotNull()
            & (F.col("price") >= 0)
        )
    )

    products = products.dropDuplicates(["product_id"])

    customers = (
        customers
        .filter(F.col("customer_id").isNotNull())
        .dropDuplicates(["customer_id"])
    )

    categories = categories.dropDuplicates(
        ["product_category_name"]
    )

    # --------------------------------------------------
    # 5. Join datasets and engineer features
    # --------------------------------------------------

    sales_data = (
        orders
        .join(order_items, on="order_id", how="inner")
        .join(products, on="product_id", how="left")
        .join(categories, on="product_category_name", how="left")
        .withColumn(
            "category",
            F.coalesce(
                F.col("product_category_name_english"),
                F.lit("Unknown")
            )
        )
        .withColumn(
            "month",
            F.date_format(
                F.col("order_purchase_timestamp"),
                "yyyy-MM"
            )
        )
        .withColumn(
            "year",
            F.year("order_purchase_timestamp")
        )
    )

    delivered_sales = sales_data.filter(
        F.col("order_status") == "delivered"
    )

    # --------------------------------------------------
    # 6. Business KPIs
    # --------------------------------------------------

    total_orders = orders.select("order_id").distinct().count()

    unique_customers = (
        customers
        .select("customer_unique_id")
        .distinct()
        .count()
    )

    delivered_orders_count = (
        orders
        .filter(F.col("order_status") == "delivered")
        .select("order_id")
        .distinct()
        .count()
    )

    delivered_revenue = (
        delivered_sales
        .agg(F.sum("price").alias("revenue"))
        .first()["revenue"]
    )

    print("\n========== BUSINESS KPIs ==========")
    print("Total orders:", total_orders)
    print("Unique customers:", unique_customers)
    print("Delivered orders:", delivered_orders_count)
    print(
        "Delivered product revenue (BRL):",
        round(delivered_revenue or 0, 2)
    )

    # --------------------------------------------------
    # 7. Monthly sales analysis
    # --------------------------------------------------

    monthly_sales = (
        delivered_sales
        .filter(F.col("month").isNotNull())
        .groupBy("month")
        .agg(
            F.round(F.sum("price"), 2)
            .alias("product_revenue_brl"),
            F.countDistinct("order_id")
            .alias("delivered_orders")
        )
        .orderBy("month")
    )

    print("\n========== MONTHLY SALES ==========")
    monthly_sales.show(30, truncate=False)

    export_csv(monthly_sales, "monthly_sales.csv")

    # --------------------------------------------------
    # 8. Product category revenue
    # --------------------------------------------------

    category_revenue = (
        delivered_sales
        .groupBy("category")
        .agg(
            F.round(F.sum("price"), 2)
            .alias("product_revenue_brl"),
            F.count("*").alias("order_item_count")
        )
        .orderBy(F.desc("product_revenue_brl"))
    )

    print("\n========== TOP PRODUCT CATEGORIES ==========")
    category_revenue.show(10, truncate=False)

    export_csv(category_revenue, "category_revenue.csv")

    # --------------------------------------------------
    # 9. Customer purchase behavior
    # --------------------------------------------------

    customer_behavior = (
        orders
        .filter(F.col("order_status") == "delivered")
        .join(
            customers.select(
                "customer_id",
                "customer_unique_id"
            ),
            on="customer_id",
            how="inner"
        )
        .groupBy("customer_unique_id")
        .agg(
            F.countDistinct("order_id").alias("order_count")
        )
    )

    customer_summary = customer_behavior.agg(
        F.count("*").alias(
            "customers_with_delivered_orders"
        ),
        F.sum(
            F.when(F.col("order_count") > 1, 1).otherwise(0)
        ).alias("repeat_customers"),
        F.sum(
            F.when(F.col("order_count") == 1, 1).otherwise(0)
        ).alias("single_order_customers")
    )

    customer_summary = customer_summary.withColumn(
        "repeat_customer_rate_percent",
        F.round(
            F.col("repeat_customers") * 100
            / F.when(
                F.col("customers_with_delivered_orders") > 0,
                F.col("customers_with_delivered_orders")
            ),
            2
        )
    )

    print("\n========== CUSTOMER BEHAVIOR ==========")
    customer_summary.show(truncate=False)

    export_csv(customer_summary, "customer_behavior.csv")

    # --------------------------------------------------
    # 10. Delivery-time analysis
    # --------------------------------------------------

    delivery_analysis = (
        orders
        .filter(
            (F.col("order_status") == "delivered")
            & F.col("order_purchase_timestamp").isNotNull()
            & F.col("order_delivered_customer_date").isNotNull()
        )
        .withColumn(
            "delivery_days",
            (
                F.col("order_delivered_customer_date").cast("long")
                - F.col("order_purchase_timestamp").cast("long")
            ) / 86400
        )
        .filter(F.col("delivery_days") >= 0)
    )

    delivery_summary = delivery_analysis.agg(
        F.round(F.avg("delivery_days"), 2)
        .alias("average_delivery_days"),
        F.count("*")
        .alias("orders_with_valid_delivery_dates")
    )

    print("\n========== DELIVERY ANALYSIS ==========")
    delivery_summary.show(truncate=False)

    export_csv(delivery_summary, "delivery_summary.csv")

    # --------------------------------------------------
    # 11. Yearly sales analysis
    # --------------------------------------------------

    yearly_sales = (
        delivered_sales
        .filter(F.col("year").isNotNull())
        .groupBy("year")
        .agg(
            F.round(F.sum("price"), 2)
            .alias("product_revenue_brl"),
            F.countDistinct("order_id")
            .alias("delivered_orders")
        )
        .orderBy("year")
    )

    print("\n========== YEARLY SALES ==========")
    yearly_sales.show(truncate=False)

    export_csv(yearly_sales, "yearly_sales.csv")

    # --------------------------------------------------
    # 12. Delivery performance
    # --------------------------------------------------

    delivery_performance = (
        delivery_analysis
        .filter(
            F.col("order_estimated_delivery_date").isNotNull()
        )
        .withColumn(
            "delivery_status",
            F.when(
                F.col("order_delivered_customer_date")
                <= F.col("order_estimated_delivery_date"),
                "On Time or Early"
            ).otherwise("Late")
        )
        .groupBy("delivery_status")
        .agg(
            F.countDistinct("order_id").alias("order_count")
        )
    )

    print("\n========== DELIVERY PERFORMANCE ==========")
    delivery_performance.show(truncate=False)

    export_csv(
        delivery_performance,
        "delivery_performance.csv"
    )

    # --------------------------------------------------
    # 13. Completion summary
    # --------------------------------------------------

    print("\n========== OUTPUT SUMMARY ==========")
    print("All analytics CSV files saved in:")
    print(OUTPUT_DIR)

    print("\nPySpark analytics completed successfully.")

finally:
    spark.stop()

