import pandas as pd

# Job abbreviations and their numeric equivalents
JOB_MAPPING = {
    # Base classes mapped to their advanced versions
    "GLA": 20, "PLD": 20,
    "MRD": 22, "WAR": 22,
    "LNC": 23, "DRG": 23,
    "ARC": 24, "BRD": 24,
    "CNJ": 25, "WHM": 25,
    "THM": 26, "BLM": 26,
    "ACN": 28, "SMN": 28,
    "ROG": 92, "NIN": 92,
    "SCH": 29, "MNK": 21,
    "DRK": 98, "AST": 99,
    
    # Crafters
    "CRP": 9, "BSM": 10, "ARM": 11, "GSM": 12, "LTW": 13,
    "WVR": 14, "ALC": 15, "CUL": 16,

    # Gatherers
    "MIN": 17, "BTN": 18, "FSH": 19, 
    
    # Special case
    "ALL": 1
}

# Create reverse mapping with additional categories
NUM_TO_JOB = {
    **{v: k for k, v in JOB_MAPPING.items()},
    30: "DoW",  # Disciple of War
    31: "DoM",  # Disciple of Magic
    33: "DoH",  # Disciple of the Hand
    32: "DoL"   # Disciple of the Land
}

# Job display lists
COMBAT_JOBS = [
    # Tanks
    "GLA", "PLD", "MRD", "WAR", "DRK",
    # Melee DPS
    "LNC", "DRG", "ROG", "NIN", "MNK",
    # Ranged Physical DPS
    "ARC", "BRD",
    # Magical Ranged DPS
    "THM", "BLM", "ACN", "SMN",
    # Healers
    "CNJ", "WHM", "SCH", "AST"
]

CRAFTERS = [
    #Crafters
    "CRP", "BSM", "ARM", "GSM", "LTW", 
    "WVR", "ALC", "CUL",
]

GATHERERS = [
    #Gatherers
    "MIN", "BTN", "FSH"
]


# Define which jobs belong to each broader category
DOW_JOBS = ["GLA", "PLD", "MRD", "WAR", "LNC", "DRG", "ARC", "BRD", "ROG", "NIN", "MNK", "DRK"]
DOM_JOBS = ["CNJ", "WHM", "THM", "BLM", "ACN", "SMN", "SCH", "AST"]
DOH_JOBS = ["CRP", "BSM", "ARM", "GSM", "LTW", "WVR", "ALC", "CUL"]
DOL_JOBS = ["MIN", "BTN", "FSH"]

# Rarity mapping
RARITY_MAP = {
    0: "Blank",
    1: "White",
    2: "Green (Expert)",
    3: "Blue (Rare)",
    4: "Purple (Relic)",
    7: "Pink (Aetherial)"
}

def get_job_input():
    """Get and validate job abbreviations from user"""
    print("\nAvailable Jobs:")
    print("Combat:", ", ".join(COMBAT_JOBS))
    print("Crafters:", ", ".join(CRAFTERS))
    print("Gatherers:", ", ".join(GATHERERS)) 

    while True:
        input_str = input("\nEnter one or more job abbreviations (comma separated) or 'ALL': ").strip().upper()
        if not input_str:
            print("Please enter at least one job or 'ALL'")
            continue
            
        jobs = [j.strip() for j in input_str.split(',')]
        invalid_jobs = [j for j in jobs if j not in JOB_MAPPING]
        
        if invalid_jobs:
            print(f"Invalid job codes: {', '.join(invalid_jobs)}")
            print("Please try again with valid 3-letter codes")
            continue
        
        # Convert to job IDs and add broader categories if needed
        job_ids = []
        for job in jobs:
            job_ids.append(JOB_MAPPING[job])
        
        # Check if we need to add broader categories
        if any(job in DOW_JOBS for job in jobs):
            job_ids.append(30)  # Add DoW
        if any(job in DOM_JOBS for job in jobs):
            job_ids.append(31)  # Add DoM
        if any(job in DOH_JOBS for job in jobs):
            job_ids.append(33)  # Add DoH
        if any(job in DOL_JOBS for job in jobs):
            job_ids.append(32)  # Add DoL
            
        # Remove duplicates while preserving order
        seen = set()
        unique_job_ids = []
        for job_id in job_ids:
            if job_id not in seen:
                seen.add(job_id)
                unique_job_ids.append(job_id)
                
        return unique_job_ids

def get_level_input():
    """Get and validate level input from user, supporting multiple values and ranges"""
    print("\nEnter level(s) in one of these formats:")
    print("- Single level: 50")
    print("- Multiple levels: 50, 52, 55")
    print("- Level ranges: 50-54 (inclusive)")
    print("- Mixed: 50, 52-54, 56, 60-62")
    
    while True:
        level_input = input("\nEnter level(s) (1-100): ").strip()
        if not level_input:
            print("Error: Please enter at least one level")
            continue
            
        try:
            # Clean input and split into parts
            parts = [p.strip() for p in level_input.split(',') if p.strip()]
            levels = set()
            
            for part in parts:
                if '-' in part:
                    # Handle range
                    range_parts = part.split('-')
                    if len(range_parts) != 2:
                        print(f"Error: Invalid range format '{part}'. Use 'min-max'")
                        raise ValueError
                    
                    level_min = int(range_parts[0])
                    level_max = int(range_parts[1])
                    
                    # Clamp values to 1-100 range
                    level_min = max(1, min(level_min, 100))
                    level_max = max(1, min(level_max, 100))
                    
                    if level_min > level_max:
                        print(f"Error: Invalid range '{part}'. First number must be <= second number")
                        raise ValueError
                        
                    levels.update(range(level_min, level_max + 1))
                else:
                    # Handle single level
                    level = int(part)
                    level = max(1, min(level, 100))  # Clamp to 1-100
                    levels.add(level)
            
            if not levels:
                print("Error: No valid levels entered")
                continue
                
            return sorted(levels)  # Returns a list like [50, 52, 53, 54, 56]
            
        except ValueError:
            print("Error: Please enter valid numbers/ranges (e.g., '50, 52-54, 56')")
            continue

def main():
    try:
        # Load the data file
        df = pd.read_csv('Item.csv', low_memory=False)
    except Exception as e:
        print(f"Error loading Item.csv: {e}")
        return

    # Get user inputs
    job_ids = get_job_input()
    levels = get_level_input()

    # Convert columns to appropriate types
    try:
        # Column indices:
        # 0=ID, 10=Name, 13=Rarity, 
        # 22=IsUnique, 28=CanBeHq, 
        # 41=Level, 44=JobID
        df['_level'] = pd.to_numeric(df.iloc[:, 41], errors='coerce')
        df['_jobid'] = pd.to_numeric(df.iloc[:, 44], errors='coerce')
        df['_is_unique'] = df.iloc[:, 22].astype(str).str.upper() == 'TRUE'
        df['_can_be_hq'] = df.iloc[:, 28].astype(str).str.upper() == 'TRUE'
        df['_rarity'] = pd.to_numeric(df.iloc[:, 13], errors='coerce').fillna(0).astype(int)
    except Exception as e:
        print(f"Error converting data types: {e}")
        return

    # Apply filters
    try:
        # Level filter
        level_filter = df['_level'].isin(levels)
        filtered_df = df[level_filter].copy()
        
        # Job filter if specified
        if job_ids:
            job_filter = filtered_df['_jobid'].isin(job_ids)
            filtered_df = filtered_df[job_filter].copy()
    except Exception as e:
        print(f"Error applying filters: {e}")
        return

    # Prepare results
    results = []
    try:
        for _, row in filtered_df.iterrows():
            try:
                item_id = str(row.iloc[0]) if pd.notna(row.iloc[0]) else "N/A"
                name = str(row.iloc[10]) if pd.notna(row.iloc[10]) else "Unknown"
                level = int(row['_level']) if pd.notna(row['_level']) else 0
                job_num = int(row['_jobid']) if pd.notna(row['_jobid']) else 0
                job_abbr = NUM_TO_JOB.get(job_num, str(job_num))
                is_unique = bool(row['_is_unique']) if pd.notna(row['_is_unique']) else False
                can_be_hq = bool(row['_can_be_hq']) if pd.notna(row['_can_be_hq']) else False
                rarity = int(row['_rarity']) if pd.notna(row['_rarity']) else 0
                rarity_str = RARITY_MAP.get(rarity, f"Unknown ({rarity})")
                results.append([item_id, name, level, job_abbr, is_unique, can_be_hq, rarity, rarity_str])
            except Exception as e:
                print(f"Warning: Error processing row - {e}")
                continue
    except Exception as e:
        print(f"Error processing results: {e}")
        return

    # Sort results by job abbreviation
    results.sort(key=lambda x: x[3])

    # Display results
    if not results:
        print("\nNo items found matching your criteria")
        print("Debug info:")
        print(f"Total items: {len(df)}")
        print(f"After level filter: {len(df[level_filter])}")
        if job_ids:
            print(f"After job filter: {len(filtered_df)}")
        return

    print(f"\nResults ({len(results)} items found):")
    print("{:<6} {:<50} {:<6} {:<8} {}".format("#", "Name", "Level", "Rarity", "Job"))
    print("-" * 80)
    for item_id, name, level, job, _, _, _, rarity_str in results:
        print("{:<6} {:<50} {:<6} {:<8} {}".format(item_id, name, level, rarity_str, job))

    # Ask about Artisan format
    while True:
        artisan = input("\nPrint in Artisan format? (y/n): ").strip().lower()
        if artisan in ['y', 'n']:
            break
        print("Please enter 'y' or 'n'")

    if artisan == 'y':
        # Separate craftable HQ items by rarity
        normal_items = [item for item in results if item[5] and not item[4] and item[6] == 1]  # White/Normal
        green_items = [item for item in results if item[5] and not item[4] and item[6] == 2]   # Green
        blue_items = [item for item in results if item[5] and not item[4] and item[6] == 3]    # Blue
        
        # Print each rarity section if it has items
        if normal_items:
            print("\nNormal (White) items:")
            for item in normal_items:
                print(f"1x {item[1]}")
        
        if green_items:
            print("\nGreen (Expert) items:")
            for item in green_items:
                print(f"1x {item[1]}")
        
        if blue_items:
            print("\nBlue (Rare) items:")
            for item in blue_items:
                print(f"1x {item[1]}")
        
        # Excluded items list remains the same
        excluded_items = [item for item in results if not item[5] or item[4]]
        if excluded_items:
            print("\nExcluded items:")
            for item in excluded_items:
                tags = []
                if item[4]:
                    tags.append("Unique")
                if not item[5]:
                    tags.append("Non-HQ")
                print(f"- {item[1]} [{RARITY_MAP.get(item[6], 'Unknown')}] ({', '.join(tags)})")

if __name__ == "__main__":
    main()