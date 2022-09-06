# define the basic schema of the project here
# should check on startup

def collections_common():
    collection_list = ['users']
    return collection_list


def collections_mumshoppe():
    collection_list = ['users', 'bundles','options', 'orders', 'shoppes']
    return collection_list


class template:
    collections_common = collections_common()
    collections_mumshoppe = collections_mumshoppe()
