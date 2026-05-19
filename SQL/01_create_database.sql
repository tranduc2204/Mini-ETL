CREATE SCHEMA OLTP


CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT,
    status VARCHAR(50),
    total_amount NUMERIC(10,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pipeline_state (
    pipeline_name VARCHAR PRIMARY KEY,
    last_watermark TIMESTAMP
);


CREATE TABLE orders_cdc_log (
    log_id SERIAL PRIMARY KEY,
    operation_type VARCHAR(10),
    order_id INT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);