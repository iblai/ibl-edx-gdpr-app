from tutor import hooks
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "FEATURES[ACCOUNT_DELETION] = True"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "RETIRED_USER_SALTS = ['some-Complicated-something', 'some-Complicated-something']"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "RETIREMENT_SERVICE_WORKER_USERNAME=ibl.retirement.user"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "HOST = 'koa-devlms.socialgoodplatform.com'"
    )
)
