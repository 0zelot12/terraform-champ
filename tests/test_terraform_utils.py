from terraform_champ.terraform_utils import (
    build_apply_command,
    contains_resource_change_actions,
    parse_changed_resources,
)


def test_get_parse_changed_resources():
    with open("./tests/fixtures/test_plan.json", "r") as f:
        json_content = f.read()

    changed_resources = parse_changed_resources(json_content)

    assert changed_resources == [
        "docker_container.nginx",
        "local_file.json_example",
        "local_file.txt_example_2",
        "local_file.txt_example_3",
    ]


def test_build_apply_command():
    result = build_apply_command([], [])
    assert result == ["terraform", "apply"]

    result = build_apply_command(["aws_instance.example"], ["aws_instance.example"])
    assert result == [
        "terraform",
        "apply",
        "-target=aws_instance.example",
        "-replace=aws_instance.example",
    ]

    result = build_apply_command(["aws_instance.example"], [])
    assert result == ["terraform", "apply", "-target=aws_instance.example"]

    result = build_apply_command([], ["aws_instance.example"])
    assert result == ["terraform", "apply", "-replace=aws_instance.example"]

    resources_to_target = ["aws_instance.web", "aws_s3_bucket.data", "aws_vpc.main"]
    resources_to_replace = [
        "aws_instance.web",
        "aws_s3_bucket.data",
        "aws_vpc.main",
        "aws_security_group.db",
    ]
    result = build_apply_command(resources_to_target, resources_to_replace)
    expected = [
        "terraform",
        "apply",
        "-target=aws_instance.web",
        "-target=aws_s3_bucket.data",
        "-target=aws_vpc.main",
        "-replace=aws_instance.web",
        "-replace=aws_s3_bucket.data",
        "-replace=aws_vpc.main",
        "-replace=aws_security_group.db",
    ]
    assert result == expected


def test_contains_resource_change_actions():
    assert contains_resource_change_actions(["create"]) is True
    assert contains_resource_change_actions(["update"]) is True
    assert contains_resource_change_actions(["delete"]) is True
    assert contains_resource_change_actions(["read"]) is False
