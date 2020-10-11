data = xlsread('plot_data.xlsx');
n = data(:, 1);
g_avg = data(:, 2);
g_std = data(:, 3);
splp_avg = data(:, 4);
splp_std = data(:, 5);


% % error vs n -----------------------------------------
% errorbar(n, g_avg, g_std, '--o')
% hold on
% errorbar(n, splp_avg, splp_std, 'LineWidth', 2.5)
% xlabel('Number of nodes (n)', 'FontSize', 18)
% ylabel('Entrywise error', 'FontSize', 18)
% xlim([2500 12500])
% ylim([0.0 0.03])
% set(gca, 'fontsize', 16, 'YTick', (0.0:0.01:0.03), 'Xtick', (0:2000:12000))
% legend('GeoNMF', 'SP+LP')
% legend('Location', 'Northwest')
% % ----------------------------------------------------

% % error vs k -----------------------------------------
% errorbar(k, g_avg, g_std, '--o')
% hold on
% errorbar(k, splp_avg, splp_std, 'LineWidth', 2.5)
% xlabel('Number of communities (k)', 'FontSize', 18)
% ylabel('Entrywise error', 'FontSize', 18)
% xlim([1.5 8.5])
% ylim([0.0 0.3])
% set(gca, 'fontsize', 16, 'YTick', (0.0:0.1:0.3))
% set(gca, 'fontsize', 16)
% legend('GeoNMF', 'SP+LP')
% legend('Location', 'Northwest')
% % ----------------------------------------------------

% % error vs alpha -----------------------------------------
% errorbar(alpha, g_avg, g_std, '--o')
% hold on
% errorbar(alpha, splp_avg, splp_std, 'LineWidth', 2.5)
% xlabel({'$\alpha$'}, 'Interpreter', 'latex', 'FontSize', 18)
% ylabel('Entrywise error', 'FontSize', 18)
% xlim([0 2.5])
% ylim([0.0 0.16])
% set(gca, 'fontsize', 16, 'YTick', (0.0:0.04:0.15))
% set(gca, 'fontsize', 16)
% legend('GeoNMF', 'SP+LP')
% legend('Location', 'Northwest')
% % ----------------------------------------------------

% time vs n -----------------------------------------
errorbar(n, g_avg, g_std, '--o')
hold on
errorbar(n, splp_avg, splp_std, 'LineWidth', 2.5)
xlabel('Number of nodes (n)', 'FontSize', 18)
ylabel('Wall-clock running time - log scale (s)', 'FontSize', 18)
xlim([2500 12500])
set(gca, 'fontsize', 16, 'YScale', 'log','YminorTick', 'off')
legend('GeoNMF', 'SP+LP')
legend('Location', 'Northwest')
% ----------------------------------------------------

% % error vs off diag B -----------------------------------------
% errorbar(eps, g_avg, g_std, '--o')
% hold on
% errorbar(eps, splp_avg, splp_std, 'LineWidth', 2.5)
% xlabel({'$\delta$'}, 'Interpreter', 'latex', 'FontSize', 18)
% ylabel('Entrywise error', 'FontSize', 18)
% xlim([0 1])
% ylim([0.0 0.18])
% set(gca, 'fontsize', 16, 'YTick', (0.0:0.06:0.18))
% set(gca, 'fontsize', 16)
% legend('GeoNMF', 'SP+LP')
% legend('Location', 'Northwest')
% % ----------------------------------------------------

% % time vs off diag B -----------------------------------------
% errorbar(eps, g_avg, g_std, '--o')
% hold on
% errorbar(eps, splp_avg, splp_std, 'LineWidth', 2.5)
% xlabel({'$\delta$'}, 'Interpreter', 'latex', 'FontSize', 18)
% ylabel('Wall-clock running time (s)', 'FontSize', 18)
% xlim([0 1])
% % ylim([0.0 0.18])
% % set(gca, 'fontsize', 16, 'YTick', (0.0:0.06:0.18))
% set(gca, 'fontsize', 16)
% legend('GeoNMF', 'SP+LP')
% legend('Location', 'Northwest')
% % ----------------------------------------------------
 
