from fastapi.testclient import TestClient
from app.main import app

tst_client = TestClient(app)
def test_liveness():
    r = tst_client.get('/health')
    assert r.status_code == 200
    assert r.json() == {'status':'ok'}

def test_readiness():
    r = tst_client.get('/health/ready')
    assert r.status_code == 200

def test_db_brokedown():
    from app.core.database import get_db
    from sqlalchemy.exc import OperationalError

    class BrokeDown:
        def execute(self, *a, **k):
            raise OperationalError("select 1", {}, Exception("down"))
        def close(self): pass

    app.dependency_overrides[get_db] = lambda : BrokeDown()
    try:
        r = tst_client.get('/health/ready')
        assert r.status_code == 503
    finally:
        app.dependency_overrides.clear()