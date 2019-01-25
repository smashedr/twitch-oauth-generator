#!/usr/bin/env groovy

@Library('jenkins-libraries')_

pipeline {
    agent {
        label 'manager'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'5'))
        timeout(time: 1, unit: 'HOURS')
    }
    environment {
        env.DEV_PORT = '10184'
        env.PROD_PORT = '10185'
        env.DISCORD_ID = "smashed-alerts"
        env.COMPOSE_FILE = "docker-compose-swarm.yml"

        env.BUILD_CAUSE = getBuildCause()
        env.VERSION = getVersion("${GIT_BRANCH}")
        env.GIT_ORG = getGitGroup("${GIT_URL}")
        env.GIT_REPO = getGitRepo("${GIT_URL}")

        env.STACK_NAME = "${GIT_ORG}-${GIT_REPO}"
        env.SERVICE_NAME = "${STACK_NAME}"
    }
    stages {
        stage('Init') {
            steps {
                echo "\n--- Build Details ---\n" +
                        "GIT_URL:       ${GIT_URL}\n" +
                        "JOB_NAME:      ${JOB_NAME}\n" +
                        "SERVICE_NAME:  ${SERVICE_NAME}\n" +
                        "STACK_NAME:    ${STACK_NAME}\n" +
                        "BUILD_CAUSE:   ${BUILD_CAUSE}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "VERSION:       ${VERSION}\n"
                verifyBuild()
                sendDiscord("${DISCORD_ID}", "Pipeline Started by: ${BUILD_CAUSE}")
                getConfigs("${SERVICE_NAME}")   // remove this if you do not need config files
            }
        }
        stage('Dev Deploy') {
            when {
                allOf {
                    not { branch 'master' }
                }
            }
            environment {
                env.ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/dev.env"
                env.STACK_NAME = "dev_${STACK_NAME}"
                env.DOCKER_PORT = "${DEV_PORT}"
            }
            steps {
                echo "Starting Dev Deploy..."
                sendDiscord("${DISCORD_ID}", "Dev Deploy Started")
                setupNfs("${STACK_NAME}")       // remove this if you do not need nfs volumes
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
                sendDiscord("${DISCORD_ID}", "Dev Deploy Finished")
            }
        }
        stage('Prod Deploy') {
            when {
                allOf {
                    branch 'master'
                    triggeredBy 'UserIdCause'
                }
            }
            environment {
                env.ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/prod.env"
                env.STACK_NAME = "prod_${STACK_NAME}"
                env.DOCKER_PORT = "${PROD_PORT}"
            }
            steps {
                echo "Starting Prod Deploy..."
                sendDiscord("${DISCORD_ID}", "Prod Deploy Started")
                setupNfs("${STACK_NAME}")       // remove this if you do not need nfs volumes
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
                sendDiscord("${DISCORD_ID}", "Prod Deploy Finished")
            }
        }
    }
    post {
        always {
            cleanWs()
            script { if (!env.INVALID_BUILD) {
                sendDiscord("${DISCORD_ID}", "Pipeline Complete: ${currentBuild.currentResult}")
            } }
        }
    }
}
