from terraform_champ.terraform_utils import build_apply_command

def test_build_apply_command():
    # Test with empty list
    result = build_apply_command([])
    assert result == ["terraform", "apply"]
    
    # Test with single resource
    result = build_apply_command(["aws_instance.example"])
    assert result == ["terraform", "apply", "-target=aws_instance.example"]
    
    # Test with multiple resources
    resources = ["aws_instance.web", "aws_s3_bucket.data", "aws_vpc.main"]
    result = build_apply_command(resources)
    expected = ["terraform", "apply", "-target=aws_instance.web", "-target=aws_s3_bucket.data", "-target=aws_vpc.main"]
    assert result == expected
