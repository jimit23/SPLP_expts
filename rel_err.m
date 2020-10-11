function err = rel_err(M, M_hat)

k = size(M, 2);

col_perms = perms([1:k]);

err = Inf;
err_den = norm(M, 'fro');
for p=1:size(col_perms, 1)
    curr_M = M(:, col_perms(p, :));
    curr_err = norm(curr_M - M_hat, 'fro')/err_den;
    err = min(err, curr_err);
end
