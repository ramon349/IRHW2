echo " Starting test" 
for year in {2007,2008};
do
    models_path="./${year}_models"
    analysis_path="./${year}_analysis"
    mkdir -p "${analysis_path}"
    for i in {1..5};
    do
        output_path="./${year}_models/output${i}"
        base_data="./MQ${year}/Fold${i}"
        aug_data="./${year}_augData/Fold_${i}"
        mkdir -p "${output_path}/score"
        mkdir -p "${output_path}/comp"
        java -jar RankLib.jar -norm zscore -load "${models_path}/${year}_base_model_f${i}.txt" -test "${base_data}/test.txt" -metric2T NDCG@10 -idv "${output_path}/comp/base.txt"
        java -jar RankLib.jar -norm zscore -load "${models_path}/${year}_base_model_f${i}.txt" -rank "${base_data}/test.txt" -score "${output_path}/score/base_ScoreFile.txt"
        java -jar RankLib.jar -norm zscore -load "${models_path}/${year}_aug_model_f${i}.txt" -test "${aug_data}/test.txt" -metric2T NDCG@10 -idv "${output_path}/comp/aug.txt"
        java -jar RankLib.jar -norm zscore -load "${models_path}/${year}_aug_model_f${i}.txt" -rank "${aug_data}/test.txt" -score "${output_path}/score/aug_ScoreFile.txt"
        java -cp RankLib.jar ciir.umass.edu.eval.Analyzer -all "${output_path}/comp" -base base.txt > "${analysis_path}/analysis_fold${i}.txt"
    done 
done 
