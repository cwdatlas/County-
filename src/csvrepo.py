import pandas as pd
import os
import sys
import logging

logger = logging.getLogger('csv_repo')


class CsvRepo:
    # The CSV repo using a csv file and pandas to easily read and write and write county/city/code information.
    def __init__(self):
        # Reading Data from stated CSV file using pandas
        modpath = os.path.dirname(os.path.abspath(sys.prefix))
        self.file_path = modpath + r"/resources/CountyRepo.csv"
        try:
            logger.debug(f"INIT: Reading CSV from : '{self.file_path}'")
            self.repo = pd.read_csv(self.file_path, skipinitialspace=True)
        except FileNotFoundError:
            logger.error(f"INIT: File not found in path '{self.file_path}'")

        # Fix the DataFrame (I did copy this section from chatGPT. I was having some ISSUES)
        self.repo.columns = [col if not pd.isna(col) else 'YourNewColumnName' for col in self.repo.columns]
        self.repo = self.repo.loc[:, ~self.repo.columns.str.contains('^Unnamed')]

    def add_city(self, city: str, county: str) -> bool:
        # if both city and county exist, then a person cant add another
        if not self.repo['City'].str.lower().isin([city]).any() and self.repo['County'].str.lower().isin([county]).any():
            # find licence plate number to add to the new row
            rows_by_county = self.repo[self.repo['County'].str.contains(county, case=False, na=False)].to_dict(orient='records')
            plate_number = rows_by_county[0]['License Plate Prefix']
            # Append row to csv
            length = len(self.repo)
            self.repo.loc[len(self.repo)] = {'License Plate Prefix': plate_number,
                                             'City': city.capitalize(),
                                             'County': county.capitalize()}
            # Save csv just in case
            self.save_repo()
            # if there is now a city of the name as what was received
            return self.repo['City'].isin([city.capitalize()]).any()
        return False

    # Get_by_* are the different functions that get information from different columns.
    # They all return lists of dictionaries from different columns
    # Returns dictionary of found data.
    def get_by_city(self, city: str) -> dict:
        rows_by_city = self.repo[self.repo['City'].str.contains(city, case=False, na=False)]
        return rows_by_city.to_dict(orient='records')

    def get_by_county(self, county: str) -> dict:
        rows_by_county = self.repo[self.repo['County'].str.contains(county, case=False, na=False)]
        return rows_by_county.to_dict(orient='records')

    def get_by_code(self, code: int) -> dict:
        rows_by_code = self.repo[self.repo['License Plate Prefix'] == code]
        return rows_by_code.to_dict(orient='records')

    def save_repo(self) -> None:
        try:
            self.repo.to_csv(self.file_path, mode='w')
        except FileNotFoundError:
            logger.error(f"save_repo: File could not be written to: '{self.file_path}'")
