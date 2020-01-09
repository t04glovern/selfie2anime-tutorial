import ecs = require('@aws-cdk/aws-ecs');
import cdk = require('@aws-cdk/core');
import { Vpc, InstanceType } from '@aws-cdk/aws-ec2';

import { FargateService } from './service';

// Interface for Fargate Cluster
export interface IFargateCluster {
  name: string;
  modelName: string;
  modelLight: string;
  vpc: Vpc;
}

export class FargateCluster extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string, props: IFargateCluster) {
    super(scope, id);

    // Create an ECS cluster
    const cluster = new ecs.Cluster(this, props.name, {
      vpc: props.vpc,
      clusterName: props.name,
      capacity: {
        instanceType: new InstanceType('r5a.large'),
        desiredCapacity: 1,
        maxCapacity: 2,
        minCapacity: 1,
        spotPrice: '0.0379',
        spotInstanceDraining: true
      }
    });

    // Create a new model fargate service
    const model_service = new FargateService(this, 'cdk-model-api', {
      cluster,
      serviceName: props.modelName,
      lightModel: props.modelLight,
      logPrefix: 'fargate/' + cdk.Aws.STACK_NAME,
      port: 80,
      containerPort: 5000
    });
  }
}
