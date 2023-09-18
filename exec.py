import sys

#
args = sys.argv

dictionary = {}
print(args)

# Iterate over the array
for item in args:
    # Split each item on the '=' character
    parts = item.split('=')

    # Check if it's in the 'key=value' format
    if len(parts) == 2:
        key, value = parts
        # Add it to the dictionary
        dictionary[key] = value

print("Hello world")
if __name__ == "__main__":
    print(dictionary)
    # if 'exec' in dictionary:
    #     output = subprocess.run(dictionary['exec'], capture_output=True, shell=True)
    #     print(output.stdout)
    #     print(output.stderr)

    input("Wait")
