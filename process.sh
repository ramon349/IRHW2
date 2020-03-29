
#processingFiles 

for i in {1..5};
do 
    cd "./output${i}/" 
    awk '{print $3}' ./base_ScoreFile.txt >  new_base_ScoreFile.txt 
    awk '{print $3}' ./aug_ScoreFile.txt >  new_aug_ScoreFile.txt 
    cd ../ 
done 