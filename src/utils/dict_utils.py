def rename_key(d, old_key, new_key):
    return {(new_key if k == old_key else k): v for k, v in d.items()}
