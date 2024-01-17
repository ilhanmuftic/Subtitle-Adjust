import sys
import re

def shift_timecode(timecode, offset):
    time_parts = re.split('[:,]', timecode)
    hours, minutes, seconds, milliseconds = map(int, time_parts)
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    shifted_seconds = total_seconds + offset
    shifted_hours, remainder = divmod(shifted_seconds, 3600)
    shifted_minutes, shifted_seconds = divmod(remainder, 60)
    shifted_milliseconds = (shifted_seconds - int(shifted_seconds)) * 1000
    return f"{int(shifted_hours):02d}:{int(shifted_minutes):02d}:{int(shifted_seconds):02d},{int(shifted_milliseconds):03d}"

def adjust_subtitle_timing(filename, offset):
    with open(filename, "r") as file:
        lines = file.readlines()

    for i in range(0, len(lines)):
        if '-->' in lines[i]:
            try:
                start_time, arrow, end_time = lines[i].strip().split()
                lines[i] = f"{shift_timecode(start_time, offset)} {arrow} {shift_timecode(end_time, offset)}\n"
            except ValueError:
                print(f"Error processing line {i + 1}: {lines[i]}")

    output_filename = f"shifted_{offset}_{filename}"
    with open(output_filename, "w") as file:
        file.writelines(lines)

    print(f"Subtitle file '{output_filename}' created with adjusted timing.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python adjust_subtitles.py <filename.srt> <offset_in_seconds>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        offset = float(sys.argv[2])
    except ValueError:
        print("Error: Offset must be a valid number.")
        sys.exit(1)

    adjust_subtitle_timing(filename, offset)
