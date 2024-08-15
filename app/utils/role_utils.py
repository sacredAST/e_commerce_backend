ROLE_MAPPING = {
    -1: "UnAllowed",
    0: "Warehouse Staff",
    1: "Product Manager",
    2: "Order Agent",
    3: "Customer Support",
    4: "Administrator"
}

def convert_role_to_string(role: int) -> str:
    return ROLE_MAPPING.get(role, "Unknown")