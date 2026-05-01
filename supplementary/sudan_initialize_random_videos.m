function sudan_initialize_random_videos(subj)

    folder_path = 'C:\Users\mn0mn\Documents\Stimuli\video_3_second_final_updated';
    video_files = dir(fullfile(folder_path, '*.mp4'));

    % Initialize an empty cell array to hold the file names
    TargetMovieList = cell(length(video_files), 1);
    MaskerMovieList = cell(length(video_files), 1);

    for i = 1:length(video_files)
        [~, name, ~] = fileparts(video_files(i).name);
        file_names_without_extension{i} = name;
    end

    % Generate a random permutation of indices for TargetMovieList
    random_indices = randperm(length(file_names_without_extension));
    TargetMovieList = file_names_without_extension(random_indices);

    % Create a MaskerMovieList initially as a copy of TargetMovieList
    MaskerMovieList = TargetMovieList;

    % Loop to ensure no ith element in TargetMovieList is same as ith element in MaskerMovieList
    for i = 1:length(TargetMovieList)
        while strcmp(TargetMovieList{i}, MaskerMovieList{i})
            swap_idx = randi(length(MaskerMovieList));
            % Swap only if the random index doesn't result in another match at the new position
            if ~strcmp(TargetMovieList{i}, MaskerMovieList{swap_idx})
                temp = MaskerMovieList{i};
                MaskerMovieList{i} = MaskerMovieList{swap_idx};
                MaskerMovieList{swap_idx} = temp;
            end
        end
    end

    numTrials = 180;

    dnc = clock;
    dncstr = [num2str(dnc(1)) num2str(dnc(2)) num2str(dnc(3)) '_'];

    % Define the directory where you want to save the file
    saveDir = 'C:\Users\mn0mn\Documents\Stimuli\initialization_data';
    
    % Generate the full path for the file to be saved
    fileName = fullfile(saveDir, ['iniList_' subj '_' dncstr '.mat']);
    
    % Save the variables in the .mat file
    save(fileName, 'TargetMovieList', 'MaskerMovieList', 'numTrials');

    % Ensure the lists are column vectors
    TargetMovieList = TargetMovieList(:);
    MaskerMovieList = MaskerMovieList(:);

    % Create table with named columns
    T = table(TargetMovieList, MaskerMovieList, 'VariableNames', {'TargetMovieList', 'MaskerMovieList'});

    % Generate the full path for the CSV file to be saved
    csvFileName = fullfile(saveDir, ['iniList_' subj '_' dncstr '.csv']);
    
    % Save the table in the .csv file
    writetable(T, csvFileName);
end


