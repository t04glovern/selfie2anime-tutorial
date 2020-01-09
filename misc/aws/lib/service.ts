import ecs = require('@aws-cdk/aws-ecs');
import ecr = require('@aws-cdk/aws-ecr');
import cdk = require('@aws-cdk/core');
import elbv2 = require('@aws-cdk/aws-elasticloadbalancingv2');
import { Duration } from '@aws-cdk/core';


// Interface for public Fargate Service
export interface IFargateService {
  cluster: ecs.Cluster;
  serviceName: string;
  lightModel: string;
  logPrefix: string;
  port: number;
  containerPort: number;
}

export class FargateService extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string, props: IFargateService) {
    super(scope, id);

    // Create an Application Load Balancer
    const alb = new elbv2.ApplicationLoadBalancer(this, 'alb', {
      vpc: props.cluster.vpc,
      internetFacing: true
    });
    const tg = new elbv2.ApplicationTargetGroup(this, 'default', {
      vpc: props.cluster.vpc,
      port: props.port,
      targetType: elbv2.TargetType.INSTANCE,
      healthCheck: {
        path: '/health',
        port: props.containerPort.toString(),
        protocol: elbv2.Protocol.HTTP,
        interval: Duration.seconds(60),
        timeout: Duration.seconds(5)
      }
    });
    const listener = alb.addListener('listener', {
      port: props.port
    });
    listener.addTargetGroups('tg', {
      targetGroups: [tg]
    });

    // create a task definition with CloudWatch Logs
    const logging = new ecs.AwsLogDriver({
      streamPrefix: props.logPrefix
    });

    // Define Task Def
    const fargateTaskDefinition = new ecs.Ec2TaskDefinition(this, 'taskdef');

    // Import repository
    const repo = ecr.Repository.fromRepositoryName(this, 'repository', `${props.serviceName}-api`)

    // Associate container to task def
    fargateTaskDefinition
      .addContainer('container', {
        image: ecs.ContainerImage.fromEcrRepository(repo),
        memoryReservationMiB: 4096,
        memoryLimitMiB: 8192,
        cpu: 1024,
        logging,
        entryPoint: [
          'python3'
        ],
        command: [
          'main.py',
          '--dataset',
          `${props.serviceName}`,
          '--phase',
          'web',
          '--light',
          `${props.lightModel}`
        ],
        workingDirectory: '/app',
        environment: {
          'PYTHONUNBUFFERED': '1'
        }
      })
      .addPortMappings({
        containerPort: props.containerPort,
        hostPort: props.containerPort,
        protocol: ecs.Protocol.TCP
      });

    // Grant fargate permission to repository
    repo.grantPull(fargateTaskDefinition.taskRole)

    // Create service
    const service = new ecs.Ec2Service(this, 'service', {
      cluster: props.cluster,
      taskDefinition: fargateTaskDefinition,
      desiredCount: 1,
      serviceName: props.serviceName
    });
    tg.addTarget(service);

    // Output the DNS where you can access your service
    // tslint:disable-next-line: no-unused-expression
    new cdk.CfnOutput(this, 'albDns', {
      value: alb.loadBalancerDnsName
    });
  }
}
