from enum import Enum

class StartMenuIds(Enum):
    NEW_SUBSCRIPTION = 'new_sub'
    LIST_SUBSCRIPTIONS = 'list_subs'
    EDIT_SUBSCRIPTION = 'edit_sub'

class NewSubIds(Enum):
    RENT_APARTMENT = 'rent_apartment'
    BUY_APARTMENT = 'buy_apartment'
    GOODS = 'goods'