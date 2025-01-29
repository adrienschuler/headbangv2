# Headbang

## TODO
- [ ] Spotify Liked Songs Dataset


```
brew install lima
go install sigs.k8s.io/kind@v0.26.0
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform init
terraform apply -auto-approve

kind create cluster
kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl get pod -n kafka --watch
kubectl apply -f https://strimzi.io/examples/latest/kafka/kraft/kafka-single-node.yaml -n kafka
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka

cd api/
docker build -t headbang .
docker run -d --name headbang-api -p 8080:8080 headbang
curl http://localhost:8080/login
```
