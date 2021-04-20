""" Graphql Filter Module """
from graphene_sqlalchemy_filter import (FilterableConnectionField, FilterSet)
from .database import (Country as CountryModel, Location as LocationModel,
                       StateProvince as StateProvinceModel, Hive as HiveModel,
                       HiveData as HiveDataModel)


class CountryFilter(FilterSet):
    """Country Graphql Filter"""
    class Meta:
        """Country Graphql Filter output"""
        model = CountryModel
        fields = {
            'name': ['eq', 'ilike'],
            'shortName': ['eq']
        }


class StateProvinceFilter(FilterSet):
    """StateProvince Graphql Filter"""
    class Meta:
        """StateProvince Graphql Query output"""
        model = StateProvinceModel
        fields = {
            'name': ['eq', 'ilike'],
            'abbreviation': ['eq']
        }


class LocationFilter(FilterSet):
    """Location Graphql Filter"""
    class Meta:
        """Location Graphql Query output"""
        model = LocationModel
        fields = {
            'street_address': ['eq', 'ilike'],
            'city': ['eq', 'ilike'],
            'postal_code': ['eq', 'ilike']
        }



class FilterConnectionField(FilterableConnectionField):
    """ Consolidate the filters"""
    filters = {
        CountryModel: CountryFilter(),
        StateProvinceModel: StateProvinceFilter(),
        LocationModel: LocationFilter()
    }