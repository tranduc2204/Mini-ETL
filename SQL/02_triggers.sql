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
