import pandas as pd
import numpy as np
from loguru import logger


class Cleaner:
    def __init__(self, config) -> None:
        file_path = config.file_path
        id_path = config.id_path
        self.config = config
        self.data = pd.read_excel(file_path)
        if id_path is not None:
            self.id = pd.read_excel(id_path)
        self.events = None

    def __call__(self) -> pd.DataFrame:
        if self.config.strings_to_numbers:
            self.strings_to_numbers()
        if self.config.merge_by_id:
            self.merge_by_id()

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

    def merge_by_id(self):
        self.data['Image Name'] = self.extract_TAVI_id(self.data['Image Name'])
        self.data = self.data.rename(columns={'Image Name': 'ID_Imaging'})
        self.data = pd.merge(self.id, self.data, how='left')
        self.data = self.data.drop(columns=['ID_Imaging'])
            
    @staticmethod
    def extract_TAVI_id(col):
        col = col.apply(lambda name: name.split('_')[1])
        col = col.astype(int)
        
        return col