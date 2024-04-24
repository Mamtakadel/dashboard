from drf_yasg import openapi

todo_params = [
    openapi.Parameter(
        name="layer",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        enum=["building", "road"],
        description="layer type",
    ),
    openapi.Parameter(
        name="ward_no",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
        description="ward number",
    ),
]