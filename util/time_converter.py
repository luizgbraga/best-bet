class TimeConverter:
    @staticmethod
    def str_to_float(time):
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)

        return hour + (minute / 60)

    @staticmethod
    def all_times():
        times = []
        for hour in range(9):
            times.append(f"0{hour}:00")
            times.append(f"0{hour}:30")
        for hour in range(9, 24):
            times.append(f"{hour}:00")
            times.append(f"{hour}:30")
        return times
