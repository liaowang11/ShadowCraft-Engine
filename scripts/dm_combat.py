# Simple test program to debug + play with assassination models.
from os import path
import sys
sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

from shadowcraft.calcs.rogue.darkmantle import DarkmantleCalculator
from shadowcraft.calcs.rogue.darkmantle import settings

from shadowcraft.objects import buffs
from shadowcraft.objects import race
from shadowcraft.objects import stats
from shadowcraft.objects import procs
from shadowcraft.objects import talents
from shadowcraft.objects import glyphs

from shadowcraft.core import i18n

from time import clock

# Set up language. Use 'en_US', 'es_ES', 'fr' for specific languages.
test_language = 'local'
i18n.set_language(test_language)

start = clock()

# Set up level/class/race
test_level = 90
test_race = race.Race('pandaren')
test_class = 'rogue'

# Set up buffs.
test_buffs = buffs.Buffs(
        'short_term_haste_buff',
        'stat_multiplier_buff',
        'crit_chance_buff',
        'mastery_buff',
        'melee_haste_buff',
        'attack_power_buff',
        'spell_haste_buff',
        'armor_debuff',
        'physical_vulnerability_debuff',
        'spell_damage_debuff',
        'agi_flask_mop',
        'food_300_agi'
    )

# Set up weapons.
test_mh = stats.Weapon(18846.0, 2.6, 'axe', 'dancing_steel')
#test_oh = stats.Weapon(18846.0, 2.6, 'axe', 'dancing_steel')
test_oh = stats.Weapon(13047.0, 1.8, 'dagger', 'dancing_steel')

# Set up procs.
test_procs = procs.ProcsList(('heroic_war_assurance_of_consequence', 2), ('heroic_war_haromms_talisman', 2), 'legendary_capacitive_meta', 'fury_of_xuen')

# Set up gear buffs.
test_gear_buffs = stats.GearBuffs('rogue_t16_2pc', 'rogue_t16_4pc', 'leather_specialization', 'virmens_bite', 'virmens_bite_prepot')

# Set up a calcs object..
test_stats = stats.Stats(test_mh, test_oh, test_procs, test_gear_buffs,
                         str=80,
                         agi=27882,
                         stam=35869,
                         crit=3851,
                         haste=18871,
                         mastery=8574)

# Initialize talents..
test_talents = talents.Talents('332213', test_class, test_level)

# Set up glyphs.
glyph_list = ['recuperate']
test_glyphs = glyphs.Glyphs(test_class, *glyph_list)

# Set up settings.
test_cycle = settings.CombatCycle(stack_cds=True, weapon_swap=False)
test_settings = settings.Settings(test_cycle, response_time=.5, latency=.03, merge_damage=True)

# Build a DPS object.
calculator = DarkmantleCalculator(test_stats, test_talents, test_glyphs, test_buffs, test_race, test_settings, test_level)

# Compute DPS Breakdown.
dps_breakdown = calculator.get_dps_breakdown()
total_dps = sum(entry[1] for entry in dps_breakdown.items())

# Compute EP values.
ep_values = calculator.get_ep(baseline_dps=total_dps)
#mh_enchants_and_dps_ep_values, oh_enchants_and_dps_ep_values = calculator.get_weapon_ep(dps=True, enchants=True)

def max_length(dict_list):
    max_len = 0
    for i in dict_list:
        dict_values = i.items()
        if max_len < max(len(entry[0]) for entry in dict_values):
            max_len = max(len(entry[0]) for entry in dict_values)

    return max_len

def pretty_print(dict_list, total_sum = 1., show_percent=False):
    max_len = max_length(dict_list)

    for i in dict_list:
        dict_values = i.items()
        dict_values.sort(key=lambda entry: entry[1], reverse=True)
        for value in dict_values:
            #print value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1])
            if show_percent and ("{0:.2f}".format(float(value[1])/total_dps)) != '0.00':
                print value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1]) + ' ('+str( "{0:.2f}".format(100*float(value[1])/total_sum) )+'%)'
            else:
                print value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1])
        print '-' * (max_len + 15)

dicts_for_pretty_print = [
    ep_values
]
pretty_print(dicts_for_pretty_print)
pretty_print([dps_breakdown], total_sum=total_dps, show_percent=True)
print ' ' * (max_length(dicts_for_pretty_print) + 1), total_dps, _("total damage per second.")
print "Request time: %s sec" % (clock() - start)