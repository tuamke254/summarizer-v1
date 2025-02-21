import unittest
import json

from app.modules.processor.controller import ProcessorController


def test_index():
    processor_controller = ProcessorController()
    result = processor_controller.index()
    assert result == {'message': 'Hello, World!'}
