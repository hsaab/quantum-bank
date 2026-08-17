"""Runs last (name sorts after other tests): exercise split teardown without affecting other tests."""


def test_destroy_split_is_idempotent():
    import split_config

    split_config.destroy_split()
    split_config.destroy_split()
