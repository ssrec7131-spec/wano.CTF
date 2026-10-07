"""Consolidated official Round 1 challenges for WANO CTF (including Beginner, Intermediate, and Advanced/Expert quests)."""

from app.seeds.challenges_data_part1 import CHALLENGES_PART_1
from app.seeds.challenges_data_part2 import CHALLENGES_PART_2
from app.seeds.challenges_data_part3 import CHALLENGES_PART_3
from app.seeds.challenges_data_part4 import CHALLENGES_PART_4
from app.seeds.challenges_data_part5 import CHALLENGES_PART_5
from app.seeds.challenges_data_part6 import CHALLENGES_PART_6

ALL_ROUND_1_CHALLENGES = [
    *CHALLENGES_PART_1,
    *CHALLENGES_PART_2,
    *CHALLENGES_PART_3,
    *CHALLENGES_PART_4,
    *CHALLENGES_PART_5,
    *CHALLENGES_PART_6,
]

assert len(ALL_ROUND_1_CHALLENGES) == 42, f"Expected 42 challenges, got {len(ALL_ROUND_1_CHALLENGES)}"
