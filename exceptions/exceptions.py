class InvalidPath(ValueError):
    """ Invalid Path to directory of file exception """


class InvalidOptions(Exception):
    """ Invalid set of options provided """


class InvalidDate(ValueError):
    """ Invalid set of options provided """


class ServerError(Exception):
    """ exception if server is down """


class DownloadFailure(Exception):
    """ exception if server is down """


class UploadFailure(Exception):
    """ exception if uploading video fails """
