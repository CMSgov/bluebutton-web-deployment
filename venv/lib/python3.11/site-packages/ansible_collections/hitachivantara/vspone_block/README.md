# Hitachi Vantara VSP One Block Storage Modules for Red Hat® Ansible® 3.5.0

The Hitachi Vantara VSP One Block Storage Modules provide a comprehensive set of Ansible modules for managing Hitachi VSP One SDS Block and Hitachi VSP One series systems. These modules enable seamless integration with Red Hat Ansible, allowing users to automate storage provisioning, configuration, and management tasks.

## Hardware requirements

- VSP One SDS Block v1.17
- VSP One Block 20
- VSP One Block 24
- VSP One Block 26
- VSP One Block 28
- VSP 5100, 5500, 5100H, 5500H, 5200, 5600, 5200H, 5600H (SAS)
- VSP 5100, 5500, 5100H, 5500H, 5200, 5600, 5200H, 5600H (NVMe)
- VSP E590, E790, E990, E1090
- VSP F350, F370, F700, F800, F900, F1000, F1500
- VSP G350, G370, G700, G900, G1000, G1500

## Software requirements

- Red Hat Ansible Core - 2.16, 2.17, 2.18
- Python - 3.9 or higher

## Supported operating systems

- Oracle Enterprise Linux 8.9 or higher
- Red Hat Enterprise Linux 8.9 or higher

## Recommended Host configuration

- CPU/vCPU - 2
- Memory - 4 GB
- HardDisk - 30 GB

## Idempotence

- Idempotence is supported for this release

## Changelog

View the changelog [here](https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/CHANGELOG.rst).

## Available Modules

For a detailed list of available modules, please refer to the [Modules Documentation](https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/docs/MODULES.md).

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```bash
ansible-galaxy collection install hitachivantara.vspone_block
```

```text
collections:
    - hitachivantara.vspone_block.sds_block
```

```text
collections:
    - hitachivantara.vspone_block.vsp
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the Ansible package.

To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install hitachivantara.vspone_block --upgrade
```

If you need to install a specific version of the collection (for example, to downgrade due to issues in the latest version), you can use the following syntax to install version 3.5.0:

```bash
ansible-galaxy collection install hitachivantara.vspone_block:==3.5.0
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Troubleshooting

For troubleshooting tips and common issues, please refer to the [Troubleshooting Guide](https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/docs/TROUBLESHOOTING.md).

## Testing

This collection is tested using the official Ansible sanity tests to ensure compliance with Ansible coding standards and best practices.

## Support

For support, please use one of the following channels:

- [GitHub Issues](https://github.com/hitachi-vantara/vspone-block-ansible/issues) – for bug reports, feature requests, and technical assistance
- [Hitachi Vantara Support Portal](https://support.hitachivantara.com/) – for enterprise-grade support (requires valid support contract)
- Community discussion is welcome via GitHub or user forums

## Release Notes and Roadmap

### Release Notes

For User Guide and Release Notes, see [User Guide and Release Notes](https://docs.hitachivantara.com/search/all?query=ansible&value-filters=Option~%2522Red+Hat%2522*Product_custom~%2522Adapters+and+Drivers%2522&content-lang=en-US)

Version **3.5.0** highlights:

- General performance enhancements and bug fixes

### Roadmap

The following roadmap outlines upcoming features and improvements:

#### **Version 4.0** (Target: July 18, 2025)

- Initial storage system setup automation
- Remaining Pool Management features
- I/O performance optimization enhancements
- Support for remote replication failover workflows

#### **Version 4.1** (Target: August 15, 2025)

- Expansion of SDS Storage Cluster capabilities
- Support for user password reset operations
- Storage pool expansion features
- Initial support for SDS Block on AWS deployments

## License

[GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Author

*This collection was created by the Hitachi Vantara® Ansible Team in 2025.*
