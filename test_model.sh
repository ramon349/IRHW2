echo " Starting test" 
for i in {1..5};
do 
mkdir "output${i}"
java -jar RankLib.jar -norm zscore -load "./base_model_f${i}.txt" -test "./MQ2007/Fold${i}/test.txt" -metric2T NDCG@10 -idv "./output${i}/baseline.txt"
java -jar RankLib.jar -norm zscore -load "./aug_model_f${i}.txt" -test "./augData/Fold_${i}/test.txt" -metric2T NDCG@10 -idv "./output${i}/aug.txt"
java -cp RankLib.jar ciir.umass.edu.eval.Analyzer -all "./output${i}/" -base baseline.txt > "analysis${i}.txt"
done 

java -cp RankLib.jar ciir.umass.edu.eval.Analyzer -all "./output1/" -base baseline.txt > "analysis_general.txt"