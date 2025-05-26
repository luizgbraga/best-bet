from data.collect_data import DataCollector
from util.transpose import df_T

"""
This class is responsible for process the data collected to fit the neural network input
"""


class DataProcessor:
    def __init__(self, csv_name):
        self.data_collector = DataCollector(csv_name)

    def generate_tuples(self):
        train_data, test_data = self.data_collector.generate_training_and_test_data()
        input_train_list = df_T(train_data["input"])
        output_train_list = df_T(train_data["output"])
        input_test_list = df_T(test_data["input"])
        output_test_list = df_T(test_data["output"])
        return list(zip(input_train_list, output_train_list)), list(
            zip(input_test_list, output_test_list)
        )

    def output_to_list(self, output, threshold=0.4):
        bets = {
            "Ambos marcam": output[0][0],
            "Mais de 1 gol": output[1][0],
            "Mais de 2 gols": output[2][0],
            "Mais de 3 gols": output[3][0],
            "Mais de 4 gols": output[4][0],
            "Mais de 5 gols": output[5][0],
            "Diferença maior que 2 gols": output[6][0],
            "Diferença maior que 3 gols": output[7][0],
            "Sem gols": output[8][0],
        }
        bets_to_do = [key for key, value in bets.items() if value > threshold]

        return bets_to_do

    def get_input_size(self):
        return len(self.data_collector.club_ids) + 2

    def format_input_data(self, home_club_id, visitor_club_id, hour, round):
        input_data = [[hour / 24], [round / 38]]

        for _, value in self.data_collector.club_ids.items():
            if home_club_id == value or visitor_club_id == value:
                input_data.append([1])
            else:
                input_data.append([0])

        return input_data
