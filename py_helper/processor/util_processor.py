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
