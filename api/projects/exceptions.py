from rest_framework.exceptions import APIException


class DynamoNotEnabledError(APIException):
    status_code = 400
    default_detail = "Dynamo DB is not enabled for this project"


class ProjectMigrationError(APIException):
    status_code = 400
    default_detail = "Migration is either already done or is in progress"


class TooManyIdentitiesError(APIException):
    status_code = 400
    default_detail = "Too many identities; Please contact support"


class ProjectTooLargeError(APIException):
    status_code = 400
    default_detail = "Project is too large; Please contact support"
