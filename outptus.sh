

python3 ./process_folder.py ./2007_analysis/ perl_comp_*_base.txt 1 > 2007_perf_base_MAP.txt
python3 ./process_folder.py ./2007_analysis/ perl_comp_*_aug.txt 1 > 2007_perf_aug_MAP.txt

python3 ./process_folder.py ./2007_analysis/ perl_comp_*_base.txt 4 > 2007_perf_base_NDCG.txt
python3 ./process_folder.py ./2007_analysis/ perl_comp_*_aug.txt 4 > 2007_perf_aug_NDCG.txt


python3 ./process_folder.py ./2008_analysis/ perl_comp_*_base.txt 1 > 2008_perf_base_MAP.txt
python3 ./process_folder.py ./2008_analysis/ perl_comp_*_aug.txt 1 > 2008_perf_aug_MAP.txt

python3 ./process_folder.py ./2008_analysis/ perl_comp_*_base.txt 4 > 2008_perf_base_NDCG.txt
python3 ./process_folder.py ./2008_analysis/ perl_comp_*_aug.txt 4 > 2008_perf_aug_NDCG.txt