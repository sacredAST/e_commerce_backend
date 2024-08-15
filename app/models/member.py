class Role:
    def __init__(self, name, access_level):
        self.name = name
        self.access_level = access_level

class AdminMember(Role):
    def __init__(self):
        super().__init__("Admin Member", "full_access")

class CustomerSupport(Role):
    def __init__(self):
        super().__init__("Customer Support", "limited_access")

class OrderAgent(Role):
    def __init__(self):
        super().__init__("Order Agent", "stock_management")

class ProductManager(Role):
    def __init__(self):
        super().__init__("Product Manager", "product_management")

class WarehouseStaff(Role):
    def __init__(self):
        super().__init__("Warehouse Staff", "shipment_access")

class Member:
    def __init__(self, username, role):
        self.username = username
        self.role = role

members = [
    Member("admin", AdminMember()),
    Member("support", CustomerSupport()),
    Member("order_agent", OrderAgent()),
    Member("product_manager", ProductManager()),
    Member("warehouse_staff", WarehouseStaff())
]

def get_member(username):
    for member in members:
        if member.username == username:
            return member
    return None

def check_access(member, feature):
    role_access_map = {
        "full_access": ["*"],
        "limited_access": ["order_info", "customer_reviews", "returns"],
        "stock_management": ["stock_levels", "sales_data", "shipment_management"],
        "product_management": ["product_add", "product_edit", "product_update"],
        "shipment_access": ["shipment_access", "unit_received"]
    }

    if member.role.access_level in role_access_map:
        allowed_features = role_access_map[member.role.access_level]
        if feature in allowed_features or "*" in allowed_features:
            return True
    
    return False

# Example usage
member = get_member("admin")
print(member.username, member.role.name, member.role.access_level)
print(check_access(member, "product_add"))
