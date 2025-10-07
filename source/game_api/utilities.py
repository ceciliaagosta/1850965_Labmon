# Utility functions
from datetime import datetime, timezone
import config
import random

# Rarity weight function - returns a weights for rarity levels 1 to 5 based on time passed since last encounter
def rarity_weights(last_encounter_time):
    if last_encounter_time is None:
        return [1, 0, 0, 0, 0]  # if first encounter ever, only rarity 1
    
    time_diff = (datetime.now(timezone.utc) - last_encounter_time).total_seconds() / 60  # in minutes

    if time_diff < 30:
        return []
    
    # Define base weights for rarities 1 to 5
    base = config.BASE_WEIGHTS.copy()

    # Increase weights for higher rarities based on time passed
    # Every half hour passed increases chance of rare monsters slightly
    factor = min(time_diff / 30, 3)  # cap effect at 3 hours

    # Shift weight toward rare monsters
    adjusted = [
        max(1, base[0] - factor * 5),
        max(1, base[1] - factor * 2),
        base[2] + factor * 2,
        base[3] + factor * 3,
        base[4] + factor * 4
    ]

    # Normalize
    total = sum(adjusted)
    return [w / total for w in adjusted]

# Rarity selection function
def choose_rarity(weights):
    if weights == []:
        return 0  # if weights list is empty, return rarity 0 (no encounter)
    return random.choices(config.RARITY_LEVELS, weights=weights, k=1)[0]

# Monster selection function
def select_monster(encounter_pool):
    return random.choice(encounter_pool)[0]  # return the first element which is the monster_id

# Catch attempt function
def attempt_catch(catch_rate, item_effect):
    adjusted_rate = catch_rate * item_effect
    return random.random() < adjusted_rate