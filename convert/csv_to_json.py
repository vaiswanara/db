import csv
import json

INPUT_FILE = "links2.txt"
OUTPUT_FILE = "lessons_live.json"
#OUTPUT_FILE = "lessons_archive.json"

lessons = []

with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)

    index = 1

    def first_present(row_dict, keys, default=""):
        for key in keys:
            value = row_dict.get(key)
            if value is not None:
                return value.strip()
        return default

    for row in reader:

        playlist = first_present(row, ["Playlist"])
        title = first_present(row, ["Tittle", "Title"])
        video = first_present(row, ["YouTube_Vidoe_ID", "YouTube_Video_ID"])
        pdf = first_present(row, ["google_doc_link"])
        thumbnail = f"https://img.youtube.com/vi/{video}/mqdefault.jpg"
        status = row.get('status', 'ON').strip().upper()

        # Skip OFF lessons
        if status == "OFF":
            continue

        # clean pdf
        if pdf.lower() == "none":
            pdf = ""

        # build lesson object
        lesson = {
            "id": f"{playlist}_{video}".replace(" ", "_"),
            "playlist": playlist,
            "title": title,
            "videoId": video,
            "pdfLink": pdf,
            "thumbnail": thumbnail,
            "status": status
        }

        lessons.append(lesson)
        index += 1

# final json
output = {
    "lessons": lessons
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as jsonfile:
    json.dump(output, jsonfile, indent=2, ensure_ascii=False)

print("SUCCESS: lessons.json created with", len(lessons), "lessons")
