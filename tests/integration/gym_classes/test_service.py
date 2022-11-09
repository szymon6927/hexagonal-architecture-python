import pytest
from bson import ObjectId
from pymongo.database import Database

from src.gym_classes.errors import GymClassNotFound
from src.gym_classes.models import CreateOrUpdateClass, GymClass
from src.gym_classes.service import GymClassService


@pytest.mark.usefixtures("seed_db")
def test_can_get_all_sorted_by_day(mongodb: Database) -> None:
    # given
    service = GymClassService(mongodb)

    # when
    result = service.get_all()

    # then
    assert len(result) == 5
    assert result[0].name == "Cross fit kids"
    assert result[4].name == "MMA"


@pytest.mark.usefixtures("seed_db")
def test_can_get_one(mongodb: Database) -> None:
    # given
    service = GymClassService(mongodb)

    # when
    gym_class = service.get(ObjectId("63500520c1f28686b7d7da2c"))

    # then
    assert isinstance(gym_class, GymClass)
    assert gym_class.name == "Pilates 1"
    assert gym_class.day == "Monday"
    assert gym_class.description == "test 1"


@pytest.mark.usefixtures("seed_db")
def test_should_raise_an_error_if_gym_class_does_not_exist(mongodb: Database) -> None:
    # given
    service = GymClassService(mongodb)

    # expect
    with pytest.raises(GymClassNotFound):
        service.get(ObjectId())


def test_can_create_new_gym_class(mongodb: Database) -> None:
    # given
    service = GymClassService(mongodb)
    collection = mongodb.get_collection("gym_classes")

    # when
    result = service.create(CreateOrUpdateClass(name="Test", day="Monday", time="10:30", coach="John Doe"))

    # then
    documents = list(collection.find({}))
    assert isinstance(result, GymClass)
    assert len(documents) == 1
    assert documents[0]["name"] == "Test"


@pytest.mark.usefixtures("seed_db")
def test_can_update_gym_class(mongodb: Database) -> None:
    # given
    service = GymClassService(mongodb)
    collection = mongodb.get_collection("gym_classes")

    # when
    result = service.update(
        "63500520c1f28686b7d7da2c", CreateOrUpdateClass(name="Test", day="Monday", time="10:30", coach="John Doe")
    )

    # then
    document = collection.find_one({"_id": ObjectId("63500520c1f28686b7d7da2c")})
    assert isinstance(result, GymClass)
    assert result.name == "Test"
    assert document["name"] == "Test"  # type: ignore


@pytest.mark.usefixtures("seed_db")
def test_can_delete(mongodb: Database) -> None:
    # given
    service = GymClassService(mongodb)
    collection = mongodb.get_collection("gym_classes")

    # when
    service.delete("63500520c1f28686b7d7da2c")

    # then
    documents = list(collection.find({}))
    assert len(documents) == 4
    assert "63500520c1f28686b7d7da2c" not in [str(document["_id"]) for document in documents]
