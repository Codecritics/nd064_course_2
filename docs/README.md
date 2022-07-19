# UdaConnect
## Usage
### Setup
To launch the project first position yourself at root path:
 1. `kubectl apply -f k8s`
 2. `shell scripts/run_db_command.sh (pod of postgres)`
 3. `helm repo add bitnami https://charts.bitnami.com/bitnami`
 4. `helm install kafka-release bitnami/kafka -f kafka-values.yml`
 5. `k apply -f modules/frontend/k8s`
 6. `k apply -f modules/person-service/k8s`
 7. `k apply -f modules/location-service/k8s`
 8. `k apply -f modules/location-grpc/k8s`
 9. `k apply -f modules/kafka-service/k8s`
 10. `k apply -f modules/location-connection/k8s`

