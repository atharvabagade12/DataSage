"""
Shared missing value markers used across the entire DataSage pipeline.

This list is passed as `na_values` to pd.read_csv / pd.read_excel / pd.read_json
so that these placeholders are recognized as NaN at load time.
"""

MISSING_VALUE_MARKERS = [
    '',  ' ',  '  ',                                    # Empty / whitespace
    '?', '-', '--', '---', '...', '.',                  # Common placeholders
    'null', 'NULL', 'Null',                             # Null variants
    'None', 'none', 'NONE',                             # None variants
    'NA', 'N/A', 'n/a', 'na', 'Na',                    # NA variants
    'NaN', 'nan', 'NAN',                                # NaN variants
    'missing', 'Missing', 'MISSING',                    # Missing variants
    'undefined', 'Undefined', 'UNDEFINED',              # Undefined variants
    'not available', 'Not Available', 'NOT AVAILABLE',  # Not available variants
    'nil', 'NIL', 'Nil',                                # Nil variants
    '#N/A', '#NA', '#N/A N/A',                          # Excel error codes
    '#VALUE!', '#REF!', '#DIV/0!', '#NULL!', '#NAME?', '#NUM!',
    '-1.#IND', '1.#QNAN', '1.#IND',                    # C-level NaN representations
]
