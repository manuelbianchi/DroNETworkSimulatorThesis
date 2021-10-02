test baselines
for nd in "5" "8" "10" "15" "20" "25" "30";
do 
    for alg in "SVF" "CPVF";
    do 
        echo "run: ${alg} - ndrones ${nd} "
        python3 -m src.experiments.experiment_ndrones -nd ${nd} -i_s 0 -e_s 10 -alg ${alg} &
        python3 -m src.experiments.experiment_ndrones -nd ${nd} -i_s 10 -e_s 20 -alg ${alg} &
        python3 -m src.experiments.experiment_ndrones -nd ${nd} -i_s 20 -e_s 30 -alg ${alg} &
    done;
done; 
wait

python3 -m src.experiments.json_and_plot -nd 5 -nd 10 -nd 15 -nd 20 -nd 25 -nd 30 -i_s 1 -e_s 30 -exp_suffix SVF -exp_suffix CPVF

#test speeds
#for ns in "3" "5" "8" "12" "14";
#do
#	for alg in "SVF" "CPVF";
#        do
#		echo "run: ${alg} - speed ${ns} "
#        	python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 0 -e_s 10 -alg ${alg} &
#        	python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 10 -e_s 20 -alg ${alg} &
#        	python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 20 -e_s 30 -alg ${alg} &
#        done;
#done;
#wait
#
#python3 -m src.experiments.json_and_plot -ns 3 -ns 5 -ns 8 -ns 12 -ns 14 -i_s 1 -e_s 30 -exp_suffix SVF -exp_suffix CPVF

#for ns in "18";
#do
#    for alg in "CPVF" "SVF";
#    do
#        echo "run: ${alg} - speed ${ns} "
#        python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 0 -e_s 5 -alg ${alg} &
#        python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 5 -e_s 10 -alg ${alg} &
#        python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 10 -e_s 15 -alg ${alg} &
#	python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 15 -e_s 20 -alg ${alg} &
#	python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 20 -e_s 25 -alg ${alg} &
#	python3 -m src.experiments.experiment_ndrones -ns ${ns} -i_s 25 -e_s 30 -alg ${alg} &
#    done;
#done;
#wait

