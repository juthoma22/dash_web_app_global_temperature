import sys
import kaggle
import pandas as pd
import numpy as np


class DataHandler:
    def __init__(self):
        self.dataset = "berkeleyearth/climate-change-earth-surface-temperature-data"
        self.path = "./kaggle"
        self.csv_file = "./kaggle/GlobalLandTemperaturesByCountry.csv"

    def download_dataset(self):
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            self.dataset, path=self.path, force=True, unzip=True
        )

    def open_files(self):
        df_global_temperatures_country = pd.read_csv(self.csv_file)
        return df_global_temperatures_country

    def read_files(self, second_try=False):
        """
        read_files(self, second_try) -> (pd.df, [str], [str])

        Reading file in the path, stored in self.path, if not existant download them from self.url using the kaggle API.
        Returning a pandas dataframe as well as a list of years and a list of countries in that dataframe.

        second_try -- Wether or not it's being called the second time, used to try twice when kaggle API times out -> Bool
        """
        try:
            df_country = self.open_files()

        except (FileNotFoundError, OSError):
            # if files don't exist or are locked, download them
            try:
                self.download_dataset()
                df_country = self.open_files()
            except kaggle.rest.ApiException as ex:
                if ex.status == 403:
                    # Forbidden
                    sys.exit(
                        "No files found locally and download forbidden, check credentials and url"
                    )
                elif ex.status == 401:
                    # Unauthorized
                    sys.exit(
                        "No files found locally and no credentials found, check credentials"
                    )
                elif ex.status == 404:
                    # Not Found
                    sys.exit("No files found locally and online, check url")
                elif ex.status == 408:
                    # Timed out
                    if second_try:
                        sys.exit(
                            "No files found locally and connection to kaggle timed out"
                        )
                    else:
                        self.read_files(second_try=True)
                else:
                    sys.exit(
                        f"No files found locally and kaggle returned status {ex.status}"
                    )
            except (FileNotFoundError, OSError) as ex:
                sys.exit(f"Downloaded files not found or corrupted {type(ex)}")

        df_country = df_country.dropna()

        # Extract the years from df['dt']
        years = np.unique(df_country["dt"].apply(lambda x: x[:4]))

        # Extract the countries from df['Country']
        countries = df_country["Country"].unique()

        return df_country, years, countries
