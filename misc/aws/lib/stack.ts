import cdk = require('@aws-cdk/core');
import ec2 = require('@aws-cdk/aws-ec2');
import { SubnetType } from '@aws-cdk/aws-ec2';

import { FargateCluster } from "./cluster";

export class FargateStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const modelName = this.node.tryGetContext('modelName');
    const modelLight = this.node.tryGetContext('modelLight');

    // VPC Configuration
    const vpc = new ec2.Vpc(this, 'vpc', {
      cidr: '10.160.0.0/16',
      maxAzs: 2,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'Ingress',
          subnetType: SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'Application',
          subnetType: SubnetType.PRIVATE,
        },
        {
          cidrMask: 28,
          name: 'Database',
          subnetType: SubnetType.ISOLATED,
        }
      ],
    });

    const cluster = new FargateCluster(this, "cluster", {
      name: 'cdk-model-cluster',
      modelName,
      modelLight,
      vpc: vpc
    })
  }
}
