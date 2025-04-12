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

Here is a sample run of our script:

Available Jobs:  
Combat: GLA, PLD, MRD, WAR, DRK, LNC, DRG, ROG, NIN, MNK, ARC, BRD, THM, BLM, ACN, SMN, CNJ, WHM, SCH, AST  
Crafters: CRP, BSM, ARM, GSM, LTW, WVR, ALC, CUL  
Gatherers: MIN, BTN, FSH

Enter one or more job abbreviations (comma separated) or 'ALL': **MIN, BTN**

Enter level(s) in one of these formats:
- Single level: 50
- Multiple levels: 50, 52, 55
- Level ranges: 50-54 (inclusive)
- Mixed: 50, 52-54, 56, 60-62

Enter level(s) (1-100): **71, 72-74**

Results (23 items found):
| #      | Name                                               | Level | Rarity   | Job  |
|--------|----------------------------------------------------|-------|----------|------|
| 27086  | Deepgold Hatchet                                   | 71    | White    | BTN  |
| 27097  | Deepgold Scythe                                    | 71    | White    | BTN  |
| 27107  | Bluespirit Hatchet                                 | 74    | White    | BTN  |
| 27118  | Bluespirit Scythe                                  | 74    | White    | BTN  |
| 27166  | Brightlinen Turban of Gathering                   | 71    | White    | DoL  |
| 27167  | Brightlinen Coat of Gathering                     | 71    | White    | DoL  |
| 27168  | Smilodonskin Gloves of Gathering                  | 71    | White    | DoL  |
| 27169  | Brightlinen Bottoms of Gathering                  | 71    | White    | DoL  |
| 27170  | Smilodonskin Shoes of Gathering                   | 71    | White    | DoL  |
| 27176  | Atrociraptorskin Cap of Gathering                 | 74    | White    | DoL  |
| 27177  | Atrociraptorskin Vest of Gathering                | 74    | White    | DoL  |
| 27178  | Atrociraptorskin Gloves of Gathering              | 74    | White    | DoL  |
| 27179  | Pixie Cotton Slops of Gathering                   | 74    | White    | DoL  |
| 27180  | Atrociraptorskin Boots of Gathering               | 74    | White    | DoL  |
| 27206  | Smilodonskin Survival Belt                        | 71    | White    | DoL  |
| 27207  | Smilodonskin Earrings                             | 71    | White    | DoL  |
| 27208  | Smilodonskin Choker                               | 71    | White    | DoL  |
| 27209  | Smilodonskin Wristband                            | 71    | White    | DoL  |
| 27210  | Smilodonskin Ring                                 | 71    | White    | DoL  |
| 27085  | Deepgold Pickaxe                                  | 71    | White    | MIN  |
| 27096  | Deepgold Sledgehammer                             | 71    | White    | MIN  |
| 27106  | Bluespirit Pickaxe                                | 74    | White    | MIN  |
| 27117  | Bluespirit Sledgehammer                           | 74    | White    | MIN  |

Print in Artisan format? (y/n): y

Normal (White) items:
1x Deepgold Hatchet  
1x Deepgold Scythe  
1x Bluespirit Hatchet  
1x Bluespirit Scythe  
1x Brightlinen Turban of Gathering  
1x Brightlinen Coat of Gathering  
1x Smilodonskin Gloves of Gathering  
1x Brightlinen Bottoms of Gathering  
1x Smilodonskin Shoes of Gathering  
1x Atrociraptorskin Cap of Gathering  
1x Atrociraptorskin Vest of Gathering  
1x Atrociraptorskin Gloves of Gathering  
1x Pixie Cotton Slops of Gathering  
1x Atrociraptorskin Boots of Gathering  
1x Smilodonskin Survival Belt  
1x Smilodonskin Earrings  
1x Smilodonskin Choker  
1x Smilodonskin Wristband  
1x Smilodonskin Ring  
1x Deepgold Pickaxe  
1x Deepgold Sledgehammer  
1x Bluespirit Pickaxe  
1x Bluespirit Sledgehammer  

In this example, we entered our classes as **MIN, BTN**, and our levels as **71, 72-74**.

## Additional Documentation and Acknowledgments

This project includes the following files sourced from external repositories:

   - Item.csv  
   - ClassJobCategory.json

Original files are from xivapi/ffxiv-datamining, © XIVAPI. These files are used under the assumption that they are licensed under the MIT License, if you are the rights holder and believe this is incorrect, please contact us.
