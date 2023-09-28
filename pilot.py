import subprocess
import sys

#
args = sys.argv

dictionary = {}
# print(args)

# Iterate over the array
for item in args:
    # Split each item on the '=' character
    parts = item.split("=")

    # Check if it's in the 'key=value' format
    if len(parts) == 2:
        key, value = parts
        # Add it to the dictionary
        dictionary[key] = value

print(dictionary)


def capture_output():
    output = subprocess.run(dictionary["exec"], capture_output=True)
    output = output.stdout.decode("utf-8")
    print("Output: {}".format(output))


if __name__ == "__main__":
    if "exec" in dictionary:
        print(f"Running command: {dictionary['exec']}")
        """ Working """
        output = subprocess.run(
            dictionary["exec"], shell=True
        )  # capture_output=True, reads the output
    input("Press Any key to continue")
# exit()
