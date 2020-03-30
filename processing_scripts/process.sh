
#This script processes the score files so the perl script can process them 
for year in {2007,2008}; 
do 
    for i in {1..5};
    do 
        models_path="./${year}_models/output${i}/score"
        perl_score="./${year}_models/output${i}/perlScore"
        mkdir -p "${perl_score}" 
        awk '{print $3}' "${models_path}/base_ScoreFile.txt" > "${perl_score}/base_ScoreFile.txt"
        awk '{print $3}' "${models_path}/aug_ScoreFile.txt" >  "${perl_score}/aug_ScoreFile.txt" 
    done 
done 