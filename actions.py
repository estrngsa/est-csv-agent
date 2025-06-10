def get_max_item_info(csv_data):
    """
    Retorna um dicionário com todos os campos do header + os campos do item
    que teve maior QUANTIDADE.
    """
    max_q = -float("inf")
    best = None
    for nf in csv_data.values():
        head = nf["head"]
        for item in nf["items"]:
            q = item.get("QUANTIDADE", 0)
            if q > max_q:
                max_q = q
                # copia o header e injeta os campos do item
                best = {
                    **{f"head_{k}": v for k, v in head.items()},
                    **{f"item_{k}": v for k, v in item.items()},
                }
    return best


def get_max_head_info(csv_data):
    """
    Retorna um dicionário com todos os campos do header que teve maior VALOR NOTA FISCAL.
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
