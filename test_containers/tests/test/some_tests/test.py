#!/usr/bin/env python3

from exasol_python_test_framework import udf


class SuccessfulTest(udf.TestCase):

    def test_dummy(self):
        pass


if __name__ == '__main__':
    udf.main()
