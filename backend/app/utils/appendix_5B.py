import re
from pathlib import Path

import pdfplumber

APPENDIX_5B_RE = re.compile(r"\bAppendix\s+5B\b", re.IGNORECASE)
APPENDIX_RE = re.compile(r"\bAppendix\s+\d+[A-Z]\b", re.IGNORECASE)
NUMBERED_ITEM_RE = re.compile(r"^(?P<number>\d+\.\d+)\s+(?P<label>.*)")
SUB_ITEM_RE = re.compile(r"^\((?P<number>[a-z])\)\s+(?P<label>.*)", re.IGNORECASE)
SECTION_RE = re.compile(r"^(?P<number>\d+)\.\s+(?P<label>.*)")
AMOUNT_PAIR_RE = re.compile(
    r"(?<![\w)])(?P<current>\(-?\d[\d,]*\)|-?\d[\d,]*|-)\s+"
    r"(?P<comparison>\(-?\d[\d,]*\)|-?\d[\d,]*|-)(?=\s|$)"
)
SECTION_LABELS = {
    1: "Cash flows from operating activities",
    2: "Cash flows from investing activities",
    3: "Cash flows from financing activities",
    4: "Net increase / (decrease) in cash and cash equivalents for the period",
}


def parse_amount(val_str):
    """Converts a string representation of a financial value into an integer."""
    if not val_str:
        return 0
    # Clean whitespace and unwanted characters
    cleaned = val_str.replace(" ", "").replace("$", "").replace(",", "").strip()
    if not cleaned or cleaned == "-":
        return 0
    # Handle negative numbers wrapped in parentheses, e.g., (227)
    if cleaned.startswith("(") and cleaned.endswith(")"):
        return -int(cleaned[1:-1])
    try:
        return int(cleaned)
    except ValueError:
        return 0


def _clean_text(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _trim_label_prefix(label):
    label = _clean_text(label)
    label = re.sub(
        r"^\d+(?:\.\d+)+(?:\([a-z]\))?\.?\s*",
        "",
        label,
        flags=re.IGNORECASE,
    )
    label = re.sub(r"^\([a-z]\)\s*", "", label, flags=re.IGNORECASE)
    return label.strip(" .")


def _is_appendix_5b_table_page(text):
    return bool(
        APPENDIX_5B_RE.search(text)
        and re.search(r"\bquarterly\s+cash\s+flow\s+report\b", text, re.IGNORECASE)
    )


def _appendix_5b_page_indices(pdf):
    """Locate Appendix 5B page indexes before doing cash-flow extraction."""
    appendix_5b_pages = []
    appendix_pages = []
    in_appendix_5b = False

    for index, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        is_appendix_5b_table_page = _is_appendix_5b_table_page(text)
        if is_appendix_5b_table_page:
            in_appendix_5b = True
        elif in_appendix_5b and APPENDIX_RE.search(text):
            in_appendix_5b = False

        if in_appendix_5b:
            appendix_pages.append(index)

        if is_appendix_5b_table_page:
            appendix_5b_pages.append(index)

    if appendix_pages:
        return sorted(set(appendix_pages))
    if appendix_5b_pages:
        return appendix_5b_pages
    return range(len(pdf.pages))


def _strip_amount_pair(text):
    match = AMOUNT_PAIR_RE.search(text)
    if not match:
        return _clean_text(text), ""
    label = _clean_text(text[: match.start()] + " " + text[match.end() :])
    return label, match.group("current")


def _line_item_from_buffer(item):
    if not item:
        return None

    label, value = _strip_amount_pair(" ".join(item["lines"]))
    if not value:
        return None

    label = _trim_label_prefix(label)
    if not label:
        return None

    section_label = item.get("section_label")
    parent_label = item.get("parent_label")
    if parent_label:
        label = f"{parent_label} - {label}"

    if section_label:
        label = f"{section_label} - {label}"

    return label, value


def _cash_flow_items_from_text(text):
    current_item = None
    current_section_number = None
    section_label = ""
    parent_label = ""
    active_cash_flow_section = False

    for raw_line in text.splitlines():
        line = _clean_text(raw_line)
        if not line:
            continue

        if re.search(r"\bASX\s+Listing\s+Rules\b|\bSee\s+chapter\s+19\b", line, re.IGNORECASE):
            if current_item:
                item = _line_item_from_buffer(current_item)
                if item:
                    yield item
                current_item = None
            continue

        section_match = SECTION_RE.match(line)
        if section_match and not NUMBERED_ITEM_RE.match(line):
            section_number = int(section_match.group("number"))
            active_cash_flow_section = 1 <= section_number <= 4
            current_section_number = section_number if active_cash_flow_section else None
            section_label = _trim_label_prefix(section_match.group("label"))
            parent_label = ""

            if current_item:
                item = _line_item_from_buffer(current_item)
                if item:
                    yield item
            current_item = None
            continue

        numbered_match = NUMBERED_ITEM_RE.match(line)
        sub_item_match = SUB_ITEM_RE.match(line)
        starts_item = numbered_match or sub_item_match

        if numbered_match:
            section_number = int(numbered_match.group("number").split(".", 1)[0])
            active_cash_flow_section = 1 <= section_number <= 4
            if active_cash_flow_section and current_section_number != section_number:
                current_section_number = section_number
                section_label = SECTION_LABELS.get(section_number, "")

        if not active_cash_flow_section:
            continue

        if starts_item:
            if current_item:
                item = _line_item_from_buffer(current_item)
                if item:
                    yield item

            label_part = starts_item.group("label")
            if numbered_match and not AMOUNT_PAIR_RE.search(line):
                parent_label = _trim_label_prefix(label_part)

            current_item = {
                "lines": [line],
                "section_label": section_label,
                "parent_label": parent_label if sub_item_match else "",
            }
            continue

        if not current_item:
            section_label = _clean_text(f"{section_label} {line}")
            continue

        if current_item:
            current_item["lines"].append(line)

    if current_item:
        item = _line_item_from_buffer(current_item)
        if item:
            yield item


def extract_cash_flows(pdf_path):
    """Extract every current-quarter cash-flow item from Appendix 5B."""
    extracted_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_index in _appendix_5b_page_indices(pdf):
            page = pdf.pages[page_index]
            text = page.extract_text() or ""

            for label, value in _cash_flow_items_from_text(text):
                extracted_data[label] = parse_amount(value)

    return extracted_data

if __name__ == '__main__':
    data = extract_cash_flows(Path(__file__).parent / 'data/VAL/cash_flow_30_April.PDF')
    for k, v in data.items():
        print(k,":", v)
