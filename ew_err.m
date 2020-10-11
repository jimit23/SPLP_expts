function err = ew_err(M, M_hat)

k = size(M, 2);

col_perms = perms([1:k]);

err = Inf;
for p=1:size(col_perms, 1)
    curr_M = M(:, col_perms(p, :));
    curr_err = max(max(abs(curr_M - M_hat)));
    err = min(err, curr_err);
end
