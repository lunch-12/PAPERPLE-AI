 pipeline {
    agent any

    environment {
        REPO = 'lunch-12/PAPERPLE-AI'
        IMAGE_NAME = 'hnnynh/paperple-ai'
        DOCKER_CREDENTIALS_ID = 'dockerhub'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "https://github.com/${REPO}.git"
            }
        }
        
        stage('Remove Previous Docker Image') {
            steps {
                script {
                    def images = sh(script: "docker images -q '${IMAGE_NAME}'", returnStdout: true).trim()

                    if (images) {
                        sh "docker rmi -f ${images} || true"
                        echo "Deleted Docker images: ${images}"
                    } else {
                        echo "No Docker images found with name: ${IMAGE_NAME}"
                    }
                }
            }
        }
            
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}:v0.0.${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        dockerImage.push("v0.0.${env.BUILD_NUMBER}")
                    }
                }
            }
        }
    }
    
    post {
        success {
            slackSend (
                channel: '#클라우드', 
                color: '#00FF00', 
                message: "BUILD SUCCESS: ${REPO} BUILD Job ${env.JOB_NAME} [${env.BUILD_NUMBER}]"
            )
        }
        failure {
            slackSend (
                channel: '#클라우드', 
                color: '#FF0000', 
                message: "BUILD FAIL: ${REPO} BUILD Job ${env.JOB_NAME} [${env.BUILD_NUMBER}]"
            )
        }
    }
}