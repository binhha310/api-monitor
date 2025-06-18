pipeline {
    agent any
    options {
        skipDefaultCheckout()
    }

    environment {
        IMAGE_REPO = 'binhha310/apimonitor'
        BACKEND_CHART_PATH = 'charts/api-monitor-backend'
        VERSION_TAG = "${BUILD_NUMBER}"
        GIT_CRED_ID = 'git-creds'
    }

    parameters {
        string(name:'GIT_URL', defaultValue:'https://github.com/binhha310/api-monitor.git', description:'The URL of the source Git repository to use.')
        string(name:'GIT_BRANCH', defaultValue:'main', description:'The branch in the source Git repository to use.')
    }

    stages {
        stage('Checkout') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-creds-id', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    checkout([
                    $class: 'GitSCM',
                    branches: [[name: params.GIT_BRANCH]],
                    userRemoteConfigs: [[
                        url: "https://${GIT_USER}:${GIT_TOKEN}@${params.GIT_URL.replace('https://', '')}"
                    ]]
                ])
                }
                stash name: 'sources', includes: '**', excludes: '**/.git,**/.git/**'
            }
        }
        stage('Build docker') {
            agent {
                label 'docker-build'
            }
            steps {
                unstash 'sources'
                container(name: 'kaniko') {
                    sh '/kaniko/executor --context=`pwd` --dockerfile=`pwd`/Dockerfile.backend  --destination=binhha310/apimonitor:${VERSION_TAG}'
                }
            }
        }
        stage('Update GitOps Repo') {
            steps {
                unstash 'sources'
                withCredentials([usernamePassword(credentialsId: 'git-pat', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git config --global user.email "ci@example.com"
                        git config --global user.name "Jenkins CI"

                        # Update image tag
                        sed -i "s|tag:.*|tag: \\"$VERSION_TAG\\"|" ${BACKEND_CHART_PATH}/values.yaml

                        git add ${BACKEND_CHART_PATH}/values.yaml
                        git commit -m "Update image tag to $VERSION_TAG"

                        # Push using HTTPS + token auth
                        git push https://${GIT_USER}:${GIT_TOKEN}@${params.GIT_URL.replace('https://', '')} HEAD:main
                    '''
                }
            }
        }
    }
}
