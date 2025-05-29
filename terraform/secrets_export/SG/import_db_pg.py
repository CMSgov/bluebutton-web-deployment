import boto3
import json
import time

TARGET_VPC_ID = 'vpc-0f6c096a4a2265841'
REGION = 'us-east-1'
INPUT_FILE = 'source_vpc_vpc-9b3fc9fd_sgs_details.json'

ec2 = boto3.client('ec2', region_name=REGION)

with open(INPUT_FILE) as f:
    data = json.load(f)

security_groups = data.get('SecurityGroups', [])

def find_existing_sg(name, vpc_id):
    response = ec2.describe_security_groups(
        Filters=[
            {'Name': 'group-name', 'Values': [name]},
            {'Name': 'vpc-id', 'Values': [vpc_id]}
        ]
    )
    if response['SecurityGroups']:
        print(f'🔍 Found SG "{name}" in target VPC')
        return response['SecurityGroups'][0]
    else:
        print(f'❓ SG "{name}" not found in target VPC')
        return None

def authorize_ingress(group_id, permissions):
    try:
        ec2.authorize_security_group_ingress(GroupId=group_id, IpPermissions=permissions)
        print('  ➕ Ingress rules added')
    except ec2.exceptions.ClientError as e:
        if 'InvalidPermission.Duplicate' in str(e):
            print('  ℹ️ Ingress rules already exist, skipping duplicate')
        else:
            raise

def authorize_egress(group_id, permissions):
    try:
        ec2.authorize_security_group_egress(GroupId=group_id, IpPermissions=permissions)
        print('  ➕ Egress rules added')
    except ec2.exceptions.ClientError as e:
        if 'InvalidPermission.Duplicate' in str(e):
            print('  ℹ️ Egress rules already exist, skipping duplicate')
        else:
            raise

for sg in security_groups:
    if not isinstance(sg, dict):
        print(f"⚠️ Skipping invalid SG entry: {sg}")
        continue

    name = sg.get('GroupName', 'unnamed-sg')
    desc = sg.get('Description', 'no description')

    if name == 'default':
        print(f'⏭️ Skipping default SG: {name}')
        continue

    try:
        existing = find_existing_sg(name, TARGET_VPC_ID)
        if existing:
            print(f'🗑️ Deleting existing SG: {name} ({existing["GroupId"]})')
            try:
                ec2.delete_security_group(GroupId=existing['GroupId'])
                time.sleep(1)
            except Exception as e:
                print(f'❌ Could not delete SG "{name}": {e}')
                continue

        response = ec2.create_security_group(
            GroupName=name[:255],
            Description=desc,
            VpcId=TARGET_VPC_ID
        )
        new_sg_id = response['GroupId']
        print(f'✅ Recreated SG: {name} → {new_sg_id}')

        # Add Name tag explicitly
        ec2.create_tags(
            Resources=[new_sg_id],
            Tags=[{'Key': 'Name', 'Value': name}]
        )
        print(f'🏷️ Added Name tag: {name}')

        if sg.get('IpPermissions'):
            authorize_ingress(new_sg_id, sg['IpPermissions'])

        if sg.get('IpPermissionsEgress'):
            authorize_egress(new_sg_id, sg['IpPermissionsEgress'])

    except Exception as e:
        print(f'❌ Error recreating SG "{name}": {e}')
