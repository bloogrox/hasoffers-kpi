from dynamic_preferences import types
from dynamic_preferences.registries import global_preferences_registry


NON_INCENT = 'non_incent'
INCENT = 'incent'

MIN_CR = 'min_cr'
MAX_CR = 'max_cr'
PACC = 'pacc'
CLICKS_IF_ZERO_CONV = 'clicks_if_zero_conv'
CAP_FILL = 'cap_fill'
MIN_CLICKS = 'min_clicks'
STATUS = 'status'


non_incent = types.Section(NON_INCENT, verbose_name='Non Incent')
incent = types.Section(INCENT, verbose_name='Incent')


@global_preferences_registry.register
class Min_CR_NonIncent(types.FloatPreference):
    section = non_incent
    name = MIN_CR
    verbose_name = 'Min CR'
    default = .0


@global_preferences_registry.register
class Max_CR_NonIncent(types.FloatPreference):
    section = non_incent
    name = MAX_CR
    verbose_name = 'Max CR'
    default = .0


@global_preferences_registry.register
class PACC_NonIncent(types.IntegerPreference):
    section = non_incent
    name = PACC
    verbose_name = 'Click Cost Loss'
    default = 0


@global_preferences_registry.register
class Clicks_If_Zero_Conv_NonIncent(types.IntegerPreference):
    section = non_incent
    name = CLICKS_IF_ZERO_CONV
    verbose_name = 'Conversions = 0; Clicks >'
    default = 0


@global_preferences_registry.register
class Cap_Fill_NonIncent(types.FloatPreference):
    section = non_incent
    name = CAP_FILL
    verbose_name = 'Affiliate CAP Fill <'
    default = .0


@global_preferences_registry.register
class Min_Clicks_NonIncent(types.IntegerPreference):
    section = non_incent
    name = MIN_CLICKS
    verbose_name = 'Minimum Clicks'
    default = 100


# INCENT
@global_preferences_registry.register
class Min_CR_Incent(types.FloatPreference):
    section = incent
    name = MIN_CR
    verbose_name = 'Min CR'
    default = .0


@global_preferences_registry.register
class Max_CR_Incent(types.FloatPreference):
    section = incent
    name = MAX_CR
    verbose_name = 'Max CR'
    default = .0


@global_preferences_registry.register
class PACC_Incent(types.IntegerPreference):
    section = incent
    name = PACC
    verbose_name = 'Click Cost Loss'
    default = 0


@global_preferences_registry.register
class Clicks_If_Zero_Conv_Incent(types.IntegerPreference):
    section = incent
    name = CLICKS_IF_ZERO_CONV
    verbose_name = 'Conversions = 0; Clicks >'
    default = 0


@global_preferences_registry.register
class Cap_Fill_Incent(types.FloatPreference):
    section = incent
    name = CAP_FILL
    verbose_name = 'Affiliate CAP Fill <'
    default = .0


@global_preferences_registry.register
class Min_Clicks_Incent(types.IntegerPreference):
    section = incent
    name = MIN_CLICKS
    verbose_name = 'Minimum Clicks'
    default = 100


@global_preferences_registry.register
class Status(types.BooleanPreference):
    name = STATUS
    verbose_name = 'System status'
    default = True
