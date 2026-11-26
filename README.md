# weather-ml-app
DevOps Group Coursework – Flask Weather ML Application

## Repository layout

| Path | What it is |
|---|---|
| `app.py`, `templates/`, `model/model.pkl` | Flask app, HTML templates and trained model |
| `tests/` | Task 2 tests: `smoke_test.py`, `unit_test.py`, `integration_test.py` |
| `Dockerfile`, `requirements.txt`, `VERSION` | Container image; `VERSION` sets the image tag (v1, v2, ...) |
| `ansible/` | Task 3 playbooks (kubectl, minikube, deployment) and `runner-playbook.yaml` for the self-hosted runner |
| `k8s/` | Kubernetes manifests used by CD: `deployment.yaml` (rolling update), `service.yaml` (NodePort 30007) |
| `.github/workflows/` | `CI.yml` (test, build, push to DockerHub) and `CD.yml` (deploy to minikube) |

Run the tests locally from the repo root:

```bash
python -m unittest -v tests/smoke_test.py tests/unit_test.py tests/integration_test.py
```
