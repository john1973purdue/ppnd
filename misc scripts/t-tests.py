# t tests

import scipy.stats
import math
import csv

mean_b_avg_adults = [0, 0.002037, 0.001989, 0.003154, 0.004705, 0.006176, 0.007734, 0.008913, 0.010063, 0.011334, 0.012165, 0.012332, 0.013015, 0.013229]

sd_b_avg_adults = [1, 0.004505, 0.002852, 0.002608, 0.003037, 0.003290, 0.003382, 0.003653, 0.003848, 0.004235, 0.004449, 0.004374, 0.004431, 0.005012]

mean_ps_avg_adults = [0.028290, 0.035447, 0.038369, 0.048582, 0.053628, 0.058455, 0.062729, 0.064337, 0.066162, 0.067880, 0.068057, 0.066981, 0.067243, 0.066945]

sd_ps_avg_adults = [0.037620, 0.026812, 0.017385, 0.014386, 0.013881, 0.013021, 0.011872, 0.010870, 0.010338, 0.010614, 0.010814, 0.010456, 0.010424, 0.010732]

mean_nd_adults = [26.000000, 26.846775, 20.712584, 15.715158, 7.256381, 3.882833, 2.559244, 1.893046, 1.484651, 1.238584, 1.012799, 0.727300, 0.582104, 0.433911]

sd_nd_adults = [3.126944, 8.652312, 9.491070, 9.054614, 5.147934, 3.121207, 2.239700, 1.746530, 1.461331, 1.337486, 1.188452, 0.940839, 0.793725, 0.685791]

count_adults = [10, 124, 755, 2784, 5250, 7724, 9942, 10210, 9642, 7796, 5469, 3315, 2034, 1097]

mean_b_avg_children = [0, 0.003147, 0.003824, 0.005074, 0.007794, 0.009706, 0.012846, 0.013547, 0.016966, 0.017159, 0.017942, 0.029237, 0.041245, 0.097412]

sd_b_avg_children = [1, 0.002434, 0.002982, 0.002751, 0.003881, 0.004382, 0.005769, 0.006343, 0.007893, 0.008240, 0.007535, 0.010902, 0.015340, 1]

mean_ps_avg_children = [0.010339, 0.046131, 0.045250, 0.060524, 0.064550, 0.070058, 0.074337, 0.074902, 0.079493, 0.078639, 0.076027, 0.104068, 0.100413, 0.123791]

sd_ps_avg_children = [0.006304, 0.019481, 0.023530, 0.019298, 0.016710, 0.016577, 0.015923, 0.014824, 0.017210, 0.018244, 0.014121, 0.023057, 0.030468, 1]

mean_nd_children = [14.400000, 13.063829, 8.276316, 6.367213, 3.036481, 1.809083, 1.328310, 0.908689, 0.690773, 0.435897, 0.328358, 0.526316, 0.000000, 0.000000]

sd_nd_children = [4.159327, 4.483808, 4.595128, 4.316643, 2.353953, 1.614714, 1.298567, 1.063152, 0.877006, 0.683251, 0.612695, 0.964274, 0.000000, 1]

count_children = [5, 47, 152, 610, 932, 1079, 929, 679, 401, 156, 67, 19, 6, 2]

results_b_avg = []
results_ps_avg = []
results_nd = []

with open("./t-tests.txt", "w") as f:

    for i, c in enumerate(mean_b_avg_adults):
        ttest_b_avg = scipy.stats.ttest_ind_from_stats(mean_b_avg_adults[i], sd_b_avg_adults[i], count_adults[i], mean_b_avg_children[i], sd_b_avg_children[i], count_children[i])
        ttest_ps_avg = scipy.stats.ttest_ind_from_stats(mean_ps_avg_adults[i], sd_ps_avg_adults[i], count_adults[i], mean_ps_avg_children[i], sd_ps_avg_children[i], count_children[i])
        ttest_nd = scipy.stats.ttest_ind_from_stats(mean_nd_adults[i], sd_nd_adults[i], count_adults[i], mean_nd_children[i], sd_nd_children[i], count_children[i])
        
        results_b_avg = [ttest_b_avg[0],ttest_b_avg[1],mean_b_avg_adults[i],sd_b_avg_adults[i],count_adults[i],mean_b_avg_children[i],sd_b_avg_children[i],count_children[i]]
        results_ps_avg = [ttest_ps_avg[0],ttest_ps_avg[1],mean_ps_avg_adults[i],sd_ps_avg_adults[i],count_adults[i],mean_ps_avg_children[i],sd_ps_avg_children[i],count_children[i]]
        results_nd = [ttest_nd[0],ttest_nd[1],mean_nd_adults[i],sd_nd_adults[i],count_adults[i],mean_nd_children[i],sd_nd_children[i],count_children[i]]
        
        results_b_avg.append((mean_b_avg_adults[i] - mean_b_avg_children[i]) / math.sqrt((sd_b_avg_adults[i] ** 2 + sd_b_avg_children[i] ** 2) / 2))
        results_ps_avg.append((mean_ps_avg_adults[i] - mean_ps_avg_children[i]) / math.sqrt((sd_ps_avg_adults[i] ** 2 + sd_ps_avg_children[i] ** 2) / 2))
        results_nd.append((mean_nd_adults[i] - mean_nd_children[i]) / math.sqrt((sd_nd_adults[i] ** 2 + sd_nd_children[i] ** 2) / 2))
        
        #print(str(i+1))
        #print("B")
        #print(results_b_avg)
        #print(cohens_b_avg)
        #print("PS")
        #print(results_ps_avg)
        #print(cohens_ps_avg)
        #print("ND")
        #print(results_nd)
        #print(cohens_nd)
        
        commaout = csv.writer(f, delimiter=',')
        
        commaout.writerow(results_b_avg+results_ps_avg+results_nd)



