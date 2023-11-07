from flask import Flask
from flask import request, render_template, send_from_directory, redirect, url_for, flash
from flask import session

from data.collect_data import DataCollector
from data.process_data import DataProcessor
from util.time_converter import TimeConverter
from network.network import Network

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    clubs = DataCollector.get_all_clubs()
    if request.method == 'POST':
        home_team_id = DataCollector.get_club_id(request.form['home-team'])
        visit_team_id = DataCollector.get_club_id(request.form['visit-team'])
        hour = TimeConverter.str_to_float(request.form['hour'])
        round = int(request.form['round'])
        input_data = DataProcessor.format_input_data(home_team_id, visit_team_id, hour, round)
        net = Network([len(input_data), 60, 9])
        training_data = DataCollector.generate_training_and_test_data()
        train = DataProcessor.generate_tuple(training_data['input_training_data'], training_data['output_training_data'])
        test = DataProcessor.generate_tuple(training_data['input_testing_data'], training_data['output_testing_data'])
        print(train, test)
        net.SGD(train, 30, 10, 3.0, test_data=test)
        output = net.feedforward(input_data)
        print(output)
        return render_template('inputs.html')
    
    return render_template('inputs.html', home_teams=clubs, visit_teams=clubs, hours=TimeConverter.all_times())

if __name__ == "__main__":
    app.run(debug=True)