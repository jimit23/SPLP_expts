clear
% parameters -------------------------------------
n = 5000;                             % number of nodes
k = 3;                              % number of communities
alpha = 0.5*ones(k, 1);            % dirichlet parameters
alpha(1) = 0.4*alpha(1);
alpha(k) = 4*alpha(k);
samples = round(n^0.5);           % number of samples to generate A
rho = 1;                            % sparsity parameter in MMSB
% ------------------------------------------------

% generate B -------------------------------------
% eps = 0.9;
% B = (1-eps)*eye(k) + eps*ones(k, k);
B = diag(0.5*ones(k, 1) + 0.5*rand(k, 1));
% ------------------------------------------------

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
% -----------------------------------------------

% execute splp ----------------------------------
tic
J = spa(A, k);
assert (min(J) > 0)
time_spa = toc;

tic
theta_lp = lp(A, J, k);
time_lp = toc;
% -----------------------------------------------

% calculate relative errors
r_ers_geo = rel_err(theta, theta_geo);
r_ers_lp = rel_err(theta, theta_lp);

% calculate entrywise errors
e_ers_geo = ew_err(theta, theta_geo);
e_ers_lp = ew_err(theta, theta_lp);

disp(['----------------------------------------------------------'])
disp(['graph size: ', num2str(n)])
disp(['avg relative error in GeoNMF: ', num2str(r_ers_geo)])
disp(['avg relative error in SPLP: ', num2str(r_ers_lp)])

disp(['avg entrywise error in GeoNMF: ', num2str(e_ers_geo)])
disp(['avg entrywise error in SPLP: ', num2str(e_ers_lp)])

