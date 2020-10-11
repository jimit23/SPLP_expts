function J = spa(A, k)

J = zeros(k,1);

for i = 1:k
    [~, ind] = max(sum(A.*A));
    J(i) = ind;
    uj = A(:, ind);
    A = A - (uj*(uj'*A)/norm(uj)^2);
end
