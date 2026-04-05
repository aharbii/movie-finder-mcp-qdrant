// =============================================================================
// movie-finder-mcp-qdrant — Jenkins declarative pipeline
//
// Pipeline modes (Jenkins Multibranch Pipeline):
//   PR build       — every pull request: Lint + Typecheck + Test
//   Main build     — push to main: Lint + Typecheck + Test
//
// Required Jenkins plugins: JUnit, Coverage
// =============================================================================

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds(abortPrevious: true)
    }

    environment {
        // Ensure uv is available in the Jenkins agent's PATH if installed locally
        PATH = "$HOME/.local/bin:$PATH"
    }

    stages {

        // ------------------------------------------------------------------ //
        stage('Initialize') {
            steps {
                script {
                    // Install uv if it is not already available on the Jenkins agent
                    sh '''
                        if ! command -v uv &> /dev/null; then
                            curl -LsSf https://astral.sh/uv/install.sh | sh
                        fi
                    '''
                }
                sh 'make init'
            }
        }

        // ------------------------------------------------------------------ //
        stage('Lint + Typecheck') {
            parallel {
                stage('Lint') {
                    steps { sh 'make lint' }
                }
                stage('Typecheck') {
                    steps { sh 'make typecheck' }
                }
            }
        }

        // ------------------------------------------------------------------ //
        stage('Test') {
            steps {
                sh 'make test-coverage'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'junit.xml'
                    recordCoverage(
                        tools: [
                            [parser: 'COBERTURA', pattern: 'coverage.xml']
                        ],
                        id: 'coverage',
                        name: 'MCP Coverage',
                        sourceCodeRetention: 'EVERY_BUILD',
                        failOnError: false,
                        qualityGates: [
                            [threshold: 80.0, metric: 'LINE', baseline: 'PROJECT'],
                            [threshold: 80.0, metric: 'BRANCH', baseline: 'PROJECT']
                        ]
                    )
                }
            }
        }

    }

    post {
        always {
            sh 'make clean || true'
            cleanWs()
        }
        failure {
            echo "Pipeline failed on ${env.BRANCH_NAME ?: 'manual trigger'} — check logs above."
        }
        success {
            echo "Pipeline completed successfully."
        }
    }
}
