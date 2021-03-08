def validate_as_int(number, boundaries: list):
    try:
        changed = int(number)
        if boundaries[0] <= changed <= boundaries[1]:
            return True, changed
        else:
            return False, changed
    except ValueError:
        return False, 0


def error():
    print("[ERR] Validation Error")
