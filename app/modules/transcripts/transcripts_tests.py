import unittest
import json

from app.modules.transcripts.controller import TranscriptsController


def test_index():
    transcripts_controller = TranscriptsController()
    result = transcripts_controller.index()
    assert result == {'message': 'Hello, World!'}
