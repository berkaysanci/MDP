function trans = trans_matrix(state_x, state_y,mice,cat,cheese,fear,hunger,length,height)
    trans = [0.7, 0.1, 0.1, 0.1;
             0.1, 0.7, 0.1, 0.1;
             0.1, 0.1, 0.7, 0.1;
             0.1, 0.1, 0.1, 0.7];

    if state_y + 1 > height
        trans(:, 1) = zeros(1,4);
    end
    if state_y - 1 < 1
        trans(:, 2) = zeros(1,4);
    end
    if state_x - 1 < 1
        trans(:, 3) = zeros(1,4);
    end
    if state_x + 1 > length
        trans(:, 4) = zeros(1,4);
    end
    
    for i = 1:size(trans,1)
        if sum(trans(i,:)) ~= 1.0
            fark = 1-sum(trans(i,:));
            bolum = sum(trans(i,:) ~= 0);
            eklenti = fark / bolum;
            for j = 1:size(trans,1)
                if trans(i, j) ~= 0
                    trans(i, j) = trans(i, j)+eklenti;
                end
            end
        end
    end

    action_fear = [dis(mice+[0,1],cat),dis(mice+[0,-1],cat),dis(mice+[-1,0],cat),dis(mice+[+1,0],cat)];

    ind_fear = find(max(action_fear) == action_fear);

    action_hunger = [dis(mice+[0,1],cheese),dis(mice+[0,-1],cheese),dis(mice+[-1,0],cheese),dis(mice+[+1,0],cheese)];

    ind_hunger = find(min(action_hunger) == action_hunger);


    for i = 1:size(trans,1)
        if all(trans(:,i) ~= zeros(4))
            if i == ind_fear
                trans(:, i) = trans(:,i) + fear;
            else
                trans(:, i) = trans(:, i) - fear/(nnz(trans(i,:))-1);
            end
            if i == ind_hunger
                trans(:, i) = trans(:,i) + hunger;
            elseif i ~= ind_hunger
                trans(:, i) = trans(:, i) - hunger/(nnz(trans(i,:))-1);
            end
        end
    end

    for i = 1: size(trans, 1)
        for j = 1: size(trans, 2)
            if trans(i, j) >= 1
                trans(i, j) = 1;
            end
            if trans(i, j) <= 0
                trans(i, j) = 0;
            end
        end
    end

    for i = 1: size(trans, 1)
        trans(i,:)=trans(i,:)/sum(trans(i,:));
    end

end