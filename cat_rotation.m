function A = cat_rotation(cheese)
    cheese_x = cheese(1);
    cheese_y = cheese(2);
    rotation=[[0,-2];[1,-1];[2,0];[1,1];[0,+2];[-1,1];[-2,0];[-1,-1]];
    A=zeros(size(rotation));
    for i = 1:size(A,1)
        A(i,:)=[cheese_x,cheese_y]-rotation(i,:);
    end
end