import re

from error import Error

from constants import VALID_TAGS, VALID_MARKUPS, VALID_ITEMS, VALID_FILLER_WORDS
from constants import INVALID_CHARACTERS, COMMON_ERRORS, NOT_INITIALISMS

working_files = []


def check_characters():
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            text = text.replace("(())", "")

            for filler_word in VALID_FILLER_WORDS:
                text = text.replace(filler_word, "")

            for tag in VALID_TAGS:
                text = text.replace(tag, "")

            for tag in VALID_MARKUPS:
                text = text.replace(f"<{tag}>", "")
                text = text.replace(f"</{tag}>", "")

            valid_overlaps = ["<overlap>", "</overlap>"]
            for overlap in valid_overlaps:
                text = text.replace(overlap, "")

            for character in INVALID_CHARACTERS:
                if character in text and (filename, segment) not in wrong_segments:
                    wrong_segments.append(Error(filename, "Character", f"({character})", segment))

    return wrong_segments


def check_overlaps():
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            if "<overlap>" in text and segment["speaker"] != "overlap":
                wrong_segments.append(Error(filename, "Overlap", "", text))

            #if "overlap" in text and text.count("overlap") < 4:
                #wrong_segments.append(Error(filename, "Overlap", "", text))

    return wrong_segments


def check_initialisms():
    wrong_segments = []
    initialisms = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            text = text.replace(".", "")
            text = text.replace(",", "")
            text = text.replace("¿", "")
            text = text.replace("?", "")
            text = text.replace("~", "")

            for word in text.split(" "):
                if len(word) > 1 and word.isupper():

                    if word not in initialisms:
                        initialisms.append(word)

                    if f"<initial>{word}</initial>" not in text and "~" not in word and word not in NOT_INITIALISMS:
                        wrong_segments.append(Error(filename, "Initialism", f"({word})", segment))

    return wrong_segments


def check_new_tag(new_tag, detail=False):
    match_segments = []
    wrong_segments = []
    tag_items = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            if f"<{new_tag}>" in text:
                result = re.search(f"<{new_tag}>(.*)</{new_tag}>", text)

                if result is None:
                    wrong_segments.append(Error(filename, f"Wrong use of tags", "", segment))
                    continue

                name = result.group(1).strip("?.")

                if len(name) < 1:
                    wrong_segments.append(Error(filename, f"Empty tag", "", segment))

                if name not in tag_items and new_tag not in name \
                        and "(())" not in name and len(name) > 1:
                    tag_items.append(name)
                match_segments.append((filename, segment))

                if len(name) > 0 and (name[0] == " " or name[-1] == " "):
                    wrong_segments.append(Error(filename, f"Remove space", f"({name})", segment))
                elif new_tag in VALID_ITEMS and name not in VALID_ITEMS[new_tag] and "<" not in name:
                    wrong_segments.append(Error(filename, f"Tag [{new_tag}]", f"({name})", segment))

    if detail:
        return wrong_segments
    else:
        return tag_items


def check_name_tags():
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            if "<name_first>" in text:
                result = re.search("<name_first>(.*)</name_first>", text)

                if result is None:
                    continue

                name = result.group(1).strip("?.,").replace(",", "")

                words = name.split()

                complete_words = 0
                for word in words:
                    if len(word) > 1:
                        complete_words += 1

                if len(words) > 2 and complete_words == 1:
                    wrong_segments.append(Error(filename, f"Check tag", f"({name})", segment))

    return wrong_segments


def check_for_common_errors():
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            for error in COMMON_ERRORS:
                if error in text:
                    wrong_segments.append(Error(filename, "Incorrect spelling", f"({error.strip()})", segment))

    return wrong_segments


def check_for_string(string, exceptions=[]):
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            exception_found = len([exception for exception in exceptions if exception in text]) > 0

            if string in text.split(" ") and not exception_found:
                wrong_segments.append(Error(filename, "String", f"({string})", segment))

    return wrong_segments


def check_for_tag(new_tag):
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            if f"<{new_tag}>" in text:
                result = re.search(f"<{new_tag}>(.*)</{new_tag}>", text)
                if result is None:
                    continue

                content = result.group(1)

                if "<" not in content:
                    wrong_segments.append(Error(filename, "Tag", content, segment))

    return wrong_segments


def check_file_for_string(string, not_string="*"):
    wrong_segments = []

    for file in working_files:
        filename = file["filename"]
        segments = file["segments"]

        for segment in segments:
            text = segment["text"]

            if string in text:
                wrong_segments.append((filename, "String", string, segment))

            if not_string in text:
                return []

    return wrong_segments


def search_for_occurrences(searched_terms):

    results = []
    for file in working_files:
        filename = file["filename"]

        result = {"filename": filename}

        for term in searched_terms:

            result[term] = 0
            segments = file["segments"]

            for segment in segments:
                text = segment["text"]

                if term in text:
                    result[term] = 1
                    continue

        results.append(result)

    return results
