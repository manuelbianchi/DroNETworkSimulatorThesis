test speeds
for ns in "3" "5" "8" "12" "15" "18";
do
       for alg in "SVF" "CPVF";
        do
               echo "run: ${alg} - speed ${ns} "
               python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 0 -e_s 10 -alg ${alg} &
               python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 10 -e_s 20 -alg ${alg} &
               python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 20 -e_s 30 -alg ${alg} &
        done;
done;
wait

python3 -m src.experiments.json_and_plot_nspeeds -ns 3 -ns 5 -ns 8 -ns 12 -ns 15 -ns 18 -i_s 1 -e_s 30 -exp_suffix SVF -exp_suffix CPVF

#for ns in "18";
#do
#    for alg in "CPVF" "SVF";
#    do
#        echo "run: ${alg} - speed ${ns} "
#        python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 0 -e_s 5 -alg ${alg} &
#        python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 5 -e_s 10 -alg ${alg} &
#        python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 10 -e_s 15 -alg ${alg} &
#        python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 15 -e_s 20 -alg ${alg} &
#        python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 20 -e_s 25 -alg ${alg} &
#        python3 -m src.experiments.experiment_nspeeds -ns ${ns} -i_s 25 -e_s 30 -alg ${alg} &
#    done;
#done;
#wait

