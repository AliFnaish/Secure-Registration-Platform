import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import easyocr
import re

# Avoid OpenMP conflict
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Initialize the reader once
reader = easyocr.Reader(['ar'], gpu=False)

def extract_fields_from_id(image_path):
    
    print(f"📸 Processing image: {image_path}")
    
    results = reader.readtext(image_path)
    lines = [r[1].strip() for r in results if r[1].strip()]

    print("\n📝 OCR Raw Lines Detected:")
    for idx, line in enumerate(lines):
        print(f"{idx+1}. {line}")

    field_keywords = {
        "الشهرة": "الشهرة",
        "الاب": "اسم الاب",
        "الام وشهرتها": "اسم الام وشهرتها",
        "محل الولادة": "محل الولادة"
    }

    extracted_fields = {
        "الاسم": "❌ Not Detected",
        "الشهرة": "❌ Not Detected",
        "اسم الاب": "❌ Not Detected",
        "اسم الام وشهرتها": "❌ Not Detected",
        "محل الولادة": "❌ Not Detected"
    }

    # Loop through each line and try to match the known fields
    for i, line in enumerate(lines):
        clean_line = re.sub(r"[^\u0600-\u06FF0-9a-zA-Z\s:]", "", line)
        for keyword, label in field_keywords.items():
            if keyword in clean_line:
                # Case 1: Field and value in one line with colon
                if ":" in clean_line:
                    parts = clean_line.split(":")
                    if len(parts) > 1:
                        value = parts[1].strip()
                        if len(value) > 1:
                            extracted_fields[label] = value
                else:
                    # Case 2: Field keyword is alone, value might be in next line
                    if i + 1 < len(lines):
                        next_line = re.sub(r"[^\u0600-\u06FF0-9a-zA-Z\s]", "", lines[i + 1])
                        if next_line and len(next_line.split()) <= 4:
                            extracted_fields[label] = next_line.strip()

    # Detect 'الاسم' as the line before 'الشهرة'
    for i, line in enumerate(lines):
        if "الشهرة" in line:
            for j in range(i - 1, -1, -1):
                candidate = lines[j].strip()
                if ":" not in candidate and not any(k in candidate for k in field_keywords):
                    if re.search(r"[\u0600-\u06FF]", candidate):
                        extracted_fields["الاسم"] = candidate
                        break
            break

    print("\n🔍 Final Extracted Fields:")
    for label in extracted_fields:
        print(f"{label}: {extracted_fields[label]}")

    return extracted_fields
