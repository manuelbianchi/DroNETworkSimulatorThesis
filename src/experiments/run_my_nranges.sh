#test speeds
#for nc in "150" "175" "200" "225" "250" "275";
#do
#       for alg in "SVF" "CPVF" "FLOOR";
#        do
#               echo "run: ${alg} - com_ranges ${nc} "
#               python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 0 -e_s 10 -alg ${alg} &
#               python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 10 -e_s 20 -alg ${alg} &
#               python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 20 -e_s 30 -alg ${alg} &
#        done;
#done;
#wait

python3 -m src.experiments.json_and_plot_nranges -nc 150 -nc 175 -nc 200 -nc 225 -nc 250 -nc 275 -i_s 1 -e_s 30 -exp_suffix SVF -exp_suffix CPVF -exp_suffix FLOOR

#for nc in "275";
#do
#    for alg in "CPVF" "SVF";
#    do
#        echo "run: ${alg} - com_ranges ${nc} "
#        python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 0 -e_s 5 -alg ${alg} &
#        python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 5 -e_s 10 -alg ${alg} &
#        python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 10 -e_s 15 -alg ${alg} &
#        python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 15 -e_s 20 -alg ${alg} &
#        python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 20 -e_s 25 -alg ${alg} &
#        python3 -m src.experiments.experiment_nranges -nc ${nc} -i_s 25 -e_s 30 -alg ${alg} &
#    done;
#done;
#wait

