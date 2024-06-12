function val = value_function(val, dis_fac, iteration, a,length,height,rew,mice,cat,cheese,fear,hunger)
    for k = 1:iteration
        for i = 1:length
            for j = 1:height 
                v_next = zeros([4,1]);
                if j + 1 <= height
                    v_next(1) = val(i, j + 1);
                end
                if j - 1 >= 1
                    v_next(2) = val(i, j - 1);
                end
                if i - 1 >= 1
                    v_next(3) = val(i - 1, j);
                end
                if i + 1 <= length
                    v_next(4)= val(i + 1, j);
                end
                val(i, j) = val(i, j) + a * (rew(i, j) + dis_fac * max(trans_matrix(i, j,mice,cat,cheese,fear,hunger,length,height)*v_next) - val(i, j));
            end
        end
    end
end