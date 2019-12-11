#!/usr/bin/env node
import cdk = require('@aws-cdk/core');
import { FargateStack } from '../lib/stack';

const app = new cdk.App();
new FargateStack(app, 'selfie2anime-stack', {
    env: {
        region: 'ap-southeast-2'
    }
});