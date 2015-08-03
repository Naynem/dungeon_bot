#!/usr/bin/env python3
import json
import random
from .util import *
from .modifiers import *


class LevelPerk(object): #LevelPerks always affect only the host that carries them
	name = "Unfinished perk"
	description = "Report this bug"
	requirements = {

	}
	characteristics_change = {}
	stats_change = {}
	abilities_granted = []
	modifiers_granted = []
	tags_granted = []
	priority = 0
	def __init__(self, host):
		self.uid = get_uid()
		self.host = host

	def on_combat_start(self):
		pass

	def on_combat_over(self):
		pass

	def on_item_equipped(self, item):
		pass

	def on_item_unequipped(self, item):
		pass

	def on_consumable_used(self, item):
		pass

	def on_turn(self):
		pass

	def on_round(self):
		pass

	def on_level_up(self):
		pass

	def on_attack(self, ability_info=None):
		pass

	def on_hit(self, ability_info=None):
		pass

	def on_got_hit(self, ability_info=None):
		pass

	def on_attacked(self, ability_info=None):
		pass

	def on_miss(self, ability_info=None):
		pass

	def on_buff(self, ability_info=None):
		pass

	def on_buffed(self, ability_info=None):
		pass

	def on_kill(self, ability_info=None):
		pass

	def on_death(self, ability_info=None):
		pass

	def on_experience_gained(self, ability_info=None):
		pass

	def on_energy_gained(self, amount=None):
		pass

	def on_energy_lost(self, amount=None):
		pass

	def on_health_gained(self, amount=None):
		pass

	def on_health_lost(self, amount=None):
		pass

	def on_loot(self, item_gained):
		pass

	def on_modifier_applied(self, modifier):
		pass

	def on_modifier_lifted(self, modifier):
		pass

class Educated(LevelPerk):
	name = "Educated"
	description = "Get 10 percent additional experience."
	priority = 0
	requirements = {
		"level": 1,
		"has_perks": [],
		"characteristics": {
			"intelligence": 5
		}
	}

	def __init__(self, host):
		LevelPerk.__init__(self, host)

	def on_experience_gained(self, ability_info):
		additional_gain = ability_info.use_info["experience_gained"] * 0.10
		ability_info.use_info["experience_gained"] += additional_gain
		ability_info.description +=  "%s gains %d additional experience due to being educated.\n"%(self.host.name.title(), additional_gain)
		return ability_info

class Flow(LevelPerk):
	name = "Flow"
	description = "Get 50 percent chance to recover 2 energy on kill."
	priority = 0
	requirements = {
		"level": 1,
		"has_perks": [],
		"characteristics": {
			"dexterity": 6
		}
	}

	def on_kill(self, ability_info):
		if ability_info.inhibitor == self.host and random.randint(0,100) < 50:
			ability_info.inhibitor.energy += 2
			ability_info.description += "%s recovers 2 energy!"%(self.host.name.title())
		return ability_info

class Deft(LevelPerk):
	name = "Deft"
	description = "Get a 30 percent chance to recover 1 energy after a miss."
	priority = 0
	requirements = {
		"level": 1,
		"has_perks": [],
		"characteristics": {
			"intelligence": 6,
		}
	}

	def on_miss(self, ability_info):
		if ability_info.use_info["energy_change"] < -1:
			if random.randint(0, 100) < 30:
				ability_info.inhibitor.energy += 1
				ability_info.description += "%s recovers 1 energy!"%(ability_info.inhibitor.name.title())
				return ability_info
		return ability_info

class Sweeper(LevelPerk):
	name = "Sweeper"
	description = "Get an accuracy bonus when surrounded by 4 or more enemies"
	priority = 0
	requirements = {
		"level": 1,
		"has_perks": [],
		"characteristics": {
			"strength": 6,
		}
	}

	def on_turn(self):
		msg = ""
		if self.host.event:
			combat_event = self.host.event
			if len([c for c in combat_event.turn_qeue if c.__class__.__name__ != "Enemy"])>=4:
				modifier = get_modifier_by_name("bonus", self, self.host, {"duration":1, "stats_change":{"accuracy": "4d4"}})
				msg = "%s gains a 4d4 accuracy bonus due to being surrounded by enemies.\n Hard to miss when they are all around you, huh!\n"%(self.host.name.title())
				self.host.add_modifier(modifier)
				modifier.apply()
		return msg

level_perks_listing = {
	"Educated":Educated,
	"Flow": Flow,
	"Deft": Deft,
	"Sweeper": Sweeper,
}
