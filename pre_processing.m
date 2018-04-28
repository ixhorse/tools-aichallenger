clc, clear all,  close all

CoreNum=12; 
delete(gcp('nocreate'));  
parpool('local',CoreNum);

class = 'Animals';
dataset = 'train';
data_path = ['trainval_' class '/' dataset '/'];
out_path = ['trainval_' class '/' dataset '_radial' '/'];
if ~exist(out_path, 'dir')
    mkdir(out_path);
end

mFiles = [];
[imageFiles, numFiles] = DeepTravel(data_path,mFiles,0);

for i = 1:numFiles
    image_path = imageFiles{i};
    S = regexp(image_path, '/', 'split');
    if ~exist(fullfile(out_path, S{3}), 'dir')
        mkdir(fullfile(out_path, S{3}));
    end
end


parfor i = 1:numFiles
    tic
    image_path = imageFiles{i};
    S = regexp(image_path, '/', 'split');
    image_path_new = fullfile(out_path, S{3}, S{4});
    radial_transform(image_path, image_path_new);
    toc
end

delete(gcp('nocreate')); 