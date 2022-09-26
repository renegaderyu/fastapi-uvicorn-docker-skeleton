#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from .context import Example


@pytest.fixture(scope="class")
def get_example_instance(request):
    request.cls.Example = Example(name="google", value="https://google.com")


@pytest.mark.incremental
@pytest.mark.usefixtures("get_example_instance")
class TestExample:
    params = {
        "test_example_instance": [
            dict(attrib="value", expected_result="https://google.com"),
            dict(attrib="name", expected_result="google"),
        ],
    }

    def test_example_instance(self, attrib, expected_result):
        assert getattr(self.Example, attrib) == expected_result
