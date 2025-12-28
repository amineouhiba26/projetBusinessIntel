from extract.extract_raw import extract
from transform.transform_dw import transform
from load.load_dw import load

def run_etl():
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)
    print("✅ ETL terminé avec succès")

if __name__ == "__main__":
    run_etl()
