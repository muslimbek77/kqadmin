from rest_framework.schemas.openapi import AutoSchema


class SafeAutoSchema(AutoSchema):
    def get_filter_parameters(self, path, method):
        parameters = []
        if not self.allows_filters(path, method):
            return parameters

        for filter_backend in self.view.filter_backends:
            backend = filter_backend()
            if hasattr(backend, "get_schema_operation_parameters"):
                parameters += backend.get_schema_operation_parameters(self.view)
        return parameters
