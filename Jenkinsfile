pipeline {
    agent any
    environment {
        VENV = 'wife-tester'
    }
    stages {
        stage('Remove Files') {
            steps {
                deleteDir()  // Wipes workspace before cloning
            }
        }
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'git-creds', url: 'https://github.com/KiranEaswar/TAMA-Core'
            }
        }
        stage('Create Testgrounds') {
            steps {
                sh "python3 -m venv $VENV"
            }
        }
        stage('Install Requirements') {
            steps {
                sh """
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt  # Rename to requirements.txt if needed
                """
            }
        }
        stage('Question My Wife') {
            steps {
                sh """
                    . $VENV/bin/activate
                    python3 core.py
                """
            }
        }
        stage('Clean Testground') {
            steps {  // Added missing steps block
                sh "rm -rf $VENV"
            }
        }
    }
}
