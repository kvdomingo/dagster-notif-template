from dagster import asset


@asset
def debug__asset_that_explodes() -> float:
    return 1 / 0
