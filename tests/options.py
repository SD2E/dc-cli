import pytest

longrun = pytest.mark.skipif(
    not pytest.config.option.longrun,
    reason="needs --longrun option to run")
