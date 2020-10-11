clear
% parameters -------------------------------------
n = 6000;                             % number of nodes
k = 3;                              % number of communities
alpha = 0.5*ones(k, 1);            % dirichlet parameters
samples = round(n^0.5);           % number of samples to generate A
rho = 1;                            % sparsity parameter in MMSB
% ------------------------------------------------

% generate B -------------------------------------
% eps = 0.9;
% B = (1-eps)*eye(k) + eps*ones(k, k);
B = diag(0.5*ones(k, 1) + 0.5*rand(k, 1));
% ------------------------------------------------

r_ers_geo = zeros(10, 1);
r_ers_lp = zeros(10, 1);
e_ers_geo = zeros(10, 1);
e_ers_lp = zeros(10, 1);
times_geo = zeros(10, 1);
times_spa = zeros(10, 1);
times_lp = zeros(10, 1);
lptimes = zeros(10, 1);
for s=1:10
    % generate theta ---------------------------------
    theta = zeros(n, k);
    % generating dirichlet rvs in mmsb
    for i=1:n
        for j=1:k
            theta(i, j) = gamrnd(alpha(j), 1);
        end
        rsum = sum(theta(i, :));
        theta(i,:) = theta(i, :)/rsum;
    end
    % ------------------------------------------------

    % generate P -------------------------------------
    P = rho*theta*B*theta';
    assert (min(min(P))>=0)
    assert (max(max(P))>=0)
    % ------------------------------------------------

    % generate A ------------------------------------
    tic
    A = zeros(n, n);
    for t = 1:samples
        curr_A = (rand(n, n) < P); 
        curr_A = triu(curr_A) + triu(curr_A)';
        A = A + curr_A;
    end
    A = A/samples;
    for i = 1:n
        A(i, i) = 1;
    end
    disp(['finished generating A in: ', num2str(toc), ' seconds'])
    % -----------------------------------------------

    % execute geonmf --------------------------------
    tic
    [theta_geo, ~] = GeoNMF(A, k);
    time_geo = toc;
    times_geo(s) = time_geo;
    % -----------------------------------------------

    % execute splp ----------------------------------
    tic
    J = spa(A, k);
    assert (min(J) > 0)
    time_spa = toc;
    times_spa(s) = time_spa;

    tic
    [theta_lp, lpt] = lp(A, J, k);
    time_lp = toc;
    times_lp(s) = time_lp;
    lptimes(s) = lpt;
    % -----------------------------------------------

    % calculate relative errors
    r_ers_geo(s) = rel_err(theta, theta_geo);
    r_ers_lp(s) = rel_err(theta, theta_lp);
    
    % calculate entrywise errors
    e_ers_geo(s) = ew_err(theta, theta_geo);
    e_ers_lp(s) = ew_err(theta, theta_lp);
    
    disp(['GeoNMF executed in: ', num2str(time_geo), ' seconds'])
    disp(['SPLP executed in: ', num2str(time_spa), ' + ', num2str(time_lp), ' = ', num2str(time_spa+time_lp) ' seconds'])
    disp(['finished samples (out of 10): ', num2str(s)])
end

disp(['----------------------------------------------------------'])
disp(['avg relative error in GeoNMF: ', num2str(mean(r_ers_geo))])
disp(['std dev of relative error in GeoNMF: ', num2str(std(r_ers_geo))])
disp(['avg relative error in SPLP: ', num2str(mean(r_ers_lp))])
disp(['std dev of relative error in SPLP: ', num2str(std(r_ers_lp))])

disp(['avg entrywise error in GeoNMF: ', num2str(mean(e_ers_geo))])
disp(['std dev of entrywise error in GeoNMF: ', num2str(std(e_ers_geo))])
disp(['avg entrywise error in SPLP: ', num2str(mean(e_ers_lp))])
disp(['std dev of entrywise error in SPLP: ', num2str(std(e_ers_lp))])

disp(['condition number of B: ', num2str(cond(B))])

disp(['avg time for geonmf: ', num2str(mean(times_geo))])
disp(['std dev of time for geonmf: ', num2str(std(times_geo))])
disp(['avg time for SPLP: ', num2str(mean(times_spa + times_lp))])
disp(['std dev of time for SPLP: ', num2str(std(times_spa + times_lp))])

xlswrite('test.xlsx', [mean(r_ers_geo), std(r_ers_geo), mean(r_ers_lp), std(r_ers_lp), mean(e_ers_geo), ...
    std(e_ers_geo), mean(e_ers_lp), std(e_ers_lp), cond(B), mean(times_geo), std(times_geo)...
    mean(times_spa + times_lp), std(times_spa + times_lp)])
