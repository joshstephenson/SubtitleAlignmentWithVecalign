import regex
from datetime import datetime

SRT_TIME_FORMAT = '%H:%M:%S,%f'
TIMECODE_SEPARATOR = ' --> '

class Subtitle:
    """
    Subtitle represents a single visual text element in a movie in just one language
    """
    srt_time_format = SRT_TIME_FORMAT

    def __init__(self, timestring, text, offset, offset_is_negative):
        self.offset = offset
        self.offset_is_negative = offset_is_negative

        # join multiple lines of text into one line if necessary
        self.text = text if type(text) is str else " ".join(text).strip()

        # Used to display subtitle timecodes
        self.timestring = timestring

        # Used to compare subtitle timecodes
        self.start = 0
        self.end = 0

        # Parse the time code into a number of milliseconds since the start
        self.parse_time_codes(offset, offset_is_negative)


    def has_content(self):
        return len(self.text) > 0

    def parse_time_codes(self, offset, offset_is_negative):
        """
        Turn timestrings like '01:23:45,678' into an integer offset milliseconds since movie start
        :param offset: offset is a datetime object
        :param offset_is_negative: boolean to indicate whether above offset is negative
        :return: an integer duration since video start
        """

        def _parse_timestring(timestring):
            pt = datetime.strptime(timestring, SRT_TIME_FORMAT)
            if offset_is_negative:
                microsecond = pt.microsecond - offset.microsecond
                second = pt.second - offset.second
                minute = pt.minute - offset.minute
                hour = pt.hour - offset.hour
            else:
                microsecond = pt.microsecond + offset.microsecond
                second = pt.second + offset.second
                minute = pt.minute + offset.minute
                hour = pt.hour + offset.hour
            return microsecond + (second + minute * 60 + hour * 3600) * 1000000

        parts = self.timestring.split(TIMECODE_SEPARATOR)
        self.start = _parse_timestring(parts[0])
        self.end = _parse_timestring(parts[1])

    def overlap(self, other):
        """
        Find the duration of time two subtitles overlap with each other
        :param other: the other subtitle to compare with self
        :return: duration of time two subtitles overlap with each other
        """
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        return end - start

    def merge(self, other):
        """
        Merge another subtitle with this subtitle. Used when a sentence is spread across multiple subtitles.
        :param other: other subtitle to merge
        """
        self.text += " " + other.text
        self.end = other.end
        self.timestring = self.timestring.split(TIMECODE_SEPARATOR)[0] + TIMECODE_SEPARATOR + \
                          other.timestring.split(TIMECODE_SEPARATOR)[1]

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.timestring == other.timestring

    def __hash__(self):
        return hash(self.timestring)
