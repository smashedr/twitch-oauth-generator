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
        DEV_PORT = '10184'
        PROD_PORT = '10185'
        DISCORD_ID = "smashed-alerts"
        COMPOSE_FILE = "docker-compose-swarm.yml"

        BUILD_CAUSE = getBuildCause()
        VERSION = getVersion("${GIT_BRANCH}")
        GIT_ORG = getGitGroup("${GIT_URL}")
        GIT_REPO = getGitRepo("${GIT_URL}")

        BASE_NAME = "${GIT_ORG}-${GIT_REPO}"
        SERVICE_NAME = "${BASE_NAME}"
        NFS_HOST = "nfs01.cssnr.com"
    }
    stages {
        stage('Init') {
            steps {
                echo "\n--- Build Details ---\n" +
                        "GIT_URL:       ${GIT_URL}\n" +
                        "JOB_NAME:      ${JOB_NAME}\n" +
                        "SERVICE_NAME:  ${SERVICE_NAME}\n" +
                        "BASE_NAME:     ${BASE_NAME}\n" +
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
                ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/dev.env"
                STACK_NAME = "dev_${BASE_NAME}"
                DOCKER_PORT = "${DEV_PORT}"
                NFS_DIRECTORY = "${STACK_NAME}"
            }
            steps {
                echo "\n--- Starting Dev Deploy ---\n" +
                        "ENV_FILE:      ${ENV_FILE}\n" +
                        "STACK_NAME:    ${STACK_NAME}\n" +
                        "DOCKER_PORT:   ${DOCKER_PORT}\n"
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
                ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/prod.env"
                STACK_NAME = "prod_${BASE_NAME}"
                DOCKER_PORT = "${PROD_PORT}"
                NFS_DIRECTORY = "${STACK_NAME}"
            }
            steps {
                echo "\n--- Starting Prod Deploy ---\n" +
                        "ENV_FILE:      ${ENV_FILE}\n" +
                        "STACK_NAME:    ${STACK_NAME}\n" +
                        "DOCKER_PORT:   ${DOCKER_PORT}\n"
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
