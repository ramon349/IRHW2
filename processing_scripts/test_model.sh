echo " Starting test" 
for year in {2007,2008};
    models_path="./${year}_models/"
    for i in {1..5};
    do
        mkdir -p "./${year}_models/output${i}/score"
        mkdir -p "./${year_models}output${i}/comp"
        java -jar RankLib.jar -norm zscore -load "./base_model_f${i}.txt" -test "./MQ2008/Fold${i}/test.txt" -metric2T NDCG@10 -idv "./output${i}/comp/base.txt"
        java -jar RankLib.jar -load "./base_model_f${i}.txt" -rank "./MQ2008/Fold${i}/test.txt" -score "./output${i}/score/base_ScoreFile.txt"
        java -jar RankLib.jar -norm zscore -load "./aug_model_f${i}.txt" -test "./augData1/Fold_${i}/test.txt" -metric2T NDCG@10 -idv "./output${i}/comp/aug.txt"
        java -jar RankLib.jar -load "./aug_model_f${i}.txt" -rank "./augData1/Fold_${i}/test.txt" -score "./output${i}/score/aug_ScoreFile.txt"
        java -cp RankLib.jar ciir.umass.edu.eval.Analyzer -all "./output${i}/comp" -base base.txt > "analysis${i}.txt"
    done 
done 
