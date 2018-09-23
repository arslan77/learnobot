from django.contrib.staticfiles.storage import StaticFilesStorage, ManifestStaticFilesStorage


class CustomManifestFilesMixin(StaticFilesStorage):
    manifest_strict = False