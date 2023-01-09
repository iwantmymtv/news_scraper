import os
import json

def append_to_json_file(articles, json_name:str):
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, 'jsons', f'{json_name}.json')
    print(articles)
    with open(file_path, 'r+') as f:
        # Load the existing data from the file
        existing_data = json.load(f)

        # Append the new articles to the existing data
        existing_data['articles'] += articles

        # Seek to the beginning of the file
        f.seek(0)

        # Write the modified data back to the file
        json.dump(existing_data, f)