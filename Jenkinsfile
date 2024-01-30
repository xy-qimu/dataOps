pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                echo '拉取代码'
            }
        }
        stage('构建') {
            steps {
                echo '构建打包测试'
            }
        }
        stage('部署') {
            steps {
                echo '部署上传到生产'
            }
        }
    }
}
