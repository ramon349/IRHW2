echo "Processing 2008 data"
awk '{split($2,ou,":"); print ou[2] "\t" $51}' ./utils/MQ2008_large_null.txt > ./MQ2008/simi_list.txt
echo "Calling python script on 2008 "
python3 ./get_simi.py ./utils/2008_large_simi.txt ./MQ2008/simi_feats.txt
echo "Processing 2007 data"
awk '{split($2,ou,":"); print ou[2] "\t" $51}' ./utils/MQ2007_large_null.txt > ./MQ2007/simi_list.txt
echo "Calling python script on 2007"
python3 ./get_simi.py ./utils/2007_large_simi.txt ./MQ2007/simi_feats.txt