def get_max_item_info(csv_data):
    """
    Returns a dictionary with all header fields plus the fields of the item
    that had the highest QUANTITY.
    """
    max_q = -float("inf")
    best = None
    for nf in csv_data.values():
        head = nf["head"]
        for item in nf["items"]:
            q = item.get("QUANTIDADE", 0)
            if q > max_q:
                max_q = q
                best = {
                    **{f"head_{k}": v for k, v in head.items()},
                    **{f"item_{k}": v for k, v in item.items()},
                }
    return best


def get_max_head_info(csv_data):
    """
    Returns a dictionary with all header fields for the invoice with the highest INVOICE VALUE.
    """
    max_val = -float("inf")
    best = None
    for nf in csv_data.values():
        head = nf["head"]
        v = head.get("VALOR NOTA FISCAL", 0)
        if v > max_val:
            max_val = v
            best = head.copy()
    return best
