import segmenter
import transcriber
import pandas

from os import listdir
from os.path import isfile, join


def find_errors():
    wrong_segments = []

    wrong_segments.extend(transcriber.check_characters())
    wrong_segments.extend(transcriber.check_for_common_errors())
    wrong_segments.extend(transcriber.check_initialisms())
    wrong_segments.extend(transcriber.check_overlaps())

    new_tags = ["organization", "name_first", "name_last", "phone", "email", "url", "address",
                "date_time", "credit_debit_number", "credit_debit_expiry", "credit_debit_cvv"]

    for tag in new_tags:
        wrong_segments.extend(transcriber.check_new_tag(tag, True))

    agent_names = ["Parvinder", "Gershom", "Joanne", "Caprice", "Amanda", "Freddy", "Freddie",
                   "Kevin", "Blaise", "Rachel", "Ian"]
    for name in agent_names:
        wrong_segments.extend(transcriber.check_for_string(name, ["<name_first>", "<email>", "<address>"]))

    wrong_segments.extend(transcriber.check_name_tags())

    data = []
    list_without_duplicates = []
    for segment in wrong_segments:

        try:
            if segment.text not in list_without_duplicates:
                list_without_duplicates.append(segment.text)
            else:
                continue

            data.append(
                {
                    "filename": segment.filename,
                    "type": segment.category,
                    "content": segment.content,
                    "text": segment.text
                })
        except IndexError:
            print(segment)

    new_data = pandas.DataFrame(data)
    new_data.to_csv("output/errors_found.csv")

    print(f"CSV file saved. Logged errors in {len(list_without_duplicates)} segments.")


def log_all_new_tags():
    new_tags = ["organization", "name_first", "name_last", "phone", "email", "url", "address",
                "date_time", "credit_debit_number", "credit_debit_expiry", "credit_debit_cvv"]

    segments_with_tags = []

    for new_tag in new_tags:
        results = transcriber.check_for_tag(new_tag)

        for result in results:
            segments_with_tags.append({
                "filename": result.filename,
                "tag": new_tag,
                "content": result.content,
                "text": result.text
            })

    new_data = pandas.DataFrame(segments_with_tags)
    new_data.to_csv("output/all_new_tags.csv")

    print(f"CSV file saved. Logged {len(segments_with_tags)} segments with new tags.")


def find_occurrences():
    searched_terms = ["<organization>", "<name_first>", "<name_last>", "<phone>", "<email>", "<url>", "<address>",
                      "<date_time>", "<credit_debit_number>", "<credit_debit_expiry>", "<credit_debit_cvv>"]

    results = transcriber.search_for_occurrences(searched_terms)

    new_data = pandas.DataFrame(results)
    new_data.to_csv("output/found_occurrences.csv")

    print(f"CSV file saved. Logged occurrences in {len(results)} files.")


path = "transcriptions"
files = [f for f in listdir(path) if isfile(join(path, f))]

for filename in files:
    try:
        transcriber.working_files.append({
            "filename": filename,
            "segments": segmenter.get_segments(path, filename)
        })
    except TypeError:
        print(f"Error ({filename})")
    except:
        print(f"Error ({filename})")

log_all_new_tags()
find_errors()
