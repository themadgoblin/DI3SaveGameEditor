# Save Game Modifying Guides
This guide explains how to unlock specific things in the Disney Infinity games once you decompress the save files.
Obviously, modifying save files can lead to corruption of your save data, so make sure to back up your save files before proceeding.

## Unlocking Feats And Rewards (DI 2.0 and 3.0)
You can unlock feats by modifying the `P0` file in your savegame:
Once decompressed, open the file and towards the end of it there's a section called `FeatsManager`.

This section contans a list of all feats in the following format:
```
FeatId<ID> = <ID>
FeatUnlocked<ID> = <0 or 1>
<some counters or sub-counters>
```
Where:
* `<ID>` is just a number id of the feat - Mapping the id to the actual feat can be tricky and require trial and error and using common sense.
* `<0 or 1>` indicates whether the feat is locked (0) or unlocked (1).
* `<some counters or sub-counters>` - These are usually some counters that track progress towards the feat, for example a feat that requires you to kill a specific amount od enemies will have a field below it `DeathCount<ID>` which tracks how many enemies you've killed towards that feat.

To unlock a feat, set the required counter correctly and set the `FeatUnlocked<ID>` field to `1`. But this is not enough.

`FeatsManager` also tracks the rewards you've earned from feats in the following format:
```
RewardId<ID> = <ID>
Rewarded<ID> = <0 or 1>
Purchased<ID> = <0 or 1>
```
Where:
* `<ID>` is the id of the reward - The same as the feat id,
* `<0 or 1>` indicates whether the reward has been rewarded (0 or 1) or purchased (0 or 1).

To get the reward for a feat, set both `Rewarded<ID>` and `Purchased<ID>` to `1`.
Note that some feats don't actually give rewards, so you may not find a reward section for some feats. And even if you did find it, setting both fields to `1` may not have any effect.

After unlocking a feat this way, make sure to then search for the values `ACH_FEATS_COMPLETE` and `NON_META_FEATS_COMPLETE` in the file and increment their values by `1` to reflect the newly unlocked feat.
These values track the number of feat you have completed towards the feats that are unlocked by completing other feats. I'm not sure what is the difference between them exactly, so I recommend incrementing both of them.

## Unlocking Concept Arts (DI 2.0 and 3.0)
This is actually the same as unlocking the rewards for feats as most if not all of them are unlocked by completing feats. You will just have to figure out which feat unlocks which concept art.

## Earning Gold Medals in Challenges (DI 2.0 and 3.0)
To earn a gold medal in a challenge you will need to modify the save game for the challenge playset (see README.md for more info on which file corresponds to which playset).
Once decompressed, open the file and search for the string "chal". All challenges are store in structures that has a name containing "chal".

I will explain how to set a gold medal for a specific challenge using a concrete example as I didn't map all fields exactly and most of them are irrelevnat.

Let's look at the following challenge and explain the different fields:
```
GOG_Knowhere_Chal_CombatTargets1 =
		{
			CON_UID = 1395382312
			COUNT = 1
			STATE = 1149
			MIS_COMP_DELTA = 0
			INIT_PRIORITY = 1
			FORCE_LOCK = 0
			FORCE_ACTIVATED = 0
			GS_TYPE = 1
			ICON_NAME = ""
			HIGHEST_DIFFICULTY_COMPLETED = 192
			BEST_RESULT = 1440
			BEST_RESULT_2P = 0
			MG_BACK = -1
			MG = -1
			LOC_BACK = -1
			LOC = -1
		}
```

* `COUNT` - Number of times the challenge has been completed.
* `STATE` - Current state of the challenge. I noticed 2 values here:
    - `1149` - Challenge unlocked and available to play.
    - `1147` - Challenge is locked.
* `HIGHEST_DIFFICULTY_COMPLETED` - This is actually the medal you've earned in the challenge. The values are:
    - `0` - No medal.
    - `64` - Bronze medal.
    - `128` - Silver medal.
    - `192` - Gold medal.
* `BEST_RESULT` - Your best score/time in the challenge.
    - For time results, the result is scored in milliseconds. So for example if you want to set a time of 1 minute (60 seconds), you will set this field to `60000` (60 * 1000). And 2min 19.70s = 139700.

* NOTE: DI3.0 only has 1147 STATE value for all challenges, probably since challenges are always unlocked and availbale to play providing you get to their planet.
To earn a gold medal in a challenge set the fields accordingly. Again you will need to map exactly which challenge in the file corresponds to which challenge in the game and what are the required times/scores for each medal.

**Important notes:**
* I recommend not unlocking the challenges using the `STATE` field and instead first unlocking all challenges normally. This is really easy to do.
* You **DON'T NEED TO MODIFY THE FEATS FOR THE CHALLENGES MEDALS.** - Once you unlock the gold medals using this method and load the playset, the game will automatically unlock all medal related feats for you.




