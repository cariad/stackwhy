# stackwhy

**stackwhy** is a CLI tool and Python package for visualising the most recent events on an Amazon Web Services CloudFormation stack.

For example:

```text
Logical ID           Physical ID          Resource Type               Status                                        Reason
StormyNightDeployer                       AWS::CloudFormation::Stack  UPDATE_IN_PROGRESS                            User Initiated
Deployer             StormyNightDeployer  AWS::IAM::User              UPDATE_IN_PROGRESS
HostedZone                                AWS::Route53::HostedZone    CREATE_IN_PROGRESS
Deployer             StormyNightDeployer  AWS::IAM::User              UPDATE_FAILED                                 API: iam:PutUserPolicy User:
                                                                                                                    arn:aws:iam::807041577214:user/StormyNightDeployer is not
                                                                                                                    authorized to perform: iam:PutUserPolicy on resource: user
                                                                                                                    StormyNightDeployer
HostedZone                                AWS::Route53::HostedZone    CREATE_FAILED                                 Resource handler returned message: "User:
                                                                                                                    arn:aws:iam::807041577214:user/StormyNightDeployer is not
                                                                                                                    authorized to perform: route53:CreateHostedZone (Service:
                                                                                                                    Route53, Status Code: 403, Request ID:
                                                                                                                    a21eaab2-9938-4e08-ad65-b3902509252e, Extended Request ID:
                                                                                                                    null)" (RequestToken: 03e18708-8649-fcec-3f7b-329aae06a1c5,
                                                                                                                    HandlerErrorCode: GeneralServiceException)
StormyNightDeployer                       AWS::CloudFormation::Stack  UPDATE_ROLLBACK_IN_PROGRESS                   The following resource(s) failed to create: [HostedZone].
                                                                                                                    The following resource(s) failed to update: [Deployer].
Deployer             StormyNightDeployer  AWS::IAM::User              UPDATE_COMPLETE
StormyNightDeployer                       AWS::CloudFormation::Stack  UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS
HostedZone                                AWS::Route53::HostedZone    DELETE_COMPLETE
StormyNightDeployer                       AWS::CloudFormation::Stack  UPDATE_ROLLBACK_COMPLETE
```

The full documentation is online at [cariad.github.io/stackwhy](https://cariad.github.io/stackwhy).

## Installation

`stackwhy` requires Python 3.8 or later.

```bash
pip install stackwhy
```

## 👋 Hello!

**Hello!** I'm [Cariad Eccleston](https://cariad.io) and I'm an independent/freelance software engineer. If my work has value to you, please consider [sponsoring](https://github.com/sponsors/cariad/).

If you ever raise a bug, request a feature or ask a question then mention that you're a sponsor and I'll respond as a priority. Thank you!
