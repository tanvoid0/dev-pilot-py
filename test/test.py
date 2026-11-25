import json
import random


def generate_random_longs(n, filename):
    chunk_size = 50000  # Number of long integers per chunk
    num_chunks = (n + chunk_size - 1) // chunk_size  # Calculate number of chunks

    # Create and open the GET parameters file
    with open("get-" + filename + ".txt", 'w') as get_file:
        for chunk_index in range(num_chunks):
            start = chunk_index * chunk_size
            end = min(start + chunk_size, n)
            random_longs = [random.randint(0, 2 ** 63 - 1) for _ in range(start, end)]
            get_ids = ','.join(f'{x}' for x in random_longs)
            get_file.write(get_ids + '\n')

    # Create and open the POST body JSON file
    with open("post-" + filename + ".json", 'w') as post_file:
        post_file.write('{"bodyIds": [')  # Start of JSON array

        for chunk_index in range(num_chunks):
            start = chunk_index * chunk_size
            end = min(start + chunk_size, n)
            random_longs = [random.randint(0, 2 ** 63 - 1) for _ in range(start, end)]

            # Convert the chunk of long integers to a JSON array
            chunk_json = json.dumps(random_longs, indent=4)[1:-1]  # Remove outer brackets

            if chunk_index > 0:
                post_file.write(', ')  # Separator between chunks
            post_file.write(chunk_json)

        post_file.write(']}')  # End of JSON array and object


if __name__ == "__main__":
    n = 390  # Number of random long numbers to generate
    filename = "random_longs"  # Base name for output files

    generate_random_longs(n, filename)
    print(f"Generated {n} random long numbers and saved them to get-{filename}.txt and post-{filename}.json.")
