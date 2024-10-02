import pytest
from subtitles import Subtitles
from scripts.align import get_text

@pytest.fixture
def subs():
    text = get_text('test_data/timecode_strings.srt')
    return Subtitles(text)

def test_timecode_string_can_be_parsed(subs):
    for sub in subs:
        assert sub.start is not 0 # 0 is default
        assert sub.end is not 0   # 0 is default