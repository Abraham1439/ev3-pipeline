pipeline {
    agent any
    environment {
        IMAGE_NAME = "ev3-vuln-app"
        CONTAINER_NAME = "ev3-vuln-app-container"
    }
    stages {
        stage('Build') {
            steps {
                echo 'Construyendo imagen Docker de la aplicación...'
                sh 'docker build -t $IMAGE_NAME ./app'
            }
        }
        stage('Test - Analisis Estatico (SAST)') {
            steps {
                echo 'Ejecutando Bandit (analisis estatico de seguridad)...'
                sh '''
                    pip3 install --quiet bandit || true
                    bandit -r app/ -f txt -o bandit-report.txt || true
                    cat bandit-report.txt
                '''
            }
        }
        stage('Test - Gestion de Dependencias') {
            steps {
                echo 'Auditando dependencias con pip-audit...'
                sh '''
                    pip3 install --quiet pip-audit || true
                    pip-audit -r app/requirements.txt || true
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker network create ev3-net || true
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME --network ev3-net -p 5000:5000 $IMAGE_NAME
                    sleep 5
                '''
            }
        }
        stage('Pruebas Dinamicas (OWASP ZAP)') {
            steps {
                sh '''
                    docker run --rm --network ev3-net -v $(pwd):/zap/wrk/:rw \
                      ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
                      -t http://$CONTAINER_NAME:5000 -r zap-report.html || true
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'bandit-report.txt, zap-report.html', allowEmptyArchive: true
        }
    }
}