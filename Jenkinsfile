pipeline {
    agent any
    
    environment {
        // Docker Hub credentials (configure in Jenkins)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        
        // Docker image details
        DOCKER_IMAGE = 'thestreets6c/cyber-def25-malware-detection'
        IMAGE_TAG = "${BUILD_NUMBER}"
        LATEST_TAG = 'latest'
        
        // Project configuration
        PROJECT_DIR = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Verify Files') {
            steps {
                echo 'Verifying required files exist...'
                script {
                    // Check if required files exist
                    def requiredFiles = [
                        'Dockerfile',
                        'docker-compose.yml',
                        'inference.py',
                        'requirements.txt',
                        'model.pkl'
                    ]
                    
                    requiredFiles.each { file ->
                        if (!fileExists(file)) {
                            error("Required file missing: ${file}")
                        }
                    }
                    echo 'All required files present'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    // Build the Docker image
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                        docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:${LATEST_TAG}
                    """
                }
                echo "Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }
        
        stage('Test Docker Image') {
            steps {
                echo 'Testing Docker image...'
                script {
                    // Verify the image was created
                    sh "docker images ${DOCKER_IMAGE}"
                    
                    // Optional: Run a quick test
                    sh """
                        docker run --rm ${DOCKER_IMAGE}:${IMAGE_TAG} python -c 'import sys; print(sys.version)'
                    """
                }
                echo 'Docker image test completed'
            }
        }
        
        stage('Login to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub...'
                script {
                    // Login to Docker Hub
                    sh """
                        echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin
                    """
                }
                echo 'Successfully logged in to Docker Hub'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                script {
                    // Push both tags to Docker Hub
                    sh """
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:${LATEST_TAG}
                    """
                }
                echo "Image pushed to Docker Hub: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }
        
        stage('Run Container') {
            steps {
                echo 'Running container with Docker Run...'
                script {
                    // 1. Force remove any old container with the same name
                    sh "docker rm -f malware-app || true"

                    // 2. Ensure directories exist
                    sh "mkdir -p ${PROJECT_DIR}/output"
                    // (Optional) If your repo doesn't have this folder, we create it so the mount doesn't fail
                    sh "mkdir -p ${PROJECT_DIR}/network_logs"

                    // 3. Run the container
                    // -v maps your workspace folders to the container
                    // --rm means "delete the container when finished"
                    sh """
                        docker run --name malware-app \\
                        -v ${PROJECT_DIR}/network_logs:/input/logs \\
                        -v ${PROJECT_DIR}/output:/output \\
                        ${DOCKER_IMAGE}:${IMAGE_TAG}
                    """
                }
                echo 'Container execution completed'
            }
        }
        
        stage('Verify Output') {
            steps {
                echo 'Verifying output files...'
                script {
                    // Check if alerts.csv was created
                    if (fileExists('output/alerts.csv')) {
                        echo 'Output file created successfully: output/alerts.csv'
                        
                        // Display output file content
                        sh 'cat output/alerts.csv'
                    } else {
                        echo 'Warning: Output file not found'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            script {
                // Logout from Docker Hub
                sh 'docker logout || true'
                
                // Remove the container if it's still there
                sh 'docker rm -f malware-app || true'
            }
        }
        
        success {
            echo 'Pipeline completed successfully!'
            echo "Docker image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            echo 'Image available on Docker Hub'
        }
        
        failure {
            echo 'Pipeline failed! Please check the logs.'
        }
    }
}
