import os
import random
from datetime import datetime
import pandas as pd

def extract_movie_names(directory_path):
    filenames = os.listdir(directory_path)
    movies = [os.path.splitext(name)[0] for name in filenames]
    return movies

def create_unique_movie_pairs(movie_list):
    pairs = []
    for _ in range(180):
        target = random.choice(movie_list)
        masker = random.choice([m for m in movie_list if m != target])
        pairs.append((target, masker))
    return pairs

def save_to_csv(pairs, save_directory):
    df = pd.DataFrame(pairs, columns=['TargetMovieList', 'MaskerMovieList'])

    # Generate filename with current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"iniList_{current_time}.csv"
    file_path = os.path.join(save_directory, filename)

    df.to_csv(file_path, index=False)

    return file_path

your_target_directory_path = 'C:\\Sudan\\Stimuli\\Screenshots_faces_full_updated'
your_save_directory_path = 'C:\\Sudan\\Stimuli\\initialization_data'

movies = extract_movie_names(your_target_directory_path)
movie_pairs = create_unique_movie_pairs(movies)

csv_file_path = save_to_csv(movie_pairs, your_save_directory_path)

print(f"CSV file saved at: {csv_file_path}")
