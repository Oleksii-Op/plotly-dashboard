import pandas as pd
from typing import Tuple
import warnings
from dash_app.core.config import settings


warnings.simplefilter(action="ignore", category=FutureWarning)


class LoadDataframes:

    def __init__(self):
        self.nps_prices = self._load_prices()
        self.production = self._load_production()
        self.production_nps = pd.concat(
            [
                self.production.iloc[:-2],
                self.nps_prices["NPS Estonia"],
            ],
            axis=1,
        )

    @classmethod
    def _load_prices(cls):
        nps = pd.read_csv(
            settings.datafiles.nps_file,
        )
        nps["Date"] = pd.date_range(
            start="2021-12-31 22:00",
            end="2023-12-31 21:00",
            tz="UTC",
            freq="h",
        )
        nps["Date"] = nps["Date"].dt.tz_convert(
            "Europe/Tallinn",
        )
        nps.set_index(
            "Date",
            inplace=True,
        )
        return nps

    @classmethod
    def _load_production(cls):
        production_df = pd.read_csv(settings.datafiles.est_power_prod_file)
        # Setting time as datetime64 with local zone
        production_df["Date"] = pd.date_range(
            start="2021-12-31 22:00",
            end="2023-12-31 23:00",
            tz="UTC",
            freq="h",
        )
        production_df["Date"] = production_df["Date"].dt.tz_convert(
            "Europe/Tallinn",
        )
        # Setting column Date as the index
        production_df.set_index(
            "Date",
            inplace=True,
        )
        return production_df

    @property
    def df3_new(self) -> pd.DataFrame:
        return self.production_nps

    @property
    def power_production(self) -> pd.DataFrame:
        return self.production

    @property
    def power_prod_and_prices(self) -> pd.DataFrame:
        return self.production_nps

    @property
    def all_nps_prices(
        self,
    ) -> Tuple[pd.DataFrame, list[str], list]:
        months_2022_2023 = [
            f"{year}-{month:02}" for year in range(2022, 2024) for month in range(1, 13)
        ]
        month_names = list(
            self.nps_prices.index.month_name().unique(),
        )
        return (
            self.nps_prices,
            months_2022_2023,
            month_names,
        )

    def total_prod_by_year(
        self,
        year: str,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        total_power_production_2023 = (
            self.production[f"{year}-1-1":f"{year}-12-31"].resample("YE").sum()
        )

        # Inverting the DataFrame to create a new one
        df_inverted = total_power_production_2023.T
        total_gw = pd.DataFrame()
        total_gw.index = df_inverted.index
        total_gw["Production"] = (
            df_inverted.values // 1000
        )  # Converting MegaWatts to GigaWatts

        # Selecting and separating renewables and fossil for 2023
        fossil_total = self.production[f"{year}-01-01":f"{year}-12-31"][
            [
                "Fossil Oil shale",
                "Fossil Peat",
                "Fossil Coal-derived gas",
                "Fossil Gas",
                "Waste",
            ]
        ]
        renewable_total = self.production[f"{year}-01-01":f"{year}-12-31"][
            [
                "Biomass",
                "Wind Onshore",
                "Solar",
                "Other renewable",
                "Hydro Run-of-river and poundage",
            ]
        ]

        total_ren_fossil = pd.DataFrame()
        total_ren_fossil["Fossil"] = (
            fossil_total.sum(axis=1).resample("YE").sum() // 1000
        )  # Converting MegaWatts to GigaWatts
        total_ren_fossil["Renewable"] = (
            renewable_total.sum(axis=1).resample("YE").sum() // 1000
        )  # Converting MegaWatts to GigaWatts
        total_ren_fossil = total_ren_fossil.T
        return total_gw, total_ren_fossil

    def get_renewables_fossil(
        self,
    ) -> Tuple[dict[str : pd.DataFrame], dict[str : pd.DataFrame]]:
        # Создание словаря для хранения результатов
        data_dict = {}
        prices_dict = {}

        # Цикл для обработки данных за разные года
        for year in [2022, 2023]:
            # Выбор данных за текущий год
            fossil_year = self.production_nps[
                [
                    "Fossil Oil shale",
                    "Fossil Peat",
                    "Fossil Coal-derived gas",
                    "Fossil Gas",
                    "Waste",
                ]
            ][f"{year}-01-01":f"{year}-12-31"]
            renewable_year = self.production_nps[
                [
                    "Biomass",
                    "Wind Onshore",
                    "Solar",
                    "Other renewable",
                    "Hydro Run-of-river and poundage",
                ]
            ][f"{year}-01-01":f"{year}-12-31"]
            prices_year = self.production_nps["NPS Estonia"][
                f"{year}-01-01":f"{year}-12-31"
            ]

            # Ресемплирование и вычисление среднего значения
            fossil_resampled = fossil_year.resample("5D").mean()
            renewable_resampled = renewable_year.resample("5D").mean()
            prices_resampled = prices_year.resample("5D").mean()

            # Создание DataFrame для смешанных данных
            df_mixed_year = pd.DataFrame()
            df_mixed_year["Fossil"] = fossil_resampled.sum(axis=1)
            df_mixed_year["Renewable"] = renewable_resampled.sum(axis=1)

            # Добавление в словарь
            data_dict[f"df6_mixed_{year}"] = df_mixed_year
            prices_dict[f"{year}"] = prices_resampled

        return data_dict, prices_dict


data = LoadDataframes()
