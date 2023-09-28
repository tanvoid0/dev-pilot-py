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
        echo "Just a countdown script, can ignore"
        printf "\\n%s" "{message}";
        for ((i = {count} - 1; i >= 0; i = i - 1)); do
            printf "\\033[0;31m %03ds\b\b\b\b\b\\033[0m" "$i"
            sleep 1s
        done
        printf "\\n"
        """
