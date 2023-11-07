import pandas as pd
from util.time_converter import TimeConverter

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

        testing_data = df.sample(frac=0.1)
        training_data = df.drop(testing_data.index)

        input_columns = ['hora', 'rodada'] + [f'id_{i + 1}' for i in range(len(self.club_ids))]
        output_columns = ["bs", "mt1g", "mt2g", "mt3g", "mt4g", "mt5g", "dgt2", "dgt3", "zg"]

        return  {
                    'input_training_data': training_data[input_columns],
                    'output_training_data': training_data[output_columns],
                    'input_testing_data': testing_data[input_columns],
                    'output_testing_data': testing_data[output_columns]
                }
