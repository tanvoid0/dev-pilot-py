import re


class RegexUtil:
    @staticmethod
    def name_contains_substring(name, substring):
        return name.startswith(substring)

    @staticmethod
    def find_first_in_string(string: str, pattern: str):
        match = re.search(pattern, string)
        if match:
            return match.group(0)
        else:
            return None
