import pandas as pd
from collect_data import DataCollector


class DataProcessor:
    @staticmethod
    def dataframe_to_array_transformer(dataframe):
        """
        dataframe: pandas.DataFrame

        returns: [rows]
            rows: A list of values for each column
        """

        matrix = dataframe.values.tolist()

        return matrix
    
    @staticmethod
    def generate_tuple(input_data, output_data):
        input_array = DataProcessor.dataframe_to_array_transformer(input_data)
        output_array = DataProcessor.dataframe_to_array_transformer(output_data)

        try:
            input_and_output_list = []
            for index in range(len(input_array)):
                input_and_output_list.append((input_array[index], output_array[index]))

            return input_and_output_list
        except IndexError:
            print("The size of input_data and output_data mismatched.")
            return None
        
    @staticmethod
    def output_to_array(output):
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

        bets_to_do = []

        for key, value in bets:
            if value == 1:
                bets_to_do.append(key)

        return bets_to_do
    
    @staticmethod
    def format_input_data(home_club_id, visitor_club_id, hour, round):
        input_data = [[hour/24], [round/38]]

        if not DataCollector.club_ids:
            DataCollector.update_club_id()

        for id in range(len(DataCollector.club_ids)):
            if home_club_id == id + 1 or visitor_club_id == id + 1:
                input_data.append([1])
            else:
                input_data.append([0])

        return input_data