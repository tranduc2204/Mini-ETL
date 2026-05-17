

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
(111, 'Pending',   120.50)


select *
from pipeline_state

INSERT INTO pipeline_state
VALUES ('orders_cdc', '2026-5-16');


select *
from orders_cdc_log







