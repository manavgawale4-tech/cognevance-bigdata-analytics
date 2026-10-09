import pandas as pd
import mysql.connector
from pathlib import Path
from getpass import getpass

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_DIR / "dataset"

# MySQL connection
password = getpass("Enter your MySQL root password: ")

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="ecommerce_analytics"
    )

    cursor = connection.cursor()
    print("\nConnected to MySQL successfully!")

    # Import every CSV file from the dataset folder
    csv_files = sorted(DATASET_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in: {DATASET_DIR}")

    for csv_file in csv_files:
        table_name = csv_file.stem

        print(f"\nImporting: {csv_file.name}")

        # Read large CSV files in chunks
        first_chunk = True

        for chunk in pd.read_csv(csv_file, chunksize=10000):
            # Convert pandas missing values to SQL NULL
            chunk = chunk.astype(object).where(pd.notna(chunk), None)

            columns = list(chunk.columns)

            # Safely quote column names
            quoted_columns = ", ".join(
                f"`{column.replace('`', '``')}`" for column in columns
            )

            create_columns = ", ".join(
                f"`{column.replace('`', '``')}` LONGTEXT"
                for column in columns
            )

            if first_chunk:
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                cursor.execute(
                    f"CREATE TABLE `{table_name}` ({create_columns})"
                )
                connection.commit()
                first_chunk = False

            placeholders = ", ".join(["%s"] * len(columns))
            insert_query = (
                f"INSERT INTO `{table_name}` "
                f"({quoted_columns}) VALUES ({placeholders})"
            )

            values = [
                tuple(None if pd.isna(value) else value for value in row)
                for row in chunk.itertuples(index=False, name=None)
            ]

            cursor.executemany(insert_query, values)
            connection.commit()

        print(f"Imported successfully: {table_name}")

    print("\nAll CSV files processed!")

except mysql.connector.Error as error:
    print(f"\nMySQL error: {error}")

except Exception as error:
    print(f"\nError: {error}")

finally:
    if "connection" in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")