function [ mResFiles, iTCount ] = DeepTravel( strPath, mFiles, iTotalCount )  
%   Input:  
%    strPath: the directory of the file     
%    mFiles:  save the directory of the files  
%    iTotalCount: the count of the walked files  
%   Ouput:  
%    mResFiles: the full directory of every file     
%    iTCount:   the total file count in the directory which your hava input  

    iTmpCount = iTotalCount;  
    path=strPath;  
    Files = dir(fullfile( path));  
    LengthFiles = length(Files);  
    if LengthFiles <= 2  
        mResFiles = mFiles;  
        iTCount = iTmpCount;  
        return;  
    end 
    
    for iCount=2:LengthFiles  
        if Files(iCount).isdir==1    
            if Files(iCount).name ~='.'    
                filePath = [path Files(iCount).name '/'];    
                [mFiles, iTmpCount] = DeepTravel( filePath, mFiles, iTmpCount);  
            end    
        else
            if strcmp(Files(iCount).name(end-3:end), '.jpg')
                iTmpCount = iTmpCount + 1;  
                filePath = [path Files(iCount).name];   
                mFiles{iTmpCount} = filePath; 
            else
                disp(Files(iCount).name);
            end
        end   
    end  
    mResFiles = mFiles;  
    iTCount = iTmpCount;  
end  