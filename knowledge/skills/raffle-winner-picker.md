# Canonical Skill: raffle-winner-picker

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--raffle-winner-picker`

## Summary
Picks random winners from lists, spreadsheets, or Google Sheets for giveaways, raffles, and contests. Ensures fair, unbiased selection with transparency.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `raffle-winner-picker/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/raffle-winner-picker/SKILL.md))

## Metadata
- Tags: `raffle-winner-picker, skill, skill-md`
- Languages: `c`
- Systems: `slack`
- Jobs: `raffle-winner-picker, skill-md`
- Roles: ``

## Steps
1. **Duplicate Prevention**: Ensures the same person can't win twice
2. **Multiple Sources**: Works with CSV, Excel, Google Sheets, or plain lists
3. **Multiple Winners**: Can pick one or multiple winners
4. **Random Selection**: Uses cryptographically random selection
5. **Transparent Results**: Shows the selection process clearly
6. **Winner Details**: Displays all relevant information about winners
7. Alice (alice@email.com)
8. Bob (bob@email.com)
9. Carol (carol@email.com)
10. Choosing winners from contest submissions
11. Export winner details?
12. Fair distribution of limited spots or resources
13. No bias or patterns
14. Pick another winner (excluding Sarah)?
15. Pick runner-ups?
16. Picking raffle winners at events
17. Random team assignments
18. Randomly selecting participants for surveys or tests
19. Running social media giveaways
20. Uses secure random number generation

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: raffle-winner-picker/SKILL.md
# Raffle Winner Picker

This skill randomly selects winners from lists, spreadsheets, or Google Sheets for giveaways and contests.

## When to Use This Skill

- Running social media giveaways
- Picking raffle winners at events
- Randomly selecting participants for surveys or tests
- Choosing winners from contest submissions
- Fair distribution of limited spots or resources
- Random team assignments

## What This Skill Does

1. **Random Selection**: Uses cryptographically random selection
2. **Multiple Sources**: Works with CSV, Excel, Google Sheets, or plain lists
3. **Multiple Winners**: Can pick one or multiple winners
4. **Duplicate Prevention**: Ensures the same person can't win twice
5. **Transparent Results**: Shows the selection process clearly
6. **Winner Details**: Displays all relevant information about winners

## How to Use

### From Google Sheets

```
Pick a random row from this Google Sheet to select a winner 
for a giveaway: [Sheet URL]
```

### From Local File

```
Pick 3 random winners from entries.csv
```

### From List

```
Pick a random winner from this list:
- Alice (alice@email.com)
- Bob (bob@email.com)
- Carol (carol@email.com)
...
```

### Multiple Winners

```
Pick 5 random winners from contest-entries.xlsx, 
make sure no duplicates
```

## Example

**User**: "Pick a random row from this Google Sheet to select a winner for a giveaway."

**Output**:
```
Accessing Google Sheet...
Total entries found: 247

Randomly selecting winner...

🎉 WINNER SELECTED! 🎉

Row #142
Name: Sarah Johnson
Email: sarah.j@email.com
Entry Date: March 10, 2024
Comment: "Love your newsletter!"

Selection method: Cryptographically random
Timestamp: 2024-03-15 14:32:18 UTC

Would you like to:
- Pick another winner (excluding Sarah)?
- Export winner details?
- Pick runner-ups?
```

**Inspired by:** Lenny's use case - picking a Sora 2 giveaway winner from his subscriber Slack community

## Features

### Fair Selection
- Uses secure random number generation
- No bias or patterns
- Transparent process
- Repeatable with seed (for verification)

### Exclusions
```
Pick a random winner excluding previous winners: 
Alice, Bob, Carol
```

### Weighted Selection
```
Pick a winner with weighted probability based on 
the "entries" column (1 entry = 1 ticket)
```

### Runner-ups
```
Pick 1 winner and 3 runner-ups from the list
```

## Example Workflows

### Social Media Giveaway
1. Export entries from Google Form to Sheets
2. "Pick a random winner from [Sheet URL]"
3. Verify winner details
4. Announce publicly with timestamp

### Event Raffle
1. Create CSV of attendee names and emails
2. "Pick 10 random winners from attendees.csv"
3. Export winner list
4. Email winners directly

### Team Assignment
1. Have list of participants
2. "Randomly split this list into 4 equal teams"
3. Review assignments
4. Share team rosters

## Tips

- **Document the process**: Save the timestamp and method
- **Public announcement**: Share selection details for transparency
- **Check eligibility**: Verify winner meets contest rules
- **Have backups**: Pick runner-ups in case winner is ineligible
- **Export results**: Save winner list for records

## Privacy & Fairness

✓ Uses cryptographically secure randomness
✓ No manipulation possible
✓ Timestamp recorded for verification
✓ Can provide seed for third-party verification
✓ Respects data privacy

## Common Use Cases

- Newsletter subscriber giveaways
- Product launch raffles
- Conference ticket drawings
- Beta tester selection
- Focus group participant selection
- Random prize distribution at events
