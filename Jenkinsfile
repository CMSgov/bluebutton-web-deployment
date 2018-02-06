def private_key = 'dev-key'
def vault_pass = 'vault-pass'

pipeline {
  agent any

  parameters {
    string(
      defaultValue: "",
      description: 'The branch of the application repo to deploy. Required.',
      name: 'BRANCH'
    )
    string(
      defaultValue: "",
      description: 'The CF platform version.',
      name: 'CF_VERSION'
    )
    string(
      defaultValue: "*/master",
      description: 'The branch of the deployment repo to use for deployment.',
      name: 'DEPLOY_BRANCH'
    )
    choice(
      choices: 'no\nyes',
      description: 'Should we run database migrations on deploy?',
      name: 'MIGRATE'
    )
    choice(
      choices: 'dev\ntest\nimpl\nprod',
      description: 'The environment to deploy to. Required.',
      name: 'ENV'
    )
    choice(
      choices: 'az1\naz2\naz3',
      description: 'Availability zone to launch instance in.',
      name: 'AZ'
    )
    booleanParam(
      defaultValue: true,
      description: 'When true, we will only refresh code on existing servers, not create new ones.',
      name: 'REFRESH_ONLY'
    )
  }

  stages {
    stage('Ensure ENV, BRANCH and CF_VERSION') {
      steps {
        sh """
        if [ -z "$BRANCH" ] || [ -z "$CF_VERSION" ] || [ -z "$ENV" ]
        then
          exit 1
        fi
        """
      }
    }

    stage('Set private key file') {
      steps {
        script {
            private_key = 'prod-key'
        }
      }
      when {
        expression {
          params.ENV == "prod"
        }
      }
    }

    stage('Checkout') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[
            name: "${params.DEPLOY_BRANCH}"
          ]],
          doGenerateSubmoduleConfigurations: false,
          extensions: [[
            $class: 'RelativeTargetDirectory',
            relativeTargetDir: 'code'
          ]],
          userRemoteConfigs: [[
            url: 'https://github.com/CMSgov/bluebutton-web-deployment.git'
          ]]
        ])
      }
    }

    stage('Create app server') {
      steps {
        script {
          dir('code') {
            withCredentials([
              file(credentialsId: private_key, variable: 'pk'),
              file(credentialsId: vault_pass, variable: 'vp')
            ]) {
              sh """
                ansible-playbook playbook/appherd/100_create_appserver.yml  \
                  --vault-password-file ${vp} \
                  --private-key ${pk} \
                  -e 'env=${params.ENV}' \
                  -e 'cf_platform_version=${params.CF_VERSION}' \
                  -e 'azone=${params.AZ}'
              """
            }
          }
        }
      }
      when {
        expression {
          params.REFRESH_ONLY == false
        }
      }
    }

    stage('Add volumes') {
      steps {
        script {
          dir('code') {
            withCredentials([
              file(credentialsId: private_key, variable: 'pk'),
              file(credentialsId: vault_pass, variable: 'vp')
            ]) {
              sh """
                ansible-playbook playbook/appherd/140_add_volumes.yml  \
                  --vault-password-file ${vp} \
                  --private-key ${pk} \
                  -e 'env=${params.ENV}' \
                  -e 'cf_platform_version=${params.CF_VERSION}' \
                  -e 'azone=${params.AZ}' \
                  -e 'build_target=appservers-base'
              """
            }
          }
        }
      }
      when {
        expression {
          params.REFRESH_ONLY == false
        }
      }
    }

    stage('Build app server') {
      steps {
        script {
          dir('code') {
            withCredentials([
              file(credentialsId: private_key, variable: 'pk'),
              file(credentialsId: vault_pass, variable: 'vp')
            ]) {
              sh """
                ansible-playbook playbook/appherd/200_build_appserver.yml  \
                  --vault-password-file ${vp} \
                  --private-key ${pk} \
                  -e 'env=${params.ENV}' \
                  -e 'build_target=appservers-base' \
                  -e 'collectstatic=yes' \
                  -e 'add_groups=no' \
                  -e 'add_scopes=no' \
                  -e 'migrate=no' \
                  -e 'git_branch=${params.BRANCH}' \
                  -e 'cf_platform_version=${params.CF_VERSION}'
              """
            }
          }
        }
      }
      when {
        expression {
          params.REFRESH_ONLY == false
        }
      }
    }

    stage('Deploy/refresh code') {
      steps {
        script {
          dir('code') {
            withCredentials([
              file(credentialsId: private_key, variable: 'pk'),
              file(credentialsId: vault_pass, variable: 'vp')
            ]) {
              sh """
                ansible-playbook playbook/appherd/300_refresh_server_code.yml \
                  --vault-password-file ${vp} \
                  --private-key ${pk} \
                  -e 'env=${params.ENV}' \
                  -e 'build_target=appservers' \
                  -e 'collectstatic=yes' \
                  -e 'add_groups=no' \
                  -e 'add_scopes=no' \
                  -e 'migrate=${params.MIGRATE}' \
                  -e 'git_branch=${params.BRANCH}'
              """
            }
          }
        }
      }
    }
  }
}
