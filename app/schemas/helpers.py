from graphene import (Interface, Int)


class TotalCount(Interface):
    """ Return Row Count """
    total_count = Int()

    def resolve_total_count(self, info):
        """  Return Row Count """
        return self.length
