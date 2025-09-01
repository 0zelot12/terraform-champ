from terraform_champ.terraform_utils import (
    build_apply_command,
    contains_resource_change_actions,
    parse_resources,
)


def test_parse_resources():
    with open("./tests/fixtures/test_plan.json", "r") as f:
        json_content = f.read()

    changed_resources = parse_resources(json_content, changed_only=True)
    assert changed_resources == [
        "docker_container.nginx",
        "local_file.json_example",
        "local_file.txt_example_2",
        "local_file.txt_example_3"
    ]
    
    filtered_resources = parse_resources(json_content, filter="nginx")
    assert filtered_resources == [
        "docker_container.nginx",
        "docker_image.nginx"
    ]
    
    changed_and_filtered_resources = parse_resources(json_content, changed_only=True, filter="nginx")
    assert changed_and_filtered_resources == ["docker_container.nginx"]
    
    resources = parse_resources(json_content)
    assert resources == [
        "docker_container.nginx",
        "docker_image.nginx",
        "local_file.json_example",
        "local_file.txt_example",
        "local_file.txt_example_2",
        "local_file.txt_example_3",
        "local_file.txt_example_4",
        "local_file.txt_example_5",
        "local_file.yaml_example"
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
