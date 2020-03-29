
for year in {2007,2008}; 
do 
    echo "training models for ${year}"
    models_path="./${year}_models"
    mkdir "${models_path}" 
    for i in {1..5}; 
    do 
        base_path="./MQ${year}/Fold${i}"
        aug_path="./${year}_augData/Fold_${i}"
        echo "Starting model training fold ${i}"
        java -jar RankLib.jar -norm zscore -train "${base_path}/train.txt" -test ".${base_path}/test.txt" -validate "${base_path}/vali.txt" -ranker 6 -metric2t NDCG@10 -metric2T NDCG@10 -save "${models_path}/${year}_base_model_f${i}.txt"
        echo " Start training augmented model "
        java -jar RankLib.jar -norm zscore -train "${aug_path}/train.txt" -test "${aug_path}/test.txt" -validate "./${aug_path}/vali.txt" -ranker 6 -metric2t NDCG@10 -metric2T NDCG@10 -save "${models_path}/${year}_aug_model_f${i}.txt"
    done 
    break 
done 