# ComfyUI Prompt Filter Node

A custom node for ComfyUI that filters specific words from prompts while preserving bracket structures and weight syntax.

## Features

- **Exact Match Filtering**: Only items that exactly match filter words (comma-separated) are removed
- **Bracket Structure Preservation**: Supports parentheses `()`, square brackets `[]`, curly brackets `{}`
- **Weight Syntax Support**: Preserves weight syntax like `:1.2`
- **Nested Bracket Handling**: Correctly processes multi-level nested bracket structures
- **Auto Cleanup**: Removes empty brackets and redundant commas

## Filtering Logic

This node uses **exact matching on comma-separated items**:

### Examples

1. **Basic Filtering**:
   - Input: `"beautiful girl, red, blue eyes, anime style"`
   - Filter: `"red, blue"`
   - Output: `"beautiful girl, blue eyes, anime style"`
   - Note: Only exact match `"red"` is removed, `"blue eyes"` is preserved

2. **Partial Matches Not Filtered**:
   - Input: `"red dress, red hair"`
   - Filter: `"red"`
   - Output: `"red dress, red hair"`
   - Note: `"red dress"` and `"red hair"` don't exactly match `"red"`, so they're preserved

3. **Bracket Handling**:
   - Input: `"(hi, I, am, a, girl)"`
   - Filter: `"girl, hi"`
   - Output: `"(I, am, a)"`

4. **Weight Syntax**:
   - Input: `"((1girl, loli, nude, NSFW):1.2)"`
   - Filter: `"nude, NSFW"`
   - Output: `"((1girl, loli):1.2)"`

## Installation

See [INSTALL.md](INSTALL.md) for details.

## Usage

1. Add "Prompt Filter" node in ComfyUI
2. Connect text input to `input_prompt`
3. Enter filter words in `filter_words` parameter (comma-separated)
4. Get filtered result from `output_prompt`

## Project Structure

```
prompt_filter/
├── __init__.py                 # Module initialization
├── nodes/
│   └── prompt_filter_node.py  # ComfyUI node implementation
├── utils/
│   └── text_processor.py      # Text processing logic
├── config/
│   └── node_config.py         # Node configuration
├── tests/
│   └── test_text_processor.py # Unit tests
├── README.md                   # Chinese documentation
├── README_EN.md               # English documentation
└── INSTALL.md                 # Installation guide
```

## Technical Features

1. **Atomic Design**: Each module has a single responsibility for easy maintenance
2. **Tree Structure**: Clear directory organization
3. **Low Coupling**: Minimal dependencies between modules
4. **Bilingual Support**: Chinese and English documentation
5. **User-Friendly**: Simple and intuitive interface

## Testing

Run test suite:
```bash
python tests/test_text_processor.py
```

## License

GPL-3.0 License 