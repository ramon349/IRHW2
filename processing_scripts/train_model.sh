
for year in {2007,2008}; 
do 
    echo "training models for ${year}"
    for i in {1..5}; 
    do 
        echo "Starting model training fold ${i}"
        java -jar RankLib.jar -norm zscore -train "./MQ${year}/Fold${i}/train.txt" -test "./MQ${year}/Fold${i}/test.txt" -validate "./MQ${year}/Fold${i}/vali.txt" -ranker 6 -metric2t NDCG@10 -metric2T NDCG@10 -save "${year}_base_model_f${i}.txt"
        echo " Start training augmented model "
        java -jar RankLib.jar -norm zscore -train "./${year}_augData/Fold_${i}/train.txt" -test "./${year}_augData/Fold_${i}/test.txt" -validate "./${year}_augData/Fold_${i}/vali.txt" -ranker 6 -metric2t NDCG@10 -metric2T NDCG@10 -save "${year}_aug_model_f${i}.txt"
        break 
    done 
    break 
done 