import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.models import Base
from app.core.deps import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    mock_redis = Mock()
    mock_redis.get.return_value = None
    mock_redis.setex.return_value = None
    mock_redis.delete.return_value = None

    app.dependency_overrides[get_db] = override_get_db

    with patch('app.core.cache.redis_client', mock_redis):
        with patch('app.services.analytics.get_cache') as mock_get_cache:
            with patch('app.services.analytics.set_cache') as mock_set_cache:
                mock_get_cache.return_value = None
                mock_set_cache.return_value = None

                yield TestClient(app)

    app.dependency_overrides.clear()