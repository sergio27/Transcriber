from collections import OrderedDict

import xmltodict

def get_segments(path, filename):
    with open(f"{path}/{filename}") as file:
        text = file.read()

    transcription = xmltodict.parse(text)

    speakers = {"(no speaker)": "(no speaker)", "overlap": "overlap"}
    xml_speakers = transcription["Trans"]["Speakers"]["Speaker"]

    if type(xml_speakers) == OrderedDict:
        return []
    else:
        for speaker in xml_speakers:
            speaker_id = speaker["@id"]
            speaker_name = speaker["@name"]

            speakers[speaker_id] = speaker_name

    turns = transcription["Trans"]["Episode"]["Section"]["Turn"]

    all_segments = []

    for turn in turns:
        if "@speaker" in turn:
            turn_speaker = turn["@speaker"]
            if " " in turn_speaker:
                turn_speaker = "overlap"
        else:
            turn_speaker = "(no speaker)"

        segments = turn["Sync"]

        # There's just one segment in the turn.
        if not isinstance(segments, list):
            if "#text" in turn:
                turn_text = turn["#text"]
            else:
                turn_text = ""

            segment = {
                    "speaker": speakers[turn_speaker],
                    "text": turn_text,
                    "start_time": turn["@startTime"]
            }
            all_segments.append(segment)

        # There's more than one segment in the turn.
        else:
            if "#text" in turn:
                texts = turn["#text"].split("\n\n")
            else:
                texts = [""]

            if len(segments) > len(texts):
                difference = len(segments) - len(texts)
                for n in range(difference):
                    texts.append("")

            for index in range(len(segments)):
                segment = {
                    "speaker": speakers[turn_speaker],
                    "text": texts[index],
                    "start_time": segments[index]["@time"]
                }
                all_segments.append(segment)

    for index in range(len(all_segments)):
        current_segment = all_segments[index]

        if index < len(all_segments) - 1:
            next_segment = all_segments[index + 1]
            duration = float(next_segment["start_time"]) - float(current_segment["start_time"])
            current_segment["duration"] = duration
        else:
            end_time = transcription["Trans"]["Episode"]["Section"]["@endTime"]
            duration = float(end_time) - float(current_segment["start_time"])
            current_segment["duration"] = duration

    return all_segments
