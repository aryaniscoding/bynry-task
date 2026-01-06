create table sales_order(
    id primary key,
    creaed_at timestamp default NOW()
);

create table sales_order_items(
    id primary key,
    order_id int,
    foreign key order_id references sales_order(id),
    product_id int ,
    foreign key product_id references products(id),
    quantity int
);