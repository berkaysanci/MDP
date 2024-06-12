clearvars

square=12;

grid_dim=[square,square];

mice=[2,2];
cheese=[6,6];

nest=mice;
cat=cat_rotation(cheese);

value_init = zeros(grid_dim) ;

mdp(cat, mice, cheese,nest, value_init, 0.9, 0.9,grid_dim(1),grid_dim(2))