# Snake
Trò chơi rắn Snake Xenzia sử dụng giải thuật Genetic với crossover đơn giản. 
Max population ban đầu là 800 con rắn, mỗi con có một mạng neural riêng (25 x 10 x 10 x 4)
Đầu vào của input layer là 8 hướng nhìn, mỗi hướng xác định khoảng cách từ head đến tường, đến thức ăn và đến chính đuôi của nó. Nếu vật xác định không nằm trong tầm nhìn của rắn thì input sẽ là -1
Input còn lại sẽ là hướng đi hiện tại của cái đầu
