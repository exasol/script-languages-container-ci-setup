import click

aws_options = [
    click.option('--aws-profile', required=True, type=str,
                 help="Id of the AWS profile to use."),
]
