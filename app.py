from flask import Flask
from flask import request, render_template, send_from_directory, redirect, url_for, flash
from flask import session

from data.collect_data import DataCollector
from data.process_data import DataProcessor
from util.time_converter import TimeConverter
from network.network import Network

app = Flask(__name__)

CSV_NAME = 'brasileirao.csv'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    data_collector = DataCollector(CSV_NAME)
    data_processor = DataProcessor(CSV_NAME)
    if request.method == 'POST':
        home_team_id = data_collector.get_club_id(request.form['home-team'])
        visit_team_id = data_collector.get_club_id(request.form['visit-team'])
        hour = TimeConverter.str_to_float(request.form['hour'])
        round = int(request.form['round'])
        input_data = data_processor.format_input_data(home_team_id, visit_team_id, hour, round)
        net = Network([len(input_data), 60, 9])
        train, test = data_processor.generate_tuples()
        print(train[0], test[0])
        net.SGD(train, 30, 10, 3.0, test_data=test)
        output = net.feedforward(input_data)
        bets = data_processor.output_to_list(output)
        return render_template('outputs.html', bets=bets)
    
    return render_template('inputs.html', home_teams=data_collector.get_club_names(), visit_teams=data_collector.get_club_names(), hours=TimeConverter.all_times())

if __name__ == "__main__":
    app.run(debug=True)