import os
import sys
import csv
import random
import serial
from psychopy import visual, core, event, monitors, sound, prefs
import time


#ser = serial.Serial('COM5')
#ser.write(str.encode('1'))

prefs.hardware['audioLib'] = ['pygame']
video_size = (1080,720)
from datetime import datetime
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"response_{current_datetime}.csv"



class AudioVisualExperiment:
    
    def __init__(self):
        self.win1 = visual.Window(size=(1080, 1920), screen=0, fullscr=False)
        self.win2 = visual.Window(size=(1080, 1920), screen=1, fullscr=False)
        self.win3 = visual.Window(size=(1080, 1920), screen=2, fullscr=False)
        self.responses = []
        self.transcripts_dict = self.load_transcripts()
        self.list_of_all_screenshots = self.load_screenshots()
        self.trial_count = 0
        self.total_trials = 60  # Total number of trials in a block
        self.white_noise_path = 'C:\\Users\\mn0mn\\Documents\\Stimuli\\whiteNoise_stereo.wav'  # Path to white noise sound
        self.csv_path = "C:\\Users\\mn0mn\\Documents\\Stimuli\\initialization_data\\iniList_sudan_test_10_30_20231030_.csv"
        self.spatial_video_folder = "C:\\Users\\mn0mn\Documents\\Stimuli\\sudan_spatial_videos_updated"
        self.screenshot_folder = "C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces_full_updated"  # Path to screenshot folder
        self.response_csv_path = f"C:\\Users\\mn0mn\\Documents\\Stimuli\\initialization_data\\{filename}"
        self.block_order = []  # Will hold the randomized order of blocks
        self.current_block = None
        self.csv_file = open(self.csv_path, 'r')
        self.csv_reader = csv.DictReader(self.csv_file)
        self.movie_pairs = self.load_movie_pairs()
        random.shuffle(self.movie_pairs)
        self.current_movie_index = 0
        self.current_block_index = 0
        self.continue_experiment = True 
        #self.ser = serial.Serial('COM5')
        #self.ser.write(str.encode('1'))      
        self.block_methods = ['run_audio_visual_trial', 'run_visual_only_trial', 'run_audio_only_trail']
        self.block_name_map = {
            'run_audio_visual_trial': 'Audio-Visual Block',
            'run_visual_only_trial': 'Visual-Only Block',
            'run_audio_only_trail': 'Audio-Only Block'
        }

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
        with open("C:\\Users\\mn0mn\\Documents\\Stimuli\\Transcripts\\english_translations_part2_copy.csv", 'r', encoding='ISO-8859-1') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                video_name = row['Video File'].split('.mp4')[0]
                transcript = row['Transcription']
                transcripts_dict[video_name] = transcript
        return transcripts_dict
    
    def load_screenshots(self):
        screenshot_folder = "C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces_full_updated"
        return [f.split('.jpg')[0] for f in os.listdir(screenshot_folder) if f.endswith('.jpg')]
    
    def play_white_noise_and_crosshair(self, win):
        white_noise_spatial_suffix = "_30" if win == 1 else "_-30"
        white_noise_path = f"{self.spatial_video_folder}\\whiteNoise_stereo{white_noise_spatial_suffix}.wav"
        
        white_noise = sound.Sound(white_noise_path, secs=2)
        white_noise.setVolume(0.7)
        crosshair = visual.ShapeStim(win, vertices=((0, -0.05), (0, 0.05), (0,0), (-0.05,0), (0.05, 0)), lineWidth=10, closeShape=False, lineColor='white')
        
        self.send_neurospec_trigger()
        
        white_noise.play()
        crosshair.draw()
        win.flip()
        core.wait(2)
        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()

    
    def construct_movie_paths(self, target_movie, masker_movie, target_screen, masker_screen):
        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 
        
        movie1_path = f"{self.spatial_video_folder}\\{target_movie}{target_spatial_suffix}.avi"
        movie2_path = f"{self.spatial_video_folder}\\{masker_movie}{masker_spatial_suffix}.avi"
        
        return movie1_path, movie2_path

    def load_and_play_movies(self, target_win, masker_win, target_movie_path, masker_movie_path, play_audio = True):
    # Load the target movie with audio
        target_mov = visual.MovieStim3(target_win, target_movie_path, size=video_size, noAudio=not play_audio)
        # Load the masker movie without audio
        masker_mov = visual.MovieStim3(masker_win, masker_movie_path, size=video_size, noAudio=not play_audio)

        self.send_neurospec_trigger()

        while target_mov.status != visual.FINISHED and masker_mov.status != visual.FINISHED:
            target_mov.draw()
            masker_mov.draw()
            
            target_win.flip()
            masker_win.flip()

            self.win1.clearBuffer()
            self.win2.clearBuffer()
            self.win3.clearBuffer()

            if 'escape' in event.getKeys():
                return True
        return False


    # ... escape key handling ...

        return not escape_pressed
        

    def prepare_screenshot_stimuli(self, win1, target_movie):
        screenshot1_path = f"C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces_full_updated\\{target_movie}.jpg"
        
        random_screenshots = random.sample([file for file in self.list_of_all_screenshots if file != target_movie], 4)
        all_screenshots = [target_movie] + random_screenshots
        random.shuffle(all_screenshots)
        
        true_speaker_index = all_screenshots.index(target_movie) + 1
        
        img_all = [visual.ImageStim(win1, image=f"C:\\Users\\mn0mn\\Documents\\Stimuli\\Sudan_face\\Screenshots_faces_full_updated\\{file}.jpg", size=(0.4, 0.2)) for file in all_screenshots]
        
        text = visual.TextStim(win1, text="Which speaker was in the video that you just attended to?", pos=(0, 0.9), height=0.05)
        
        return img_all, text, true_speaker_index
    
    def show_screenshots_and_collect_response(self, win1, win2, win3, target_movie):
        img_all, text, true_speaker_index = self.prepare_screenshot_stimuli(win3, target_movie)
        
        text.draw()


        for i, img in enumerate(img_all):
            img.pos = (0, 0.6 - i * 0.3)
            img.draw()
            number_text = visual.TextStim(win3, text=str(i + 1), pos=(-0.3, 0.6 - i * 0.3))
            number_text.draw()
        
        self.win1.flip()
        self.win2.flip()
        self.win3.flip()
        
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
        
        self.win1.flip()
        self.win2.flip()
        self.win3.flip()
        
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
        
    #def initialize_windows(self, target_screen, masker_screen, center_screen):
        #win1 = visual.Window(size=(1080, 1920), screen=target_screen, fullscr=False)
        #win2 = visual.Window(size=(1080, 1920), screen=masker_screen, fullscr=False)
        #center_screen = visual.Window(size=(1080, 1920), screen=center_screen, fullscr=False)

        #return win1, win2, center_screen
    
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

        target_win = self.win2 if target_screen == 1 else self.win1

        target_win.clearBuffer()

        # In run_visual_only_trial, you would use:
        self.play_white_noise_and_crosshair(target_win)

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)
        escape_pressed = self.load_and_play_movies(win1, win2, movie1_path, movie2_path)

        user_response, correct = self.show_screenshots_and_collect_response(win1, win2, win3, target_movie)

        transcript_response, transcript_correct = self.show_transcripts_and_collect_response(win1, win2, win3, target_movie)

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, "audio_visual")

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()
        #core.wait(random.uniform(14, 16))

        if 'escape' in event.getKeys():
            self.continue_experiment = False
            return False
        return True
    
    def run_audio_only_trail(self, win1, win2, win3, target_movie, masker_movie, target_screen, masker_screen, center_screen):
        
        crosshair = visual.ShapeStim(win3, vertices=((0, -0.05), (0, 0.05), (0,0), (-0.05,0), (0.05, 0)), lineWidth=10, closeShape=False, lineColor='white')
        crosshair.draw()
        self.win3.flip()

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30"

        white_noise_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        white_noise_path = f"{self.spatial_video_folder}\\whiteNoise_stereo{white_noise_spatial_suffix}.wav"
        
        white_noise = sound.Sound(white_noise_path, secs=2)
        white_noise.setVolume(0.7)


        white_noise.play()
        core.wait(2)

        #self.play_white_noise_and_crosshair(win1,target_screen)

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)
        escape_pressed = self.load_and_play_movies(win1, win2, movie1_path, movie2_path)

        user_response, correct = 10,10

        transcript_response, transcript_correct = self.show_transcripts_and_collect_response(win1, win2, win3, target_movie)

         

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, "audio_only")

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()
        #core.wait(random.uniform(14, 16))


        if 'escape' in event.getKeys():
            self.continue_experiment = False
            return False
        return True
    
    def run_visual_only_trial(self, win1, win2, win3,  target_movie, masker_movie, target_screen, masker_screen, center_screen):

    # In run_visual_only_trial, you would use:

        target_win = self.win2 if target_screen == 1 else self.win1

        target_win.clearBuffer()
        

        self.play_white_noise_and_crosshair(target_win)  # Here, you might want to rename this function or modify it to simply display the crosshair without white noise

        movie1_path, movie2_path = self.construct_movie_paths(target_movie, masker_movie, target_screen, masker_screen)
        
        self.load_and_play_movies(win1, win2, movie1_path, movie2_path, play_audio=False)  # You'll need to modify the load_and_play_movies function to accept a play_audio flag

        user_response, correct = self.show_screenshots_and_collect_response(win1, win2, win3, target_movie)

        transcript_response, transcript_correct = 10, 10

        target_spatial_suffix = "_30" if target_screen == 1 else "_-30"
        masker_spatial_suffix = "_30" if masker_screen == 1 else "_-30" 

        self.record_trial_data(target_movie, masker_movie, user_response, correct, transcript_response, transcript_correct, target_spatial_suffix, masker_spatial_suffix, "visual_only")

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()
        #core.wait(random.uniform(14, 16))

        if 'escape' in event.getKeys():
            self.continue_experiment = False
            return False
        return True
    
        
    

    def run_control_trial(self, win1, win2, target_screen, masker_screen):

        target_win = self.win2 if target_screen == 1 else self.win1

        target_win.clearBuffer()


        self.play_white_noise_and_crosshair(target_win)  # Assuming you still want the white noise and crosshair

        # Keep displaying the crosshair for 3 seconds
        crosshair = visual.ShapeStim(target_win, vertices=((0, -0.05), (0, 0.05), (0,0), (-0.05,0), (0.05, 0)), lineWidth=10, closeShape=False, lineColor='white')
        crosshair.draw()
        
        target_win.flip()
        self.send_neurospec_trigger()
        core.wait(3) # as if crosshair fixation is the

        target_win.clearBuffer()
        target_win.flip()

        win1.clearBuffer()
        win2.clearBuffer()
        self.win3.clearBuffer()
        win1.flip()
        win2.flip()
        self.win3.flip()

        # No need to collect any responses for this control trial, unless you want to.
        # But you can record which screen was used, for analysis purposes.
        self.record_control_trial_data(target_screen)
        #core.wait(random.uniform(14, 16))

    def run_control_block(self):
        self.control_screen_selections = [0, 1] * 10  # 0 for right, 1 for left
        random.shuffle(self.control_screen_selections)

        announcement = visual.TextStim(self.win3, text=f"Starting control block. Press spacebar to continue", pos=(0, 0),height=0.05)
        announcement.draw() 
        self.win3.flip()    
        event.waitKeys(keyList=["space"])

        self.win1.clearBuffer()
        self.win2.clearBuffer()
        self.win3.clearBuffer()
        self.win1.flip()
        self.win2.flip()
        self.win3.flip()

        for i in range(20):  # 20 trials in the control block
            target_screen = self.control_screen_selections.pop()
            masker_screen = 1 - target_screen
            center_screen = 2
            self.run_control_trial(self.win1, self.win2, target_screen, masker_screen)

        self.break_message()
            

    def display_block_start(self, win, block_name):
        block_name = self.block_name_map.get(block_name, "Unknown Block")
        announcement = visual.TextStim(win, text=f"Starting {block_name}. Press spacebar to continue.", pos=(0, 0),height=0.05)
        announcement.draw()
        win.flip()
        event.waitKeys(keyList=["space"])
        win.flip()

            

    
    def run_full_experiment(self):
        random.shuffle(self.block_methods)
        for block_method_name in self.block_methods:
            print(f"Running block: {block_method_name}") 
            self.display_block_start(self.win3, block_method_name)
            block_method = getattr(self, block_method_name)
            next_block_movie_pairs = self.get_next_block_movie_pairs()
            for target_movie, masker_movie in next_block_movie_pairs:

                self.exp_screen_selections = [0, 1] * 30  # 0 for right, 1 for left
                random.shuffle(self.exp_screen_selections)

                for i in range(20):  # 20 trials in the control block
                    target_screen = self.exp_screen_selections.pop()
                    masker_screen = 1 - target_screen
                    center_screen = 2

                continue_experiment = block_method(self.win1, self.win2, self.win3, target_movie, masker_movie, target_screen, masker_screen, center_screen)
                
                #if not continue_experiment:
                    #break  # If 'escape' was pressed or some other condition to stop the experiment
            self.break_message()
        

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
        closing_message = visual.TextStim(self.win3, 
                                        text="Please stay still until the experimenter says it is okay to move. The experiment is complete. Thank you!", 
                                        pos=(0, 0), height=0.05)
        closing_message.draw()
        self.win3.flip()
        event.waitKeys(keyList=["space"])  # Wait for a spacebar press to close
        self.win3.clearBuffer()

        self.win1.close()
        self.win2.close()
        self.win3.close()

    def break_message(self):
        closing_message = visual.TextStim(self.win3, 
                                        text="Please stay still until the experimenter says it is okay to move. Take a break and press spacebar to continue once you are ready.", 
                                        pos=(0, 0), height=0.05)
        closing_message.draw()
        self.win3.flip()
        event.waitKeys(keyList=["space"])  # Wait for a spacebar press to close
        self.win3.clearBuffer()

#ser.close()

experiment = AudioVisualExperiment()

experiment.run_full_experiment()

experiment.end_message()









