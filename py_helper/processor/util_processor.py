class UtilProcessor:
    @staticmethod
    def round_days(days: int):
        year = 0
        month = 0
        day = days

        while day >= 365:
            year += 1
            day -= 365

        while day >= 30:
            month += 1
            day -= 30

        day = int(day)

        return f"{year}y {month}m {day}d"

    @staticmethod
    def count_down_timer_shell_string(message, count):
        return f"""
        printf "\\n%s" "{message}";
        for ((i = {count} - 1; i >= 0; i = i - 1)); do
            printf "\\033[0;31m %03ds\b\b\b\b\b\\033[0m" "$i"
            sleep 1s
        done
        printf "\\n"
        """

    @staticmethod
    def key_value_exists_in_map(map_object, key, value):
        for item in map_object:
            if item[key] == value:
                return True
        return False

    @staticmethod
    def remove_map_from_array_where_key_value(array_object, key, value):
        temp_array = []
        for map_object in array_object:
            if map_object[key] != value:
                temp_array.append(map_object)
        return temp_array
