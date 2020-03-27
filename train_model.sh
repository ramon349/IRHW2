
for i in {1..5}; 
do 
    echo "Starting model training fold ${i}"
    java -jar RankLib.jar -norm zscore -train "./MQ2008/Fold${i}/train.txt" -test "./MQ2008/Fold${i}/test.txt" -validate "./MQ2008/Fold${i}/vali.txt" -ranker 6 -metric2t MAP -metric2T NDCG@10 -save "base_model_f${i}.txt"
    echo " Start training augmented model "
    java -jar RankLib.jar -norm zscore -train "./augData1/Fold_${i}/train.txt" -test "./augData1/Fold_${i}/test.txt" -validate "./augData1/Fold_${i}/vali.txt" -ranker 6 -metric2t MAP -metric2T NDCG@10 -save "aug_model_f${i}.txt"
done 
