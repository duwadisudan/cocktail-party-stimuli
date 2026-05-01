import os
import sys
import csv
import random
from psychopy import visual, core, event, monitors, sound, prefs
prefs.hardware['audioLib'] = ['pygame']
video_size = (1080,720)

class AudioVisualExperiment:
    
    def __init__(self):
        self.responses = []
        self.transcripts_dict = self.load_transcripts()
        self.list_of_all_screenshots = self.load_screenshots()
        self.trial_count = 0
        self.total_trials = 60  # Total number of trials in a block
        self.white_noise_path = 'C:\\Users\\mn0mn\\Documents\\Stimuli\\whiteNoise_stereo.wav'  # Path to white noise sound
        self.csv_path = "C:\\Users\\mn0mn\\Documents\\Stimuli\\initialization_data\\iniList_10_13_20231013_.csv"
        self.spatial_video_folder = "C:\\Users\\mn0mn\Documents\\Stimuli\\sudan_spatial_videos"
        self.screenshot_folder = "C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces"  # Path to screenshot folder
        self.response_csv_path = "C:\\Users\\mn0mn\Documents\\Stimuli\\initialization_data\\responses.csv"  # Where to save responses
        self.block_order = []  # Will hold the randomized order of blocks
        self.current_block = None
        self.csv_file = open(self.csv_path, 'r')
        self.csv_reader = csv.DictReader(self.csv_file)
        self.movie_pairs = self.load_movie_pairs()
        random.shuffle(self.movie_pairs)
        self.current_movie_index = 0
        self.current_block_index = 0
        self.continue_experiment = True
        self.block_methods = ['run_audio_visual_trial', 'run_visual_only_trial', 'run_audio_only_trail']


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
        with open("C:\\Users\\mn0mn\\Documents\\Stimuli\\Transcripts\\english_translations_part2.csv", 'r', encoding='ISO-8859-1') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                video_name = row['Video File'].split('.mp4')[0]
                transcript = row['Transcription']
                transcripts_dict[video_name] = transcript
        return transcripts_dict
    
    def load_screenshots(self):
        screenshot_folder = "C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces"
        return [f.split('.jpg')[0] for f in os.listdir(screenshot_folder) if f.endswith('.jpg')]
    
    def play_white_noise_and_crosshair(self, win, target_screen):
        white_noise_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        white_noise_path = f"{self.spatial_video_folder}\\whiteNoise_stereo{white_noise_spatial_suffix}.wav"
        
        white_noise = sound.Sound(white_noise_path, secs=2)
        crosshair = visual.ShapeStim(win, vertices=((0, -0.05), (0, 0.05), (0,0), (-0.05,0), (0.05, 0)), lineWidth=10, closeShape=False, lineColor='white')
        
        white_noise.play()
        crosshair.draw()
        win.flip()
        core.wait(2)

    
    def construct_movie_paths(self, target_movie, masker_movie, target_screen, masker_screen):
        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 
        
        movie1_path = f"{self.spatial_video_folder}\\{target_movie}{target_spatial_suffix}.avi"
        movie2_path = f"{self.spatial_video_folder}\\{masker_movie}{masker_spatial_suffix}.avi"
        
        return movie1_path, movie2_path

    def load_and_play_movies(self, win1, win2, movie1_path, movie2_path, play_audio = True):
        mov1 = visual.MovieStim3(win1, movie1_path, size=video_size, noAudio=not play_audio)
        mov2 = visual.MovieStim3(win2, movie2_path, size=video_size, noAudio=not play_audio)

        while mov1.status != visual.FINISHED and mov2.status != visual.FINISHED:
            mov1.draw()
            mov2.draw()
            win1.flip()
            win2.flip()

            if 'escape' in event.getKeys():
                return True
        return False        

    def prepare_screenshot_stimuli(self, win1, target_movie):
        screenshot1_path = f"C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces\\{target_movie}.jpg"
        
        random_screenshots = random.sample([file for file in self.list_of_all_screenshots if file != target_movie], 4)
        all_screenshots = [target_movie] + random_screenshots
        random.shuffle(all_screenshots)
        
        true_speaker_index = all_screenshots.index(target_movie) + 1
        
        img_all = [visual.ImageStim(win1, image=f"C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces\\{file}.jpg", size=(0.2, 0.2)) for file in all_screenshots]
        
        text = visual.TextStim(win1, text="Which speaker was in the video that you just attended to?", pos=(0, 0.9), height=0.05)
        
        return img_all, text, true_speaker_index
    
    def show_screenshots_and_collect_response(self, win1, win2, win3, target_movie):
        img_all, text, true_speaker_index = self.prepare_screenshot_stimuli(win3, target_movie)
        
        text.draw()
        for i, img in enumerate(img_all):
            img.pos = (0, 0.6 - i * 0.3)
            img.draw()
            number_text = visual.TextStim(win3, text=str(i + 1), pos=(-0.2, 0.6 - i * 0.3))
            number_text.draw()
        
        win1.flip()
        win2.flip()
        win3.flip()
        
        keys = event.waitKeys(keyList=["1", "2", "3", "4", "5"])
        user_response = keys[0]
        correct = 1 if user_response == str(true_speaker_index) else 0
        
        return user_response, correct
    

    def prepare_transcript_stimuli(self, win3, target_movie):
        target_transcript = self.transcripts_dict.get(target_movie, "Unknown")
        
        random_transcripts = random.sample([trans for key, trans in self.transcripts_dict.items() if key != target_movie], 4)
        all_transcripts = [target_transcript] + random_transcripts
        random.shuffle(all_transcripts)
        
        true_transcript_index = all_transcripts.index(target_transcript) + 1
        
        transcript_text = visual.TextStim(win3, text="What was the target speaker saying?", pos=(0, 0.9),height=0.05)
        
        return all_transcripts, transcript_text, true_transcript_index
    
    def show_transcripts_and_collect_response(self, win1, win2, win3, target_movie):
        all_transcripts, transcript_text, true_transcript_index = self.prepare_transcript_stimuli(win3, target_movie)
        
        transcript_text.draw()
        for i, trans in enumerate(all_transcripts):
            trans_text = visual.TextStim(win3, text=f"{i + 1}. {trans}", pos=(0, 0.6 - i * 0.3), height=0.05)
            trans_text.draw()
        
        win1.flip()
        win2.flip()
        win3.flip()
        
        keys = event.waitKeys(keyList=["1", "2", "3", "4", "5"])
        transcript_response = keys[0]
        transcript_correct = 1 if transcript_response == str(true_transcript_index) else 0
        
        return transcript_response, transcript_correct
    

    def select_movies(self):
        # Assuming self.csv_path is the path to your CSV file
        with open(self.csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            row = next(csv_reader)  # Assuming you want to read the first row; modify as needed
            target_movie = row['TargetMovieList']
            masker_movie = row['MaskerMovieList']
        return target_movie, masker_movie
    
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
    
    def record_trial_data(self, target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix):
        trial_data = {
            "TargetMovie": target_movie,
            "MaskerMovie": masker_movie,
            "TargetSpatialSuffix": target_spatial_suffix,  # Add this line
            "MaskerSpatialSuffix": masker_spatial_suffix,  # Add this line
            "Response": user_response,
            "Correct": correct,
            "TranscriptResponse": transcript_response,
            "TranscriptCorrect": transcript_correct
    }
    # ... (existing code to write this data to CSV)


        with open(self.response_csv_path, 'a', newline='') as csv_file:
            fieldnames = ["TargetMovie", "MaskerMovie","TargetSpatialSuffix","MaskerSpatialSuffix","Response", "Correct", "TranscriptResponse", "TranscriptCorrect"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            if self.trial_count == 0:
                csv_writer.writeheader()
            
            csv_writer.writerow(trial_data)

        self.trial_count += 1


    def run_audio_visual_trial(self, win1, win2, win3, target_movie, masker_movie, target_screen, masker_screen, center_screen):
        self.play_white_noise_and_crosshair(win1, target_screen)

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)
        escape_pressed = self.load_and_play_movies(win1, win2, movie1_path, movie2_path)

        user_response, correct = self.show_screenshots_and_collect_response(win1, win2, win3, target_movie)

        transcript_response, transcript_correct = self.show_transcripts_and_collect_response(win1, win2, win3, target_movie)

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix)

        win1.close()
        win2.close()
        win3.close()

        if 'escape' in event.getKeys():
            self.continue_experiment = False
            return False
        return True
    
    def run_audio_only_trail(self, win1, win2, win3, target_movie, masker_movie, target_screen, masker_screen, center_screen):
        
        crosshair = visual.ShapeStim(win3, vertices=((0, -0.05), (0, 0.05), (0,0), (-0.05,0), (0.05, 0)), lineWidth=10, closeShape=False, lineColor='white')
        crosshair.draw()
        win3.flip()

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30"

        white_noise_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        white_noise_path = f"{self.spatial_video_folder}\\whiteNoise_stereo{white_noise_spatial_suffix}.wav"
        
        white_noise = sound.Sound(white_noise_path, secs=2)

        white_noise.play()
        core.wait(2)

        #self.play_white_noise_and_crosshair(win1,target_screen)

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)
        escape_pressed = self.load_and_play_movies(win1, win2, movie1_path, movie2_path)

        user_response, correct = 10,10

        transcript_response, transcript_correct = self.show_transcripts_and_collect_response(win1, win2, win3, target_movie)

         

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix)

        win1.close()
        win2.close()
        win3.close()

        if 'escape' in event.getKeys():
            self.continue_experiment = False
            return False
        return True
    
    def run_visual_only_trial(self, win1, win2, win3,  target_movie, masker_movie, target_screen, masker_screen, center_screen):
        self.play_white_noise_and_crosshair(win1,target_screen)  # Here, you might want to rename this function or modify it to simply display the crosshair without white noise

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)
        
        self.load_and_play_movies(win1, win2, movie1_path, movie2_path, play_audio=False)  # You'll need to modify the load_and_play_movies function to accept a play_audio flag

        user_response, correct = self.show_screenshots_and_collect_response(win1, win2, win3, target_movie)

        transcript_response, transcript_correct = 10, 10

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix)

        win1.close()
        win2.close()
        win3.close()

        if 'escape' in event.getKeys():
            self.continue_experiment = False
            return False
        return True
    

    def run_control_trial(self, win1, win2, target_screen, masker_screen):

        self.play_white_noise_and_crosshair(win1,target_screen)  # Assuming you still want the white noise and crosshair

        # Keep displaying the crosshair for 3 seconds
        crosshair = visual.ShapeStim(win1, vertices=((0, -0.05), (0, 0.05), (0,0), (-0.05,0), (0.05, 0)), lineWidth=10, closeShape=False, lineColor='white')
        crosshair.draw()
        win1.flip()
        core.wait(3)
        win1.close()

        # No need to collect any responses for this control trial, unless you want to.
        # But you can record which screen was used, for analysis purposes.
        self.record_control_trial_data(target_screen)

    def run_control_block(self):
        self.control_screen_selections = [0, 1] * 10  # 0 for right, 1 for left
        random.shuffle(self.control_screen_selections)

        win1 = visual.Window(size=(1080, 1920), screen=0, fullscr=False)
        win2 = visual.Window(size=(1080, 1920), screen=1, fullscr=False)
        win3 = visual.Window(size=(1080, 1920), screen=2, fullscr=False)
        announcement = visual.TextStim(win3, text=f"Starting control block. Press spacebar to continue", pos=(0, 0))
        announcement.draw() 
        win3.flip()    
        event.waitKeys(keyList=["space"])

        win1.flip()
        win2.flip()
        win3.flip()

        for i in range(20):  # 20 trials in the control block
            target_screen = self.control_screen_selections.pop()
            masker_screen = 1 - target_screen
            center_screen = 2
            win1, win2, win3 = self.initialize_windows(target_screen, masker_screen, center_screen)
            self.run_control_trial(win1, win2, target_screen, masker_screen)
            win1.close()
            win2.close()
            win3.close()

    def display_block_start(self, win, block_name):
        announcement = visual.TextStim(win, text=f"Starting {block_name} block. Press spacebar to continue.", pos=(0, 0),height=0.05)
        announcement.draw()
        win.flip()
        event.waitKeys(keyList=["space"])
        win.flip()

            

    
    def run_full_experiment(self):
        random.shuffle(self.block_methods)
        for block_method_name in self.block_methods:
            print(f"Running block: {block_method_name}") 
            win1, win2, win3 = self.initialize_windows(0, 1, 2)
            self.display_block_start(win3, block_method_name)
            block_method = getattr(self, block_method_name)
            next_block_movie_pairs = self.get_next_block_movie_pairs()
            for target_movie, masker_movie in next_block_movie_pairs:
                target_screen, masker_screen, center_screen = self.select_screens()
                win1, win2, win3 = self.initialize_windows(target_screen, masker_screen, center_screen)
                continue_experiment = block_method(win1, win2, win3, target_movie, masker_movie, target_screen, masker_screen, center_screen)
                if not continue_experiment:
                    break  # If 'escape' was pressed or some other condition to stop the experiment

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



    def start_experiment(self):
        next_block_movie_pairs = self.get_next_block_movie_pairs()  # Get the 60 movie pairs for this block
        for i, (target_movie, masker_movie) in enumerate(next_block_movie_pairs):
            target_screen, masker_screen = self.select_screens()
            win1, win2 = self.initialize_windows(target_screen, masker_screen)
            
            self.run_audio_visual_trial(win1, win2, target_movie, masker_movie, target_screen, masker_screen)

            win1.close()
            win2.close()

            


spatial_video_folder = "path_to_spatial_videos"
transcript_csv_path = "path_to_transcripts"
screenshot_folder = "path_to_screenshots"
white_noise_path = "path_to_white_noise"

  

experiment = AudioVisualExperiment()
experiment.run_control_block()
experiment.run_full_experiment()



