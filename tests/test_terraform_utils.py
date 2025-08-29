from terraform_champ.terraform_utils import build_apply_command


def test_build_apply_command():
    result = build_apply_command([], [])
    assert result == ["terraform", "apply"]

    result = build_apply_command(
        ["aws_instance.example"], ["aws_instance.example"]
    )
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
    resources_to_replace = ["aws_instance.web", "aws_s3_bucket.data", "aws_vpc.main", "aws_security_group.db"]
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