import pandas as pd

class DataCollector():
    csv_name = "brasileirao.csv"
    total_data = pd.read_csv(csv_name, index_col='ID')
    club_ids = {}

    @staticmethod
    def update_club_id():
        DataCollector.total_data = pd.read_csv(DataCollector.csv_name)
        club_names = DataCollector.total_data['mandante'].unique().tolist()

        i = 1
        for club in club_names:
            if club not in DataCollector.club_ids.keys():
                DataCollector.club_ids[club] = i
                i += 1

        print(f"Found {len(DataCollector.club_ids.keys())} clubs at {DataCollector.csv_name}.\n\n")

    @staticmethod
    def get_all_clubs():
        if not DataCollector.club_ids:
            DataCollector.update_club_id()
    
        club_names = list(DataCollector.club_ids.keys())
        club_names.sort()

        return club_names
    
    @staticmethod
    def generate_training_and_test_data():
        data_frame = DataCollector.total_data.copy()

        testing_data = data_frame.sample(frac=0.1)
        training_data = data_frame.drop(testing_data.index)
        
        if not DataCollector.club_ids:
            DataCollector.update_club_id()

        input_columns = ['hora', 'rodada']
        for i in range(len(DataCollector.club_ids)):
            input_columns.append(f"id{i+1}")

        output_columns = ["bs", "mt1g", "mt2g", "mt3g",
                          "mt4g", "mt5g", "dgt2", "dgt3",
                          "zero_gols"]
        
        input_training_data = training_data[input_columns]
        output_training_data = training_data[output_columns]
        input_testing_data = testing_data[input_columns]
        output_testing_data = testing_data[output_columns]

        return  {
                    'input_training_data': input_training_data,
                    'output_training_data': output_training_data,
                    'input_testing_data': input_testing_data,
                    'output_testing_data': output_testing_data
                }        
