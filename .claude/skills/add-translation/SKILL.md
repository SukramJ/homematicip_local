---
name: add-translation
description: Add or update translation keys for i18n. Covers strings.json (primary source), en.json sync, and de.json German translations. Use when adding new log messages, UI strings, or updating existing translations.
---

# Adding a Translation

**IMPORTANT**: `aiohomematic/strings.json` is the **primary source** for all translation keys. The file `translations/en.json` is automatically synchronized from `strings.json`.

## Step 1: Use Translation in Code

```python
from aiohomematic import i18n

# In code (for log messages)
_LOGGER.info(i18n.tr("log.my.message.key", param=value))
```

## Step 2: Add to Translation Catalogs (in this order)

```bash
# Step 1: Add key to aiohomematic/strings.json (PRIMARY SOURCE)
{
  "log.my.message.key": "My message with {param}"
}

# Step 2: Run sync script to copy to en.json
python script/check_i18n_catalogs.py --fix

# Step 3: Add German translation to translations/de.json
{
  "log.my.message.key": "Meine Nachricht mit {param}"
}
```

## Step 3: Validate Translations

```bash
python script/check_i18n.py aiohomematic/  # Check usage in code
python script/check_i18n_catalogs.py       # Check catalog sync
```

## Key Files

| File                                | Purpose                                 |
| ----------------------------------- | --------------------------------------- |
| `aiohomematic/strings.json`         | Primary source for all translation keys |
| `aiohomematic/translations/en.json` | Auto-synced from strings.json           |
| `aiohomematic/translations/de.json` | German translations (manual)            |
| `script/check_i18n.py`              | Validate translation usage in code      |
| `script/check_i18n_catalogs.py`     | Check catalog sync between files        |
