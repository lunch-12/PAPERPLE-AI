 pipeline {
    agent any

    environment {
        REPO = 'lunch-12/PAPERPLE-AI'
        IMAGE_NAME = 'paperple-ai'
        ECR_ACCESS = 'ECR_Access'
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
                        try {
                            sh "docker rmi -f ${images}"
                        } catch (Exception e) {
                            sh 'docker stop run-test'
                            sh 'docker rm run-test'
                            sh "docker rmi -f ${images}"
                        }
                        echo "Deleted Docker images: ${images}"
                    } 
                    else {
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
        
        stage('Run Test Container') {
            steps {
                script {
                    sh "docker run -d --name run-test -p 8000:8000 ${IMAGE_NAME}:v0.0.${env.BUILD_NUMBER}"
                }
            }
        }
       
        stage('Call Health Check API') {
            steps {
                script {
                    def httpCode
                    def retry = true

                    while (retry) {
                        try {
                            httpCode = sh(script: 'curl -s -o /dev/null -w %{http_code} http://localhost:8000/health', returnStdout: true).trim()
                            retry = false
                            env.HTTP_CODE = httpCode
                        } catch (Exception e) {
                            echo "Error occurred: ${e.message}. Retrying"
                        }
                
                        sleep(5) 
                    }
                }
            }
        }        

        stage('Test Env Cleanup') {
            steps {
                script {
                    sh 'docker stop run-test'
                    sh 'docker rm run-test'
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    if(env.HTTP_CODE != '200'){
                        echo "${env.HTTP_CODE}"
                        error("Health Check Failure: ${env.HTTP_CODE}")
                    }
                }
            }
        }       
        
        stage('Push to ECR') {
            steps {
                script {
                    docker.withRegistry("https://024848437933.dkr.ecr.ap-northeast-2.amazonaws.com", "ecr:ap-northeast-2:${env.ECR_ACCESS}") {
                        docker.image("${env.IMAGE_NAME}:v0.0.${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }
      
        stage('Trigger CD Job') {
            steps {
                echo "IMAGE_TAG = v0.0.${env.BUILD_NUMBER}"
                build job: 'paperple-ai-cd', parameters: [string(name: 'IMAGE_TAG', value: "v0.0.${env.BUILD_NUMBER}")], 
                    wait: false
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
