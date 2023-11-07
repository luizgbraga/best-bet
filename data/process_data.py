from data.collect_data import DataCollector
from util.transpose import transpose

class DataProcessor:
    def __init__(self, csv_name):
        self.data_collector = DataCollector(csv_name)

    def generate_tuples(self):
        data = self.data_collector.generate_training_and_test_data()
        input_training_list = [transpose(lst) for lst in data['input_training_data'].values.tolist()]
        output_training_list = [transpose(lst) for lst in data['output_training_data'].values.tolist()]
        input_testing_list = [transpose(lst) for lst in data['input_testing_data'].values.tolist()]
        output_testing_list = [transpose(lst) for lst in data['output_testing_data'].values.tolist()]
        return list(zip(input_training_list, output_training_list)), list(zip(input_testing_list, output_testing_list))
    
    def output_to_list(self, output):
        bets = {}

        bets['Ambos marcam'] = output[0][0]
        bets['Mais de 1 gol'] = output[1][0]
        bets['Mais de 2 gols'] = output[2][0]
        bets['Mais de 3 gols'] = output[3][0]
        bets['Mais de 4 gols'] = output[4][0]
        bets['Mais de 5 gols'] = output[5][0]
        bets['Diferença maior que 2 gols'] = output[6][0]
        bets['Diferença maior que 3 gols'] = output[7][0]
        bets['Sem gols'] = output[8][0]

        bets_to_do = [key for key, value in bets.items() if value == 1]

        return bets_to_do

    def format_input_data(self, home_club_id, visitor_club_id, hour, round):
        input_data = [[hour/24], [round/38]]

        for _, value in self.data_collector.club_ids.items():
            if home_club_id == value or visitor_club_id == value:
                input_data.append([1])
            else:
                input_data.append([0])

        return input_data