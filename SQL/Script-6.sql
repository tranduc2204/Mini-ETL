create schema OLTP
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT,
    status VARCHAR(50),
    total_amount NUMERIC(10,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (user_id, status, total_amount, updated_at)
VALUES
(101, 'Pending',   120.50, '2026-05-10 08:15:00'),
(102, 'Completed', 450.00, '2026-05-10 09:30:00'),
(103, 'Cancelled',  75.99, '2026-05-10 10:05:00'),
(104, 'Completed', 999.99, '2026-05-11 11:20:00'),
(105, 'Pending',   210.75, '2026-05-11 13:45:00'),
(101, 'Shipped',   330.40, '2026-05-12 14:10:00'),
(106, 'Completed',  89.90, '2026-05-12 15:25:00'),
(107, 'Pending',   560.00, '2026-05-13 16:50:00'),
(108, 'Returned',  145.30, '2026-05-14 18:00:00'),
(109, 'Completed', 720.15, '2026-05-15 19:35:00');

select *
from orders

CREATE TABLE pipeline_state (
    pipeline_name VARCHAR PRIMARY KEY,
    last_watermark TIMESTAMP
);

-- TABLE ORDER_CDC_LOG 
CREATE TABLE orders_cdc_log (
    log_id SERIAL PRIMARY KEY,
    operation_type VARCHAR(10),
    order_id INT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Trigger function
--
--Function này sẽ:
--
--detect INSERT
--detect UPDATE
--detect DELETE

CREATE OR REPLACE FUNCTION track_orders_changes()
RETURNS TRIGGER AS $$
BEGIN

    -- INSERT
    IF TG_OP = 'INSERT' THEN

        INSERT INTO orders_cdc_log (
            operation_type,
            order_id,
            changed_at
        )
        VALUES (
            'INSERT',
            NEW.order_id,
            CURRENT_TIMESTAMP
        );

        RETURN NEW;
    END IF;

    -- UPDATE
    IF TG_OP = 'UPDATE' THEN

        INSERT INTO orders_cdc_log (
            operation_type,
            order_id,
            changed_at
        )
        VALUES (
            'UPDATE',
            NEW.order_id,
            CURRENT_TIMESTAMP
        );

        -- auto update updated_at
        NEW.updated_at = CURRENT_TIMESTAMP;

        RETURN NEW;
    END IF;

    -- DELETE
    IF TG_OP = 'DELETE' THEN

        INSERT INTO orders_cdc_log (
            operation_type,
            order_id,
            changed_at
        )
        VALUES (
            'DELETE',
            OLD.order_id,
            CURRENT_TIMESTAMP
        );

        RETURN OLD;
    END IF;

    RETURN NULL;

END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER orders_cdc_trigger
BEFORE INSERT OR UPDATE OR DELETE
ON orders
FOR EACH ROW
EXECUTE FUNCTION track_orders_changes();

select *
from orders

INSERT INTO orders (user_id, status, total_amount)
VALUES
(991, 'Pending',   22042002)


select *
from pipeline_state

INSERT INTO pipeline_state
VALUES ('orders_cdc', '2026-5-16');


select *
from orders_cdc_log


select *
from orders 
where order_id = 4
update orders 
set total_amount = 2204
where order_id = 4


select *
from pipeline_state
select *
from orders_cdc_log

update pipeline_state

pipeline_state

CREATE TABLE processed_files (
    file_name TEXT PRIMARY KEY,
    processed_at TIMESTAMP
    
);

select *
from processed_files

delete FROM  processed_files
where file_name = 'data/bronze/orders_20260518082630.csv'



select *
from pipeline_state
where pipeline_name = 'orders_cdc'


delete from orders_cdc_log 
delete from pipeline_state 
delete from processed_files 
delete from ordeRS 
------------------------------------------------- check business rule-----------------------------
select *
from ordeRS



update orders 
set total_amount = 2002
where order_id = 44


select *
from orders_cdc_log


select *
from processed_files  



