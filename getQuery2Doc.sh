echo -e "qid \t did" > MQ2008_list.txt
awk '{split($2,ou,":"); print ou[2] "\t" $51}' Large_NULL.txt >> MQ2008_list.txt
