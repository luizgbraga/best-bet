import pandas as pd
from util.time_converter import TimeConverter

'''
This class is responsible for collecting data from a CSV file
It divides the data into training and testing data (70-30 split)
'''
class DataCollector():
    def __init__(self, csv_name):
        self.total_data = pd.read_csv(csv_name)
        self.club_names = self.total_data['mandante'].unique().tolist()
        self.club_ids = { club_name: i + 1 for i, club_name in enumerate(self.club_names) }

    def get_club_id(self, club_name):
        return self.club_ids[club_name]

    def get_club_names(self):
        return sorted(self.club_names)

    def generate_training_and_test_data(self):
        df = self.total_data.copy()
        df['hora'] = df['hora'].map(TimeConverter.str_to_float)/24
        df['rodada'] /= 38

        test = df.sample(frac=0.3)
        train = df.drop(test.index)

        input_columns = ['hora', 'rodada'] + [f'id_{i + 1}' for i in range(len(self.club_ids))]
        output_columns = ['bs', 'mt1g', 'mt2g', 'mt3g', 'mt4g', 'mt5g', 'dgt2', 'dgt3', 'zg']

        test_data = {
            'input': test[input_columns],
            'output': test[output_columns]
        }
        train_data = {
            'input': train[input_columns],
            'output': train[output_columns]
        }

        return  train_data, test_data
