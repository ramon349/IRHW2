for year in {2007,2008};
do 
    for i in {1..5};
    do 
        perl_score="./${year}_models/output${i}/perlScore"
        analysis_path="./${year}_analysis"
        perl ./processing_scripts/mslr-eval-score-mslr.pl "./MQ${year}/Fold${i}/test.txt" "${perl_score}/base_ScoreFile.txt" "${analysis_path}/perl_comp_${i}_base.txt" 0
        perl ./processing_scripts/mslr-eval-score-mslr.pl "./MQ${year}/Fold${i}/test.txt" "${perl_score}/aug_ScoreFile.txt" "${analysis_path}/perl_comp_${i}_aug.txt" 0
    done 
done 