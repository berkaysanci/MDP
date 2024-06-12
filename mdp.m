function mdp(cat_array, mice, cheese,nest, value_initial, discount, lear_rate,length,height)
    cat = cat_array(1,:);
    value = value_initial;
    reward=reward_func([length,height], cheese, cat);

    hunger = 0.2;
    fear = 0;
    peynir_flag=0;
    iteration = 0;

    while 1 == 1
        mice_cat_dis_old = dis(mice,cat);
        value = value_function(value, discount,20,lear_rate,length,height,reward,mice,cat,cheese,fear,hunger);
        mice = policy(mice, value,length,height,mice,cat,cheese,fear,hunger);

        iteration = iteration+1;
        cat=cat_array(mod(iteration,size(cat_array,1))+1,:);
        mice_cat_dis_new = dis(mice,cat);

        fear = fear+(mice_cat_dis_old-mice_cat_dis_new)/1000;

        if peynir_flag == 0
            reward = reward_func([length, height], cheese, cat);
        else
            reward = reward_func(([length, height]), nest, cat);
            cheese = mice;
        end

        if all(mice == cheese) && peynir_flag == 0
            hunger = 0;
            peynir_flag = 1;
        else
            hunger = hunger+ 0.001;
        end

        if all(mice == cat)
            disp="kedi yakaladı"
            break
        end

        if all(mice == nest) && peynir_flag == 1
            disp="peyniri aldı ve yuvaya götürdü"
            break
        end

    end
end