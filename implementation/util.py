def unique_list(l):
    return list(set(l))


def unique_concatenate(l1, l2):
    return unique_list(unique_list(l1) + unique_list(l2))
