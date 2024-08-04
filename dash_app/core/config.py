from pydantic_settings import BaseSettings

from pathlib import Path


class DataFiles(BaseSettings):
    est_power_prod_file: str = str(
        Path(__file__).parent.parent / "est_power_production_2022-2023.csv",
    )
    nps_file: str = str(
        Path(__file__).parent.parent / "nps_2022_2023.csv",
    )


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    datafiles: DataFiles = DataFiles()


settings = Settings()
