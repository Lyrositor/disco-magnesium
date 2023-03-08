COPOTYPES = {"apocalypse_cop", "art_cop", "boring_cop", "lawbringer", "sorry_cop", "superstar_cop"}
POLITICALS = {"communist", "moralist", "revacholian_nationhood", "ultraliberal"}

THC_COOKING = "cooking"
THC_FIXED = "fixed"
THC_PRESENT = "present"
THC_UNKNOWN = "unknown"

ItemGroups = {}
ItemTypes = {}
State = {
    money = 0,
    day = 1,
    time = 8,
    damage_health = 0,
    damage_morale = 0,
    is_kim_here = false,
    is_kim_wearing_piss_jacket = false,
    is_cuno_in_party = false,
    is_outside = false,
    is_raining = false,
    is_snowing = false,
    is_hardcore = false,
    has_beaten_hardcore = false,
    items = {},
    equipped = {},
    thoughts = {},
}
Variable = {}

function AddCunoToParty()
    _DebugLog("Adding Cuno to party")
    State.is_cuno_in_party = true
end

function AddGraphito()
    _DebugLog("Adding graphito")
end

function Afterthought(orb_name)
    _DebugLog("Scheduling '" .. orb_name .. "' afterthought")
end

function ApplyCharacterScheduleConditions(schedule_name)
    _DebugLog("Applying character schedule '" .. schedule_name .. "'")
end

function AuthoritySpotlightOff()
    _DebugLog("Turning off Authority spotlight")
end

function AuthoritySpotlightOn()
    _DebugLog("Turning on Authority spotlight")
end

function CancelTask(var_name)
    _DebugLog("Cancelling task '" .. var_name .. "'")
    _SetVariable(var_name, true)
end

function CheckEquipped(item_name)
    local equipped = State.equipped.__contains__(item_name)
    _DebugLog("Checking if '" .. item_name .. "' is equipped: " .. tostring(equipped))
    return equipped
end

function CheckEquippedGroup(group)
    local equipped = _ContainsGroupItem(State.equipped, group)
    _DebugLog("Checking if '" .. group .. "' group is equipped: " .. tostring(equipped))
    return equipped
end

function CheckHeldRightGroup(group)
    -- Assume the held (right) group items can only ever be equipped into the held (right)
    return CheckEquippedGroup(group)
end

function CheckItem(item_name)
    local owned = State.items.__contains__(item_name)
    _DebugLog("Checking if '" .. item_name .. "' is owned: " .. tostring(owned))
    return owned
end

function CheckItemGroup(group)
    local owned = _ContainsGroupItem(State.items, group)
    _DebugLog("Checking if '" .. group .. "' group is owned: " .. tostring(owned))
    return owned
end

function ClearAllInputLocks()
    _DebugLog("Clearing all input locks")
end

function CloseTequilaDoor()
    _DebugLog("Closing door to Harry's room")
end

function Continue()
    -- Do nothing
end

function DamageEndurance(damage)
    _DebugLog("Dealing " .. damage .. " health damage")
    State.damage_health = State.damage_health + damage
end

function DamageEnduranceWithNewspaper(damage, newspaper)
    DamageEndurance(damage)
    _DebugLog("Showing newspaper '" .. newspaper .. "'")
end

function DamageVolition(damage)
    _DebugLog("Dealing " .. damage .. " morale damage")
    State.damage_morale = State.damage_morale + damage
end

function DayCount()
    _DebugLog("Checking current day: " .. State.day)
    return State.day
end

function DestroyObject(object)
    _DebugLog("Destroying object '" .. object .. "'")
end

function EndDayShack()
    _DebugLog("Ending day at the coastal shack")
end

function EndDayWhirling()
    _DebugLog("Ending day at the Whirling-in-Rags")
end

function EndTribunal()
    _DebugLog("Ending tribunal")
end

function FinishTask(var_name)
    _DebugLog("Finishing task '" .. var_name .. "'")
    _SetVariable(var_name, true)
end

function FlagNotSet(variable_name)
    return not FlagSet(variable_name)
end

function FlagSet(variable_name)
    local flag_set = Variable[variable_name] == true
    _DebugLog("Checking flag '" .. variable_name .. "': " .. tostring(flag_set))
    return flag_set
end

function GainItem(item_name)
    _DebugLog("Gaining item '" .. item_name .. "'")
    State.items.add(item_name)
end

function GainMoneyAlways(amount)
    _DebugLog("Gaining " .. amount .." money")
    State.money = State.money + amount
end

function GainMoneyOnce(amount)
    GainMoneyAlways(amount)
end

function GainTask(var_name)
    _DebugLog("Gaining task '" .. var_name .. "'")
    _SetVariable(var_name, true)
end

function GainThought(thought_name)
    _DebugLog("Gaining thought '" .. thought_name .. "'")
    State.thoughts[thought_name] = THC_PRESENT
end

function GoTo(area_id)
    _DebugLog("Going to area '" .. area_id .. "'")
end

function GoToDestination(area_id, destination_id)
    _DebugLog("Going to area '" .. area_id .. "' with destination '" .. destination_id .. "'")
end

function GraffitoAlight()
    _DebugLog("Setting graffito alight")
end

function GraffitoExtinguish()
    _DebugLog("Extinguishing graffito")
end

function HasDoorDialogue()
    _DebugLog("Checking if door has dialogue (stub)")
    return false
end

function HasEnduranceDamage()
    local has_damage = State.damage_health > 0
    _DebugLog("Checking if health is damaged: " .. tostring(has_damage))
    return has_damage
end

function HasHat()
    local wearing_item = _WearsItemOfType("hat")
    _DebugLog("Checking if wearing a hat: " .. tostring(wearing_item))
    return wearing_item
end

function HasJacket()
    local wearing_item = _WearsItemOfType("jacket")
    _DebugLog("Checking if wearing a jacket: " .. tostring(wearing_item))
    return wearing_item
end

function HasNecktie()
    local wearing_item = _WearsItemOfType("neck")
    _DebugLog("Checking if wearing a neck item: " .. tostring(wearing_item))
    return wearing_item
end

function HasPants()
    local wearing_item = _WearsItemOfType("pants")
    _DebugLog("Checking if wearing pants: " .. tostring(wearing_item))
    return wearing_item
end

function HasPawnablesInInventory()
    _DebugLog("Checking if there are pawnables in the inventory (stub)")
    return true
end

function HasShirt()
    local wearing_item = _WearsItemOfType("shirt")
    _DebugLog("Checking if wearing shirt: " .. tostring(wearing_item))
    return wearing_item
end

function HasShoes()
    local wearing_item = _WearsItemOfType("shoes")
    _DebugLog("Checking if wearing shoes: " .. tostring(wearing_item))
    return wearing_item
end

function HasVolitionDamage()
    local has_damage = State.damage_morale > 0
    _DebugLog("Checking if morale is damaged: " .. tostring(has_damage))
    return has_damage
end

function HealAllEndurance()
    _DebugLog("Healing all health damage")
    State.damage_health = 0
end

function HealAllVolition()
    _DebugLog("Healing all morale damage")
    State.damage_morale = 0
end

function HealEndurance(health)
    _DebugLog("Healing " .. health .. " health damage")
    State.damage_health = State.damage_health - health
    if State.damage_health < 0 then
        State.damage_health = 0
    end
end

function HealVolition(health)
    _DebugLog("Healing " .. health .. " morale damage")
    State.damage_morale = State.damage_morale - health
    if State.damage_morale < 0 then
        State.damage_morale = 0
    end
end

function HideDialogueImage(image)
    _DebugLog("Hiding image '" .. image .. "'")
end

function HideVisCal(name)
    _DebugLog("Hiding visual calculus scene '" .. name .. "'")
end

function HideVisCalAfterConversation(name)
    HideVisCal(name)
end

function HourCount()
    _DebugLog("Checking current hour: " .. State.time)
    return State.time
end

function IsAfternoon()
    local is_afternoon = State.time >= 12 and State.time < 18
    _DebugLog("Checking if it is afternoon: " .. tostring(is_afternoon))
    return is_afternoon
end

function IsCunoInParty()
    _DebugLog("Checking if Cuno is in the party: " .. tostring(State.is_cuno_in_party))
    return State.is_cuno_in_party
end

function IsDayFrom(day)
    local is_from_day = State.day >= day
    _DebugLog("Checking if current day is on or after day " .. day .. ": " .. tostring(is_from_day))
    return is_from_day
end

function IsDaytime()
    local is_daytime = State.time >= 8 and State.time < 20
    _DebugLog("Checking if it is daytime: " .. tostring(is_daytime))
    return is_daytime
end

function IsDayUntil(day)
    local is_until_day = State.day <= day
    _DebugLog("Checking if current day is on or before day " .. day .. ": " .. tostring(is_until_day))
    return is_until_day
end

function IsDusk()
    local is_dusk = State.time >= 18 and State.time < 20
    _DebugLog("Checking if it is dusk: " .. tostring(is_dusk))
    return is_dusk
end

function IsEvening()
    local is_evening = State.time >= 20
    _DebugLog("Checking if it is evening: " .. tostring(is_evening))
    return is_evening
end

function IsExterior()
    _DebugLog("Checking if outside: " .. tostring(State.is_outside))
    return State.is_outside
end

function IsHighestCopotype(copotype)
    local is_highest = _IsHighestReputation(copotype, COPOTYPES)
    _DebugLog("Checking if '" .. copotype .. "' is highest copotype: " .. tostring(is_highest))
    return is_highest
end

function IsHighestPolitical(political)
    local is_highest = _IsHighestReputation(political, POLITICALS)
    _DebugLog("Checking if '" .. political .. "' is highest political: " .. tostring(is_highest))
    return is_highest
end

function IsHourBetween(first, second)
    local is_hour_between = false
    if (first < second) then
        is_hour_between = State.time >= first and State.time <= second
    else
        is_hour_between = State.time >= first or State.time <= second
    end
    _DebugLog("Checking if '" .. State.time .. "' is between " .. first .. " and " .. second .. ": " .. tostring(is_hour_between))
    return is_hour_between
end

function IsKimHere()
    _DebugLog("Checking if Kim is here: " .. tostring(State.is_kim_here))
    return State.is_kim_here
end

function IsKimInParty()
    return IsKimHere()
end

function IsKimWearingPissJacket()
    _DebugLog("Checking if Kim is wearing the piss jacket: " .. tostring(State.is_kim_wearing_piss_jacket))
    return State.is_kim_wearing_piss_jacket
end

function IsHardcoreModeActive()
    _DebugLog("Checking if hardcore mode is active: " .. tostring(State.is_hardcore))
    return State.is_hardcore
end

function IsMorning()
    local is_morning = State.time >= 8 and State.time < 12
    _DebugLog("Checking if it is morning: " .. tostring(is_morning))
    return is_morning
end

function IsNight()
    local is_night = State.time >= 0 and State.time <= 2
    _DebugLog("Checking if it is night: " .. tostring(is_night))
    return is_night
end

function IsNighttime()
    local is_nighttime = State.time <= 2 or State.time >= 20
    _DebugLog("Checking if it is nighttime: " .. tostring(is_nighttime))
    return is_nighttime
end

function IsNoon()
    local is_noon = State.time == 12
    _DebugLog("Checking if it is noon: " .. tostring(is_noon))
    return is_noon
end

function IsRaining()
    _DebugLog("Checking if it is raining: " .. tostring(State.is_raining))
    return State.is_raining
end

function IsSnowing()
    _DebugLog("Checking if it is snowing: " .. tostring(State.is_snowing))
    return State.is_snowing
end

function IsTaskActive(task_name)
    _DebugLog("Checking if task '" .. task_name .. "' is active")
    return Variable[task_name] == true
end

function IsTHCCooking(name)
    return IsTHCPresent(name)
    -- return _CheckTHCStatus(name) == THC_COOKING
end

function IsTHCCookingOrFixed(name)
    return IsTHCCooking(name) or IsTHCFixed(name)
end

function IsTHCFixed(name)
    return IsTHCPresent(name)
    -- return _CheckTHCStatus(name) == THC_FIXED
end

function IsTHCPresent(name)
    return _CheckTHCStatus(name) == THC_PRESENT
end

function LetterSleep()
    _DebugLog("Putting Harry to sleep after reading letter")
end

function LoseItem(item_name)
    _DebugLog("Losing item '" .. item_name .. "'")
    if State.items.__contains__(item_name) then
        State.items.remove(item_name)
    end
end

function LoseMoneyAlways(amount)
    _DebugLog("Losing " .. amount .." money")
    State.money = State.money - amount
end

function LoseMoneyOnce(amount)
    LoseMoneyAlways(amount)
end

function MoneyAmount()
    return State.money
end

function Mullenize()
    _DebugLog("Mullenizing")
end

function NewspaperEndgame(type, title, opener)
    _DebugLog("Showing newspaper clipping '" .. type .. "' (title: '" .. title .. "', opener: '" .. opener .. "'")
end

function NextMorningTime()
    return 8  -- Is this correct?
end

function NightyNightKitsuragiShack()
    _DebugLog("Saying good night to Kim at the shack")
    State.is_kim_here = false
end

function Obsession(orb_name)
    _DebugLog("Scheduling '" .. orb_name .. "' obsession")
end

function OpenBookstoreCurtains()
    _DebugLog("Opening bookstore curtains")
end

function PassTime()
    _DebugLog("Waiting 15 minutes (stub)")
end

function PlaySoundGroup(group, variation, volume)
    _DebugLog("Playing sound group (group: '" .. group .. "', variation: '" .. variation .. "', volume: " .. volume)
end

function PosseEndgame()
    _DebugLog("Ending the game with the posse")
end

function PrimeSpecialEndButton()
    _DebugLog("Priming the special end button")
end

function RemoveAndHideKitsuragi()
    _DebugLog("Removing Kim from party")
    State.is_kim_here = false
end

function RemoveAndHideKitsuragiUntilMorning()
    RemoveAndHideKitsuragi()
end

function RemoveCunoFromParty()
    _DebugLog("Removing Cuno from party")
    State.is_cuno_in_party = false
end

function RemoveCunoWaitAtFort()
    RemoveCunoFromParty()
end

function RemoveKitsuragiWaitAtChurch()
    RemoveAndHideKitsuragi()
end

function RemoveKitsuragiWaitAtLair()
    RemoveAndHideKitsuragi()
end

function RemoveKitsuragiWaitAtTent()
    RemoveAndHideKitsuragi()
end

function RemoveWhiteCheck(value)
    _DebugLog("Removing white check for '" .. tostring(value) .. "' (stub)")
end

function Reputation(variable, value)
    _DebugLog("Adjusting '" .. variable .. "' reputation by " .. value)
    local variable_name = "reputation." .. variable
    _SetVariable(variable_name, Variable[variable_name] + value)
end

function ReputationGrows(variable)
    Reputation(variable, 1)
end

function ReputationLowers(variable)
    Reputation(variable, -1)
end

function ResetCamera()
    _DebugLog("Resetting camera")
end

function ResetCameraMarker()
    _DebugLog("Resetting camera marker")
end

function ReturnKitsuragi()
    _DebugLog("Returning Kim to party")
    State.is_kim_here = true
end

function RotationLockOff()
    _DebugLog("Locking off rotation")
end

function SellItemGroup(group)
    _DebugLog("Selling group '" .. group .. "' (stub)")
end

function SellItemGroupWithModifier(group, modifier)
    _DebugLog("Selling group '" .. group .. "' with modifier " .. modifier .. " (stub)")
end

function SetAreaState(area_name, state_name)
    _DebugLog("Setting area '" .. area_name .. "' to '" .. state_name .. "'")
end

function SetFlag(variable_name)
    if variable_name ~= nil then
        _DebugLog("Setting flag '" .. variable_name .. "'")
        _SetVariable(variable_name, true)
    end
end

function SeaFortSleepDream()
    _DebugLog("Going to sleep with dream at the sea fort")
end

function SeaFortSleepNoDream()
    _DebugLog("Going to sleep without dream at the sea fort")
end

function SetTriggerAnimation(target, animation)
    _DebugLog("Setting trigger animation '" .. animation .. "' for '" .. target .. "'")
end

function SetVariableValue(variable_name, new_value)
    _DebugLog("Setting variable '" .. variable_name .. "' to '" .. tostring(new_value) .. "'")
    _SetVariable(variable_name, new_value)
end

function SkipToDebriefLocation()
    _DebugLog("Skipping to debrief location")
end

function ShackBedWasUsed()
    _DebugLog("The coast shack bed was used")
end

function ShowDialogueImage(image_name)
    _DebugLog("Showing dialogue image '" .. image_name .. "'")
end

function ShowInventoryForPawning()
    _DebugLog("Showing inventory for pawning")
end

function ShowVisCal(name)
    _DebugLog("Showing Visual Calculus scene .. '" .. name .. "'")
end

function SubstanceUsedMore(substance)
    local used_more = Variable["stats.uses_" .. substance] > 1
    _DebugLog("Checking if substance '" .. substance .. "' was used more: " .. tostring(used_more))
    return used_more
end

function SubstanceUsedOnce(substance)
    local used_once = Variable["stats.uses_" .. substance] >= 1
    _DebugLog("Checking if substance '" .. substance .. "' was used at least once: " .. tostring(used_once))
    return used_once
end

function TeleportTo(scene_name, location_marker)
    _DebugLog("Teleporting to scene '" .. scene_name .. "' at location marker '" .. location_marker .. "'")
end

function TeleportToAndFocusCamera(scene_name, location_marker, camera_focus)
    _DebugLog("Teleporting to scene '" .. scene_name .. "' at location marker '" .. location_marker .. "' with camera focus '" .. camera_focus .. "'")
end

function TequilaExpressionStopped()
    _DebugLog("Stopping the Expression")
end

function TequilaFascist()
    _DebugLog("Harry is now a fascist")
end

function TequilaPutOnBodysuit()
    _DebugLog("Harry has put on the leotard")
end

function TequilaRemoveBodysuit()
    _DebugLog("Harry has removed the leotard")
end

function TequilaShaved()
    _DebugLog("Harry has shaved")
end

function TequilaUnobscured()
    _DebugLog("Harry is no longer obscured")
end

function TequilaWakeUp()
    _DebugLog("Harry has woken up")
end

function TimeSinceKimWentToSleep()
    _DebugLog("Checking how much time has passed since Kim went to sleep (stub)")
    return 15
end

function TotalHourCount()
    local totalHourCount = (State.day - 1) * 24 - 8 + State.time
    _DebugLog("Checking total hour count: " .. totalHourCount)
    return totalHourCount
end

function TurnOffCeilingFan()
    _DebugLog("Turning off the ceiling fan")
end

function TurnOffFanLight()
    _DebugLog("Turning off the fan light")
end

function TurnOnFanLight()
    _DebugLog("Turning on the fan light")
end

function UnlockKlaasjeDoor()
end

function UseSubstanceInHand(hand)
    _DebugLog("Use substance in " .. hand .. " hand (stub)")
end

function WakeFromDream()
    _DebugLog("Waking from dream")
end

function WakeFromDreamSeaFort()
    _DebugLog("Waking from sea fort dream")
end

function WasGameBeatenInHardcoreMode()
    _DebugLog("Checking if game was beaten in hardcore mode: " .. tostring(State.has_beaten_hardcore))
    return State.has_beaten_hardcore
end

function WeirdClothing()
    _DebugLog("Checking if wearing weird clothing (stub)")
    return true
end

function WhirlingBedWasUsed()
    _DebugLog("The Whirling-in-Rags bed was used")
end

function WhirlingEngineStart()
    _DebugLog("Starting engine noise at the Whirling-in-Rags")
end

function WhirlingEngineStop()
    _DebugLog("Stopping engine noise at the Whirling-in-Rags")
end

function XPMajorSetBool(var)
    XPSetBool(var, "major")
end

function XPMinorSetBool(var)
    XPSetBool(var, "minor")
end

function XPPicoSetBool(var)
    XPSetBool(var, "pico")
end

function XPSetBool(var, amount)
    _DebugLog("Setting XP for '" .. var .. "' (" .. amount .. ")")
    _SetVariable(var, true)
end

function XPStandardSetBool(var)
    XPSetBool(var, "standard")
end

function XPTinySetBool(var)
    XPSetBool(var, "tiny")
end

function once(num)
    _DebugLog("Applying " .. num .. " once (stub)")
    return num
end

function _CheckTHCStatus(name)
    local status = THC_UNKNOWN
    if python.as_attrgetter(State.thoughts)['__contains__'](name) then
        status = State.thoughts[name]
    end
    _DebugLog("Checking '" .. name .. "' thought cabinet status: " .. status)
    return status
end

function _ContainsGroupItem(iterable, group)
    for item in python.iter(iterable) do
        if ItemGroups[item] == group then
            return true
        end
    end
    return false
end

function _DebugLog(string)
    Logger.debug(string)
end

function _IsHighestReputation(reputation, options)
    return _IsHighest("reputation.", reputation, options)
end

function _IsHighest(prefix, reputation, options)
    local var_name = prefix .. reputation
    local to_beat = Variable[var_name]
    for _, option in ipairs(options) do
        if option ~= var_name and Variable[prefix .. option] > to_beat then
            return false
        end
    end
    return to_beat > 0
end

function _SetVariable(name, value)
    -- Mirror any variable changes back to the actual variable object
    Variable[name] = value
    State.variables[name] = value
end

function _WearsItemOfType(type)
    for item in python.iter(State.equipped) do
        if ItemTypes[item] == type then
            return true
        end
    end
    return false
end
