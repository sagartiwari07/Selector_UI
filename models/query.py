from utility import covert_symbol


class Query:
    """

    This class constructor takes an optional list of queries. If no queries are given then it will return an empty
    dictionary.

    Query must be in the following format:

    1. [<fieldName>, <filedValue>] => {'fieldName': fieldValue}
    2. [<fieldName>, <Relational Operator> ,<rangeValue>] => {'fieldName': {'$lte': rangeValue}}
    3. [<fieldName>, <rangeValue1>, <rangeValue2>] => {'fieldName': {'$lte': rangeValue1, '$gte': rangeValue2}}

    """

    def __init__(self, query_list: list = None, **kwargs):
        self.field = ''
        self.query: dict = {}
        if kwargs.__contains__('key') and kwargs.__contains__('value'):
            self.query[kwargs.get('key')] = kwargs.get('value')
        elif query_list is not None:
            for arg in query_list:
                if isinstance(arg, list):
                    if arg[0] != 'srvtime':
                        self.field = f'value.{arg[0]}'
                    else:
                        self.field = arg[0]
                    if len(arg) == 2:
                        self.query[self.field] = arg[1]
                    elif len(arg) == 3 and covert_symbol(arg[1]) is not None:
                        self.query[self.field] = {
                            covert_symbol(arg[1]): arg[2]
                        }
                    else:
                        self.query[self.field] = {
                            covert_symbol('>'): arg[1],
                            covert_symbol('<'): arg[2]
                        }
            if query_list.count('or') > 0:
                self.query = {'$or': [{key: value} for key, value in self.query.items()]}

    def get(self) -> dict:
        return self.query
