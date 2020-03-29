for i in {1..5};
do 
    cd "./output${i}/" 
    perl ../mslr-eval-score-mslr.pl "../MQ2008/Fold${i}/test.txt" ./new_base_ScoreFile.txt RAMEN_d.txt 0
    echo " Doing other test "
    perl ../mslr-eval-score-mslr.pl "../MQ2008/Fold${i}/test.txt" ./new_aug_ScoreFile.txt RAMEN_c.txt 0
    cd ../ 
done 
