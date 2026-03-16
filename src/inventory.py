def check_inventory(predicted_demand, current_stock=300):

    predicted_demand = int(predicted_demand)

    safety_stock = 100
    total_required = predicted_demand + safety_stock

    if current_stock < total_required:
        order_quantity = total_required - current_stock
        alert = "⚠ Low Stock! Generate Procurement Order."
    else:
        order_quantity = 0
        alert = "✅ Stock Level is Sufficient."

    return order_quantity, alert