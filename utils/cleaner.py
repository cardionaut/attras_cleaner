import pandas as pd
import numpy as np
from loguru import logger


class Cleaner:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.events = None

    def __call__(self) -> pd.DataFrame:
        self.strings_to_numbers()

        return self.data
    
    def strings_to_numbers(self):
        rename_dict = {
            'Unchecked': 0,
            'Checked': 1,
            'No': 0,
            'Yes': 1,
            'I': 1,  # NYHA categories
            'I-II': 2,
            'II': 3,
            'II-III': 4,
            'III': 5,
            'III-IV': 6,
            'IV': 7,
            'I°': 1,  # insufficiency grades
            'II°': 2,
            'III°': 3,
            'IV°': 4,
            '1VD': 1,
            '2VD': 2,
            '3VD': 3,
            'none': np.nan,
        }

        for old, new in rename_dict.items():  # faster than Series.replace for len(data) > 100
            self.data = self.data.replace(old, new, regex=False)