CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_customers_updated_at
BEFORE UPDATE ON customers
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_vendors_updated_at
BEFORE UPDATE ON vendors
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_vendor_products_updated_at
BEFORE UPDATE ON vendor_products
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_delivery_persons_updated_at
BEFORE UPDATE ON delivery_persons
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_support_agents_updated_at
BEFORE UPDATE ON support_agents
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER trg_cases_updated_at
BEFORE UPDATE ON cases
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();