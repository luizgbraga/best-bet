from data.process_data import DataProcessor
from network.network import Network


class Train:
    def __init__(self, csv_name):
        self.data_processor = DataProcessor(csv_name)
        self.net = Network([self.data_processor.get_input_size(), 60, 9], random=True)

    def train(self):
        train, test = self.data_processor.generate_tuples()
        self.net.SGD(train, 30, 10, 3.0, test_data=test)
