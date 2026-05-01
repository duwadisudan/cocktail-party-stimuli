import os
import sys
import csv
import random
import serial
from psychopy import visual, core, event, monitors, sound, prefs
import time
from datetime import datetime
import pandas as pd

prefs.hardware['audioLib'] = ['pygame']
video_size = (1080,720)
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
filename_response = f"response_{current_datetime}.csv"
filename_iniList = f"iniList_{current_datetime}.csv"

class WholeExperiment:
    
    def __init__(self):
        self.win1 = visual.Window(size=(1080, 1920), screen=0, fullscr=False)
        self.win2 = visual.Window(size=(1080, 1920), screen=1, fullscr=False)
        self.win3 = visual.Window(size=(1080, 1920), screen=2, fullscr=False)
        self.responses = []
        self.transcripts_dict = self.load_transcripts()
        self.list_of_all_screenshots = self.load_screenshots()
        self.trial_count = 0
        self.csv_path = f"C:\Sudan\Stimuli\initialization_data\\{filename_iniList}"
        self.spatial_video_folder = r"C:\Sudan\\Stimuli\sudan_spatial_videos_updated"
        self.response_csv_path = f"C:\Sudan\Stimuli\initialization_data\\{filename_response}"
        self.current_block = None
        self.movie_pairs = self.load_movie_pairs()
        random.shuffle(self.movie_pairs)
        self.current_block_index = 0
        #self.ser = serial.Serial('COM5')
        #self.ser.write(str.encode('1')) 
        self.block_methods = ['run_audio_visual_trial', 'run_visual_only_trial', 'run_audio_only_trail']
        self.block_name_map = {
            'run_audio_visual_trial': 'Audio-Visual Block',
            'run_visual_only_trial': 'Visual-Only Block',
            'run_audio_only_trail': 'Audio-Only Block'
        }

        red_circle = visual.Circle(
            win=self.win3,
            radius=30,
            fillColor='red',
            lineColor='red',
            pos=(0, -self.win3.size[1] / 2 + 90),
            units='pix'
            )

        red_circle.autoDraw = True

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
        
        file_path = os.path.join(save_directory, filename_iniList)

        df.to_csv(file_path, index=False)

        return file_path

    your_target_directory_path = 'C:\\Sudan\\Stimuli\\Screenshots_faces_full_updated'
    your_save_directory_path = 'C:\\Sudan\\Stimuli\\initialization_data'

    movies = extract_movie_names(your_target_directory_path)
    movie_pairs = create_unique_movie_pairs(movies)

    csv_file_path = save_to_csv(movie_pairs, your_save_directory_path)

    print(f"CSV file saved at: {csv_file_path}")

    def send_neurospec_trigger(self):
        #self.ser.write(str.encode('0'))
        time.sleep(0.1)
        #self.ser.write(str.encode('1'))

    def load_movie_pairs(self):
        movie_pairs = []
        with open(self.csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                movie_pairs.append((row['TargetMovieList'], row['MaskerMovieList']))
        return movie_pairs

    def get_next_block_movie_pairs(self):
        start_index = self.current_block_index * 60
        end_index = start_index + 60

        next_block_movie_pairs = self.movie_pairs[start_index:end_index]

        self.current_block_index += 1

        return next_block_movie_pairs
    
    def load_transcripts(self):
        transcripts_dict = {}
        with open(r"C:\\Sudan\\Stimuli\\Transcripts\\english_translations_part2_copy.csv", 'r', encoding='ISO-8859-1') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                video_name = row['Video File'].split('.mp4')[0]
                transcript = row['Transcription']
                transcripts_dict[video_name] = transcript
        return transcripts_dict
    
    def load_screenshots(self):
        screenshot_folder = r"C:\\Sudan\\Stimuli\\Screenshots_faces_full_updated"
        return [f.split('.jpg')[0] for f in os.listdir(screenshot_folder) if f.endswith('.jpg')]
    
    def play_white_noise_and_crosshair(self, win, target_screen):
        white_noise_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        white_noise_path = f"{self.spatial_video_folder}\\whiteNoise_stereo{white_noise_spatial_suffix}.wav"

        white_noise = sound.Sound(white_noise_path, secs=2)
        white_noise.setVolume(0.7)
        crosshair = visual.ShapeStim(win, vertices=((-0.2, 0), (0.2, 0), (0,0), (0,-0.1), (0, 0.1)), lineWidth=20, closeShape=False, lineColor='white')

        #self.send_neurospec_trigger()
        white_noise.play()
        crosshair.draw()
        win.flip(clearBuffer=True)
        core.wait(2)
        self.win3.flip(clearBuffer=True)
        
    def construct_movie_paths(self, target_movie, masker_movie, target_screen, masker_screen):
        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 
        
        movie1_path = f"{self.spatial_video_folder}\\{target_movie}{target_spatial_suffix}.avi"
        movie2_path = f"{self.spatial_video_folder}\\{masker_movie}{masker_spatial_suffix}.avi"
        
        return movie1_path, movie2_path

    def load_and_play_movies(self, win1, win2, mov1, mov2):

        while mov1.status != visual.FINISHED and mov2.status != visual.FINISHED:
            mov1.draw()
            mov2.draw()
            
            win1.flip(clearBuffer=True)
            win2.flip(clearBuffer=True)

        self.win1.flip(clearBuffer=True)
        self.win2.flip(clearBuffer=True)
        self.win3.flip(clearBuffer=True)        

    def load_and_play_movies_no_video(self, win1, win2, mov1, mov2):

        crosshair = visual.ShapeStim(self.win3, vertices=((-0.2, 0), (0.2, 0), (0,0), (0,-0.1), (0, 0.1)), lineWidth=20, closeShape=False, lineColor='white')
        crosshair.draw()
        self.win3.flip()

        while mov1.status != visual.FINISHED and mov2.status != visual.FINISHED:
            mov1.draw()
            mov2.draw()
            
            win1.flip()
            win2.flip()

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()
            
    def prepare_screenshot_stimuli(self, win1, target_movie, masker_movie):
        
        random_screenshots = random.sample([file for file in self.list_of_all_screenshots if file != target_movie], 1)
        all_screenshots = [target_movie] + [masker_movie] + random_screenshots
        random.shuffle(all_screenshots)
        
        true_speaker_index = all_screenshots.index(target_movie) + 1
        
        img_all = [visual.ImageStim(win1, image=f"C:\\Sudan\\Stimuli\\Screenshots_faces_full_updated\\{file}.jpg", size=(0.4, 0.2)) for file in all_screenshots]
        
        text = visual.TextStim(win1, text="Which speaker was in the video that you just attended to?", pos=(0, 0.55), height=0.06, bold = True)
        
        return img_all, text, true_speaker_index
    
    def show_screenshots_and_collect_response(self, win1, win2, win3, target_movie,masker_movie):
        img_all, text, true_speaker_index = self.prepare_screenshot_stimuli(win3, target_movie,masker_movie)
        
        text.draw()

        for i, img in enumerate(img_all):
            img.pos = (0, 0.25 - i * 0.3)
            img.draw()
            number_text = visual.TextStim(win3, text=str(i + 1), pos=(-0.3, 0.25 - i * 0.3))
            number_text.draw()
        
        win1.flip()
        win2.flip()
        win3.flip()

        keys = event.waitKeys(keyList=["1", "2", "3", "4", "5", "num_1", "num_2", "num_3", "num_4", "num_5"])
        user_response = keys[0]

        numpad_mapping = {
            "num_1": "1",
            "num_2": "2",
            "num_3": "3",
            "num_4": "4",
            "num_5": "5"
        }

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

        user_response = numpad_mapping.get(user_response, user_response)

        correct = 1 if user_response == str(true_speaker_index) else 0
        
        return user_response, correct
    

    def prepare_transcript_stimuli(self, win3, target_movie, masker_movie):
        target_transcript = self.transcripts_dict.get(target_movie, "Unknown")
        masker_transcript = self.transcripts_dict.get(masker_movie, "Unknown")
        random_transcripts = random.sample([trans for key, trans in self.transcripts_dict.items() if key != target_movie], 1)
        all_transcripts = [target_transcript] + [masker_transcript] + random_transcripts
        random.shuffle(all_transcripts)
        true_transcript_index = all_transcripts.index(target_transcript) + 1
        transcript_text = visual.TextStim(win3, text="What was the target speaker saying?", pos=(0, 0.55), height=0.06, bold=True)
        return all_transcripts, transcript_text, true_transcript_index
    
    def show_transcripts_and_collect_response(self, win1, win2, win3, target_movie, masker_movie):
        all_transcripts, transcript_text, true_transcript_index = self.prepare_transcript_stimuli(win3, target_movie, masker_movie)
        
        transcript_text.draw()
        for i, trans in enumerate(all_transcripts):
            trans_text = visual.TextStim(win3, text=f"{i + 1}. {trans}", pos=(0, 0.25 - i * 0.3), height=0.05)
            trans_text.draw()
        
        win1.flip()
        win2.flip()
        win3.flip()
        
        keys = event.waitKeys(keyList=["1", "2", "3", "4", "5", "num_1", "num_2", "num_3", "num_4", "num_5"])
        transcript_response = keys[0]

        numpad_mapping = {
            "num_1": "1",
            "num_2": "2",
            "num_3": "3",
            "num_4": "4",
            "num_5": "5"
        }

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

        transcript_response = numpad_mapping.get(transcript_response, transcript_response)

        transcript_correct = 1 if transcript_response == str(true_transcript_index) else 0
        
        return transcript_response, transcript_correct
    
    def select_screens(self):
        target_screen = random.choice([0, 1])
        masker_screen = 1 - target_screen
        center_screen = 2
        return target_screen, masker_screen, center_screen
    
    def initialize_windows(self, target_screen, masker_screen, center_screen):
        win1 = visual.Window(size=(1080, 1920), screen=target_screen, fullscr=False)
        win2 = visual.Window(size=(1080, 1920), screen=masker_screen, fullscr=False)
        center_screen = visual.Window(size=(1080, 1920), screen=center_screen, fullscr=False)

        return win1, win2, center_screen
    
    def record_trial_data(self, target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, block_type):
        trial_data = {
            "BlockType": block_type,
            "TargetMovie": target_movie,
            "MaskerMovie": masker_movie,
            "TargetSpatialSuffix": target_spatial_suffix,
            "MaskerSpatialSuffix": masker_spatial_suffix,
            "Response": user_response,
            "Correct": correct,
            "TranscriptResponse": transcript_response,
            "TranscriptCorrect": transcript_correct
        }

        with open(self.response_csv_path, 'a', newline='') as csv_file:
            fieldnames = ["BlockType", "TargetMovie", "MaskerMovie","TargetSpatialSuffix","MaskerSpatialSuffix","Response", "Correct", "TranscriptResponse", "TranscriptCorrect"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            if self.trial_count == 0:
                csv_writer.writeheader()
            
            csv_writer.writerow(trial_data)

        self.trial_count += 1

    def run_audio_visual_trial(self, win1, win2, win3, target_movie, masker_movie, target_screen, masker_screen, center_screen):
        
        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)

        mov1 = visual.MovieStim3(win1, movie1_path, size= video_size)
        mov2 = visual.MovieStim3(win2, movie2_path, size= video_size)

        self.play_white_noise_and_crosshair(win1, target_screen)

        self.load_and_play_movies(win1, win2, mov1, mov2)

        user_response, correct = self.show_screenshots_and_collect_response(win1, win2, win3, target_movie, masker_movie)

        transcript_response, transcript_correct = self.show_transcripts_and_collect_response(win1, win2, win3, target_movie,masker_movie)

        inter_trial_interval  = random.uniform(14, 16)

        crosshair = visual.ShapeStim(self.win3, vertices=((-0.2, 0), (0.2, 0), (0,0), (0,-0.1), (0, 0.1)), lineWidth=20, closeShape=False, lineColor='white')
        crosshair.draw()
        self.win3.flip()

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, "audio_visual")


        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()
    
    def run_audio_only_trail(self, win1, win2, win3, target_movie, masker_movie, target_screen, masker_screen, center_screen):

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30"

        white_noise_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        white_noise_path = f"{self.spatial_video_folder}\\whiteNoise_stereo{white_noise_spatial_suffix}.wav"
        
        white_noise = sound.Sound(white_noise_path, secs=2)
        white_noise.setVolume(0.7)

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)

        hidden_video_size = (1, 1)

        mov1 = visual.MovieStim3(win1, movie1_path, size=hidden_video_size)
        mov2 = visual.MovieStim3(win2, movie2_path, size=hidden_video_size)

        crosshair = visual.ShapeStim(win3, vertices=((-0.2, 0), (0.2, 0), (0,0), (0,-0.1), (0, 0.1)), lineWidth=20, closeShape=False, lineColor='white')
        crosshair.draw()
        win3.flip()

        #self.send_neurospec_trigger() # because there is no white noise function here

        white_noise.play()
        core.wait(2)

        self.load_and_play_movies_no_video(win1, win2, mov1, mov2)
        
        user_response, correct = 10,10

        transcript_response, transcript_correct = self.show_transcripts_and_collect_response(win1, win2, win3, target_movie,masker_movie)

        inter_trial_interval  = random.uniform(14, 16)

        crosshair = visual.ShapeStim(self.win3, vertices=((-0.2, 0), (0.2, 0), (0,0), (0,-0.1), (0, 0.1)), lineWidth=20, closeShape=False, lineColor='white')
        crosshair.draw()
        self.win3.flip()

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, "audio_only")

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()
    
    def run_visual_only_trial(self, win1, win2, win3,  target_movie, masker_movie, target_screen, masker_screen, center_screen):
        
        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)

        mov1 = visual.MovieStim3(win1, movie1_path, size=video_size, noAudio = True)
        mov2 = visual.MovieStim3(win2, movie2_path, size=video_size, noAudio = True)

        self.play_white_noise_and_crosshair(win1,target_screen)  # Here, you might want to rename this function or modify it to simply display the crosshair without white noise

        self.win3.clearBuffer()
        self.win3.flip()
        
        self.load_and_play_movies(win1, win2, mov1, mov2)  # You'll need to modify the load_and_play_movies function to accept a play_audio flag

        user_response, correct = self.show_screenshots_and_collect_response(win1, win2, win3, target_movie,masker_movie)

        inter_trial_interval  = random.uniform(14, 16)

        crosshair = visual.ShapeStim(self.win3, vertices=((-0.2, 0), (0.2, 0), (0,0), (0,-0.1), (0, 0.1)), lineWidth=20, closeShape=False, lineColor='white')
        crosshair.draw()
        self.win3.flip()

        transcript_response, transcript_correct = 10, 10

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, "visual_only")

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

    def run_control_trial(self, win1, win2, target_screen, masker_screen):

        commands = ["Move eyes to Left", "Move eyes to Right"]
        random.shuffle(commands)

        with open('C:\\Sudan\\Stimuli\\eye_no_sound.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(commands)

        if commands[1] == "Move eyes to Left":
            window_selected = self.win1
            window_number = 0
        else: 
            window_selected = self.win2
            window_number = 1

        announcement = visual.TextStim(self.win3, text=commands[1], pos=(0, 0),height=0.05)
        announcement.draw() 
        self.win3.flip()
        core.wait(1)
        self.win3.flip()

        core.wait(5) 

        win1.clearBuffer()
        win1.flip()

        inter_trial_interval  = random.uniform(14, 16)

        announcement = visual.TextStim(window_selected, text=f"Move eyes to Center", pos=(0, 0),height=0.05)
        announcement.draw() 
        window_selected.flip()

        core.wait(1)

        window_selected.flip()

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

        core.wait(2)

        self.record_control_trial_data(window_number)


    def run_control_block(self):
        self.control_screen_selections = [0, 1] * 10  # 0 for right, 1 for left
        random.shuffle(self.control_screen_selections)

        announcement = visual.TextStim(self.win3, text=f"Starting control block. Press spacebar to continue", pos=(0, 0),height=0.05)
        announcement.draw()
        
        self.win1.flip()
        self.win2.flip()
        self.win3.flip()    

        event.waitKeys(keyList=["space"])

        self.win3.clearBuffer()
        self.win3.flip()

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

        windows = {
                    0: self.win1,
                    1: self.win2,
                    2: self.win3
                }
        
        core.wait(2)

        for i in range(20):  # 20 trials in the control block
            target_screen = self.control_screen_selections.pop()
            masker_screen = 1 - target_screen
            center_screen = 2

            self.run_control_trial(windows[target_screen], windows[masker_screen], target_screen, masker_screen)
            

    def display_block_start(self, win, block_name):
        block_name = self.block_name_map.get(block_name, "Unknown Block")

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

        announcement = visual.TextStim(win, text=f"Starting {block_name}. Press spacebar to continue.", pos=(0, 0),height=0.05)
        announcement.draw()
        win.flip()
        event.waitKeys(keyList=["space"])
        
        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

    
    def run_full_experiment(self):
        random.shuffle(self.block_methods)

        windows = {
                    0: self.win1,
                    1: self.win2,
                    2: self.win3
                }
        
        for block_method_name in self.block_methods:
            print(f"Running block: {block_method_name}") 
            self.display_block_start(self.win3, block_method_name)
            block_method = getattr(self, block_method_name)
            next_block_movie_pairs = self.get_next_block_movie_pairs()
            trial_count = 0  # Initialize trial count
            for target_movie, masker_movie in next_block_movie_pairs:
                target_screen, masker_screen, center_screen = self.select_screens()

                block_method(windows[target_screen], windows[masker_screen], windows[center_screen], target_movie, masker_movie, target_screen, masker_screen, center_screen)
                
                trial_count += 1  # Increment trial count

                if trial_count % 2 == 0:  # Check if it's time for a break

                    self.inter_block_break_message()
                    self.win3.clearBuffer()


                    

            self.break_message()
            event.waitKeys(keyList=["space"])  # Wait for spacebar press to continue
            self.win3.clearBuffer()  # Clear the buffer after spacebar press
        

    def record_control_trial_data(self, target_screen):
        control_trial_data = {
            "BlockType": "Control",
            "TargetScreen": target_screen
        }
        self.responses.append(control_trial_data)

        with open(self.response_csv_path, 'a', newline='') as csv_file:
            fieldnames = ["BlockType", "TargetScreen"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            if self.trial_count == 0:
                csv_writer.writeheader()
            
            csv_writer.writerow(control_trial_data)

        self.trial_count += 1

    def end_message(self):
        win3 = visual.Window(size=(1080, 1920), screen=2, fullscr=False)
        closing_message = visual.TextStim(win3, 
                                        text="Please stay still until the experimenter says it is okay to move. The experiment is complete. Thank you!", 
                                        pos=(0, 0), height=0.05)
        closing_message.draw()
        win3.flip()
        event.waitKeys(keyList=["space"])  # Wait for a spacebar press to close
        
        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.close()
        self.win2.close()
        self.win3.close()


    def break_message(self):
        win3 = visual.Window(size=(1080, 1920), screen=2, fullscr=False)
        closing_message = visual.TextStim(win3, 
                                        text="Please stay still until the experimenter says it is okay to move. Take a break and press spacebar to continue once you are ready.", 
                                        pos=(0, 0), height=0.05)
        closing_message.draw()
        win3.flip()
        event.waitKeys(keyList=["space"])  # Wait for a spacebar press to close
        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

    def inter_block_break_message(self):
        closing_message = visual.TextStim(self.win3, 
                                        text="Please stay still until the experimenter says it is okay to move. Take a break and press spacebar to continue once you are ready.", 
                                        pos=(0, 0), height=0.05)
        closing_message.draw()
        self.win3.flip()
        event.waitKeys(keyList=["space"])  # Wait for a spacebar press to close
        self.win3.flip()
        self.win3.clearBuffer()

experiment = WholeExperiment()

experiment.run_control_block()
experiment.run_full_experiment()

core.wait(5)

experiment.end_message()








