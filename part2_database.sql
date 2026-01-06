create table companies (
    id primary key,
    name text not null
);
create table warehouses(
    id primary key,
    name text not null,
    company_id integer ,
    foreign key company_id references companies(id)
);
create table products(
    id primary key,sku text unique not null,
    name text not null,
    price decimal(10,2),
    is_bundle boolean default false
);
create table inventory(
    product_id int ,
    warehouse_id int,
    foreign key product_id references products(id),
    foreign key warehouse_id_id references warehouses(id),
    primary key (product_id,warehouse_id)
);
create table inventory_log(
    -- to track changes everytime
    id primary key,
    product_id int ,
    warehouse_id int ,
    foreign key product_id references products(id),
    foreign key warehouse_id_id references warehouses(id),
    change_amount int,
    reason text,
    created_at timestamp default now()
);
create table suppliers(
    id primary key,
    name text not null,
    phone bigint
);

create table supplier_products(
    supplier_id int,
    foreign key supplier_id references suppliers(id),
    product_id int ,
    foreign key product_id references products(id),
    cost decimal(10,2)
);

create index idx_warehouse_company on warehouses(id);
create index idx_inventory_warehouese on inventory(warehouse_id);
-- this will help us to look inventory by warehouse

--finally
create index idx_date on inventory_log(created_at);
--this will help us to sort log history by date fastly