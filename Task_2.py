# data_transformer_db.py
import pandas as pd
import logging
import time
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table, Boolean
from sqlalchemy.orm import sessionmaker

# Configure logging for production (file-based logging)
log_file = "data_transformer_db.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_csv_and_store(csv_path, db_uri, chunksize=10000):
    """
    Reads a large CSV file from a local path, performs data transformation and cleaning, and stores the transformed data in a database.

    Args:
        csv_path (str): Path to the local CSV file.
        db_uri (str): Database URI (e.g., 'postgresql://user:password@host:port/database').
        chunksize (int): Number of rows to process in each chunk.
    """
    try:
        if not os.path.exists(csv_path):
            logging.error(f"File not found: {csv_path}")
            return

        engine = create_engine(db_uri)
        metadata = MetaData()

        # Define the database table schema based on your CSV columns
        data_table = Table(
            'processed_data', metadata,
            Column('product_id', Integer, primary_key=True),
            Column('sku_id', Integer),
            Column('platform_commission_rate', Float),
            Column('product_commission_rate', Float),
            Column('bonus_commission_rate', Float),
            Column('venture_category1_name_en', String),
            Column('venture_category2_name_en', String),
            Column('venture_category3_name_en', String),
            Column('venture_category_name_local', String),
            Column('product_name', String),
            Column('description', String),
            Column('brand_name', String),
            Column('seller_name', String),
            Column('seller_url', String),
            Column('product_url', String),
            Column('product_small_img', String),
            Column('product_medium_img', String),
            Column('product_big_img', String),
            Column('image_url_2', String),
            Column('image_url_3', String),
            Column('image_url_4', String),
            Column('image_url_5', String),
            Column('deeplink', String),
            Column('availability', String),
            Column('current_price', Float),
            Column('promotion_price', Float),
            Column('price', Float),
            Column('discount_percentage', Float),
            Column('number_of_reviews', Integer),
            Column('rating_avg_value', Float),
            Column('seller_rating', Float),
            Column('is_free_shipping', Boolean),
            Column('business_type', String),
            Column('business_area', String)
        )

        metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        reader = pd.read_csv(csv_path, chunksize=chunksize)

        for chunk in reader:
            start_time = time.time()

            try:
                numeric_cols = ['platform_commission_rate', 'product_commission_rate', 'bonus_commission_rate',
                                'current_price', 'promotion_price', 'price', 'discount_percentage',
                                'number_of_reviews', 'rating_avg_value', 'seller_rating', 'sku_id', 'product_id']
                for col in numeric_cols:
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

                chunk['is_free_shipping'] = chunk['is_free_shipping'].fillna(0).astype(bool)
                chunk[numeric_cols] = chunk[numeric_cols].fillna(0)
                chunk = chunk.dropna(subset=['product_id', 'sku_id', 'product_name'])

            except KeyError as e:
                logging.error(f"Column missing in chunk: {e}")
                continue
            except Exception as e:
                logging.error(f"Error during data transformation: {e}")
                continue

            try:
                chunk.to_sql('processed_data', engine, if_exists='append', index=False)
            except Exception as e:
                logging.error(f"Error storing data into the database: {e}")
                session.rollback()
                continue

            end_time = time.time()
            logging.info(f"Processed chunk of {len(chunk)} rows in {end_time - start_time:.2f} seconds.")

        session.close()
        logging.info("Data transformation and storage complete.")

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")

# Example usage (replace with your actual input path and database URI)
if __name__ == "__main__":
    csv_path = "Tyroo-dummy-data.csv"
    db_uri = "postgresql://user:password@host:port/database"  # Replace with your PostgreSQL URI
    if not os.path.exists(csv_path):
        print(f"Error: Input CSV file '{csv_path}' not found.")
    else:
        transform_csv_and_store(csv_path, db_uri)