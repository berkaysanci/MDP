function A = policy(mice_mat, val_,length,height,mice,cat,cheese,fear,hunger)
    mice_x = mice_mat(1);
    mice_y = mice_mat(2);
    v_next = zeros([4,1]);
    
    if mice_y + 1 <= height
        v_next(1) = val_(mice_x, mice_y + 1);
    end
    if mice_y - 1 >= 1
        v_next(2) = val_(mice_x, mice_y - 1);
    end
    if mice_x - 1 >= 1
        v_next(3) = val_(mice_x - 1, mice_y);
    end
    if mice_x + 1 <= length
        v_next(4)= val_(mice_x + 1, mice_y);
    end
    trans = trans_matrix(mice_x, mice_y,mice,cat,cheese,fear,hunger,length,height);
    matrix = trans*v_next;
    utility = max(matrix) ;
    indeks = utility == matrix ;
    action_set = {'UP', 'DOWN', 'LEFT', 'RIGHT'} ;
    
    cp = [0, cumsum(trans(indeks,:))];
    r = rand;
    ind = find(r>cp, 1, 'last');
    action = action_set{ind};

    if strcmp(action,'UP')
        mice_y = mice_y+ 1;
    elseif strcmp(action,'DOWN')
        mice_y = mice_y- 1;
    elseif strcmp(action,'LEFT')
        mice_x = mice_x- 1;
    elseif strcmp(action,'RIGHT')
        mice_x = mice_x+ 1;
    end
    A = [mice_x,mice_y];
end
