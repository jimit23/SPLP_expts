function theta_hat = lp(A, J, k)

n = size(A, 1);
[Q, ~] = eigs(A, k, 'la');
% V = Q(:, n-k+1:n);
V=Q;

theta_hat = zeros(n, k);
for i=1:k
    cvx_begin quiet
    variable y(size(V,2))
    minimize sum(V*y)
    subject to
    V(J(i),:)*y==1
    V*y >= 0
    cvx_end
    theta_hat(:, i) = V*y/max(V*y);
end
