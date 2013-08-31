import equipment
from equipment import *
import eqmlload
from eqmlload import *
import eqmlsave
from eqmlsave import *
import eqml
from eqml import *

eqmlList = EQML("test.eqp")
ourEquip = PEquipment()
ourEquip.add_equipment(eqmlList.get_equipment_by_id(3))
ourEquip.add_equipment(eqmlList.get_equipment_by_id(0))
print ourEquip.items
ourEquip.equip_weapon_by_id(0)
print ourEquip.eqpWeapon
ourEquip.equip_weapon_by_id(3)
print ourEquip.eqpWeapon

eqmlList.save_item_list("test2.eqp")
