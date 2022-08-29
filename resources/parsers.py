from .course import ns
delete_parser = ns.parser()
delete_parser.add_argument(
    "course_id",
    type=str,
    help="The id of the course to be deleted",
    location="args",
    required=True
)
