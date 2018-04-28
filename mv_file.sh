#!/bin/sh

source_path1=./trainval_Hairstyles/train_aug/
source_path2=./trainval_Vehicles/train_aug/
source_path3=./trainval_Vehicles/train_radial/
dest_path=./trainval_Hairstyles/train/

for source_path in $source_path1 
do
    dir_list=`ls $source_path`
    for file in $dir_list
    do
        path="$source_path$file"
        if test -d $path
        then
            echo "copy $file ..."
            for image in ${path}/*
            do
                cp $image $dest_path${file}/
            done
        fi
    done
done
