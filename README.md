# Headbang

## TODO
- [x] FastAPI Spotify API Auth
- [ ] Docker Compose
- [ ] Kafka
- [ ] PostgreSQL
- [ ] Spotify Liked Songs Kafka Producer
- [ ] Spotify Liked Songs Kafka Consumer

## Setup

### API local
```bash
pyenv install 3.12
pyenv virtualenv 3.12 headbangv2
pip install --upgrade pip
pip install -r api/requirements.txt
curl http://localhost:8080/login
```

### API Docker
```bash
cd api/
docker build -t headbang .
docker run -d --name headbang-api -p 8080:8080 headbang
```

### Terraform
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform init
terraform apply -auto-approve
```

### K8 Kind
```bash
brew install lima
go install sigs.k8s.io/kind@v0.26.0
kind create cluster
```

### k8 Kafka
```bash
kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl get pod -n kafka --watch
kubectl apply -f https://strimzi.io/examples/latest/kafka/kraft/kafka-single-node.yaml -n kafka
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```
