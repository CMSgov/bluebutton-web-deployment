def private_key = 'dev-key'
def vault_pass = 'vault-pass'
def aws_creds = 'cbj-deploy'

pipeline {
  agent {
    node {
      label ''
      customWorkspace 'blue-button-deploy'
    }
  }

  parameters {
    string(
      defaultValue: "",
      description: 'The branch of the application repo to deploy. Required.',
      name: 'BRANCH'
    )
    string(
      defaultValue: "*/master",
      description: 'The branch of the deployment repo to use for deployment.',
      name: 'DEPLOY_BRANCH'
    )
    string(
      defaultValue: "",
      description: 'The Gold Image AMI id that will be used as the base for app servers.',
      name: 'AMI_ID'
    )
    string(
      defaultValue: "m3.medium",
      description: 'The class/size of the ec2 instance to launch.',
      name: 'INSTANCE_CLASS'
    )
    choice(
      choices: 'no\nyes',
      description: 'Should we run database migrations on deploy?',
      name: 'MIGRATE'
    )
    choice(
      choices: 'yes\nno',
      description: 'Should we run collectstatic on deploy?',
      name: 'COLLECT_STATIC'
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
    string(
      defaultValue: "",
      description: 'The CF platform version (e.g., "55"). Required when creating new servers.',
      name: 'CF_VERSION'
    )
    booleanParam(
      defaultValue: true,
      description: 'When true, we will only refresh code on existing servers, not create new ones.',
      name: 'REFRESH_ONLY'
    )
  }

  stages {
    stage('Ensure ENV and BRANCH') {
      steps {
        sh """
        if [ -z "${params.BRANCH}" ] || [ -z "${params.ENV}" ]
        then
          exit 1
        fi
        """
      }
    }

    stage('Ensure CF_VERSION and AMI_ID when REFRESH_ONLY is false') {
      steps {
        sh """
          if [ -z "${params.CF_VERSION}" ] || [ -z "${params.AMI_ID}" ]
          then
            exit 1
          fi
        """
      }
      when {
        expression {
          params.REFRESH_ONLY == false
        }
      }
    }

    stage('Notify HipChat') {
      steps {
        withCredentials([
          string(credentialsId: 'hipchat-room', variable: 'room'),
          string(credentialsId: 'hipchat-server', variable: 'server'),
          string(credentialsId: 'hipchat-token', variable: 'token')
        ]) {
          hipchatSend(
            color: 'GRAY',
            notify: true,
            message: "STARTED: ${env.JOB_NAME} [${params.ENV}]",
            room: room,
            sendAs: '',
            server: server,
            token: token,
            v2enabled: true
          )
        }
      }
    }

    stage('Install requirements') {
      steps {
        dir('code') {
          script {
            sh """
              virtualenv -ppython2.7 venv
              . venv/bin/activate

              pip install --upgrade pip
              pip install --upgrade cffi

              pip install ansible==2.4.2.0
              pip install boto
            """
          }
        }
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
            withAwsCli(credentialsId: aws_creds, defaultRegion: 'us-east-1') {
              withCredentials([
                file(credentialsId: private_key, variable: 'pk'),
                file(credentialsId: vault_pass, variable: 'vp')
              ]) {
                sh """
                  . venv/bin/activate

                  rm -Rf ./tmp

                  ansible-playbook playbook/appherd/100_create_appserver.yml  \
                    --vault-password-file ${vp} \
                    --private-key ${pk} \
                    -e 'env=${params.ENV}' \
                    -e 'cf_platform_version=${params.CF_VERSION}' \
                    -e 'azone=${params.AZ}' \
                    -e 'cf_app_instance_type=${params.INSTANCE_CLASS}' \
                    -e 'ami_app_gold_image=${params.AMI_ID}'
                """
              }
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
            withAwsCli(credentialsId: aws_creds, defaultRegion: 'us-east-1') {
              withCredentials([
                file(credentialsId: private_key, variable: 'pk'),
                file(credentialsId: vault_pass, variable: 'vp')
              ]) {
                sh """
                  . venv/bin/activate

                  rm -Rf ./tmp

                  EC2_INI_PATH=inventory/config/${params.ENV}.ini \
                  ansible-playbook playbook/appherd/200_build_appserver.yml  \
                    --vault-password-file ${vp} \
                    --private-key ${pk} \
                    -i inventory/ec2.py \
                    -l 'tag_State_appservers_base' \
                    -e 'env=${params.ENV}' \
                    -e 'collectstatic=${params.COLLECT_STATIC}' \
                    -e 'migrate=${params.MIGRATE}' \
                    -e 'git_branch=${params.BRANCH}' \
                    -e 'cf_platform_version=${params.CF_VERSION}' \
                    -e 'build_target=all'
                """
              }
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
            withAwsCli(credentialsId: aws_creds, defaultRegion: 'us-east-1') {
              withCredentials([
                file(credentialsId: private_key, variable: 'pk'),
                file(credentialsId: vault_pass, variable: 'vp')
              ]) {
                sh """
                  . venv/bin/activate

                  rm -Rf ./tmp

                  EC2_INI_PATH=inventory/config/${params.ENV}.ini \
                  ansible-playbook playbook/appherd/300_refresh_server_code.yml \
                    --vault-password-file ${vp} \
                    --private-key ${pk} \
                    -i inventory/ec2.py \
                    -l 'tag_Function_app_AppServer' \
                    -e 'env=${params.ENV}' \
                    -e 'collectstatic=${params.COLLECT_STATIC}' \
                    -e 'migrate=${params.MIGRATE}' \
                    -e 'git_branch=${params.BRANCH}' \
                    -e 'build_target=all'
                """
              }
            }
          }
        }
      }
      when {
        expression {
          params.REFRESH_ONLY == true
        }
      }
    }
  }

  post {
    success {
      withCredentials([
        string(credentialsId: 'hipchat-room', variable: 'room'),
        string(credentialsId: 'hipchat-server', variable: 'server'),
        string(credentialsId: 'hipchat-token', variable: 'token')
      ]) {
        hipchatSend(
            color: 'GREEN',
            notify: true,
            message: "SUCCESS: ${env.JOB_NAME} [${params.ENV}]",
            room: room,
            sendAs: '',
            server: server,
            token: token,
            v2enabled: true
        )
      }
    }

    failure {
      withCredentials([
        string(credentialsId: 'hipchat-room', variable: 'room'),
        string(credentialsId: 'hipchat-server', variable: 'server'),
        string(credentialsId: 'hipchat-token', variable: 'token')
      ]) {
        hipchatSend(
          color: 'RED',
          notify: true,
          message: "FAILED: ${env.JOB_NAME} [${params.ENV}]",
          room: room,
          sendAs: '',
          server: server,
          token: token,
          v2enabled: true
        )
      }
    }
  }
}
