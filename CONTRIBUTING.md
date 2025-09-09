# How to Contribute
We're so thankful you're considering contributing to an [open source project of
the U.S. government](https://code.gov/)! If you're unsure about anything, just
ask -- or submit the issue or pull request anyway. The worst that can happen is
you'll be politely asked to change something. We appreciate all friendly
contributions.

We encourage you to read this project's CONTRIBUTING policy (you are here), its
[LICENSE](LICENSE.md), and its [README](README.md).

## Getting Started
If you're new to the project, look for issues labeled with `good-first-issue` or `help-wanted` to get started. These are typically easier problems that don't require deep knowledge of the codebase.

## Team Specific Guidelines
The Blue Button Web Server project is maintained by the CMS team and welcomes contributions from external developers. Please review our [COMMUNITY.md](COMMUNITY.md) file for details on team structure, roles, and responsibilities. All contributors should be familiar with OAuth2, FHIR standards, and Django development practices.

## Building Dependencies
Please refer to the [README](README.md#installation)

## Building the Project
Please refer to the [README](README.md#installation)

## Workflow and Branching
We follow standard GitHub Flow practices:

1. **Fork the project** (external contributors) or create a branch (internal contributors)
2. **Check out the `main` branch**
3. **Create a feature branch** with a descriptive name
4. **Write code and tests** for your change
5. **From your branch, make a pull request** against `CMSgov/bluebutton-web-deployment/main`
6. **Work with repo maintainers** to get your change reviewed
7. **Wait for your change to be merged** into `main`
8. **Delete your feature branch** after successful merge

## Coding Style and Linters

**Style Guidelines:**
- Write clear, self-documenting code with appropriate comments

**Linting:**
- Each application has its own linting guidelines

## Writing Issues

When creating an issue, please use this format:

```
module-name: One line summary of the issue (less than 72 characters)

### Expected behavior

As concisely as possible, describe the expected behavior.

### Actual behavior

As concisely as possible, describe the observed behavior.

### Steps to reproduce the behavior

1. List all relevant steps to reproduce the observed behavior
2. Include specific API calls, user actions, or configuration
3. Mention any relevant environment details

### Additional context

- Node version
- Operating system
- Any relevant logs or error messages
```

## Writing Pull Requests
**Pull Request Guidelines:**
- File pull requests against the `main` branch
- Include a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Include screenshots for UI changes

## Documentation

We welcome improvements to the project documentation. This includes:

- API documentation updates
- Setup and configuration guides
- Developer tutorials
- Code comments and inline documentation

Please file an [issue](https://github.com/CMSGov/bluebutton-web-deployment/issues) for documentation improvements or submit a pull request with your changes.

**Documentation Resources:**
- Developer documentation: https://cmsgov.github.io/bluebutton-developer-help/
- Current deployment: https://sandbox.bluebutton.cms.gov
- Community discussions: https://groups.google.com/forum/#!forum/developer-group-for-cms-blue-button-api

## Policies

### Open Source Policy
We adhere to the [CMS Open Source
Policy](https://github.com/CMSGov/cms-open-source-policy). If you have any
questions, just [shoot us an email](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy
_Submit a vulnerability:_ Vulnerability reports can be submitted through [Bugcrowd](https://bugcrowd.com/cms-vdp). Reports may be submitted anonymously. If you share contact information, we will acknowledge receipt of your report within 3 business days.

For more information about our Security, Vulnerability, and Responsible Disclosure Policies, see [SECURITY.md](SECURITY.md).

## Public domain
This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.