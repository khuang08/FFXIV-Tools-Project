# FFXIV-Tools-Project

A simple tool to retrieve a list of equippable items in FFXIV.

## Getting Started

To use the Python script, you can setup a virtual environment and install the necessary modules or install them directly on your machine.  

You will also need Item.csv in the same folder as the location where you are running the script.

## Installation

- Download ffxiv_item_search.py and Item.csv to any desired location in the same folder
- Run the following command **"pip install pandas"**

    Note: The ClassJobCategory.json file is not required for the script. It only contains the IDs for the jobs used in Item.csv

## Usage

Available Jobs:
Combat: ACN, ARC, AST, BLM, BRD, CNJ, DRG, DRK, GLA, LNC, MNK, MRD, NIN, PLD, ROG, SCH, SMN, THM, WAR, WHM
Categories: DoW (Disciples of War), DoM (Disciples of Magic)

Crafters/Gatherers:
Available Jobs: ALC, ARM, BSM, BTN, CRP, CUL, FSH, GSM, LTW, MIN, WVR

Available Categories: DoH (Disciples of Hand), DoL (Disciples of Land)

Enter one or more job abbreviations (comma separated) or 'ALL': MIN, BTN

Enter level(s) in one of these formats:
- Single level: 50
- Multiple levels: 50, 52, 55
- Level ranges: 50-54 (inclusive)
- Mixed: 50, 52-54, 56, 60-62

Enter level(s) (1-100): 81

Results (4 items found):
| #     | Name                      | Level | Rarity | Job |
|-------|---------------------------|-------|--------|-----|
|       |                           |       |        |     |
| 35329 | High Durium Hatchet       | 81    | White  | BTN |
| 35340 | High Durium Garden Scythe | 81    | White  | BTN |
| 35328 | High Durium Pickaxe       | 81    | White  | MIN |
| 35339 | High Durium Sledgehammer  | 81    | White  | MIN |

Print in Artisan format? (y/n): y

Normal (White) items:
1x High Durium Hatchet  
1x High Durium Garden Scythe  
1x High Durium Pickaxe  
1x High Durium Sledgehammer  
Press any key to continue . . .  

In this example, we entered our classes as **MIN, BTN**, and our levels as **81**.

## Additional Documentation and Acknowledgments

This project includes the following files sourced from external repositories:

   - Item.csv  
   - ClassJobCategory.json

Original files are from xivapi/ffxiv-datamining, © XIVAPI. These files are used under the assumption that they are licensed under the MIT License, if you are the rights holder and believe this is incorrect, please contact us.
