function reward =  reward_func(grid,cheese_loc,cat_loc)
    reward = zeros(grid) + 0.01;

    che=[cheese_loc(1),cheese_loc(2)];
    catt=[cat_loc(1), cat_loc(2)];

    rew=+10;
    pun=-50;

    reward(che(1), che(2)) = rew;
    reward(catt(1), catt(2)) = pun;

    z = zeros([8, 2]);
    it = 1;
    for i = [-1, 0, 1]
        for j = [-1, 0, 1]
            if not (i == 0 && j == 0)
                z(it,:) = [i, j];
                it = it + 1;
            end
        end
    end

    reward_cheese = che.*ones([8,2]) - z;
    reward_cat = catt.*ones([8,2]) - z;

    for i = 1:grid(1)
        for j = 1:grid(2)
            if any(i == reward_cheese(:, 1)) && any(j == reward_cheese(:, 2))
                reward(i, j) = reward(i, j) + rew;
            end

            if any(i == reward_cat(:, 1)) && any(j == reward_cat(:,2))
                reward(i, j) = reward(i, j) +pun;
            end
        end
    end

end