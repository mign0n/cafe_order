from core.constants import MAX_TABLES_NUMBER
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from order.models import Meal, Order


class MealFactory(DjangoModelFactory):
    name = Faker('sentence')
    price = Faker('pydecimal', left_digits=4, right_digits=2, positive=True)

    class Meta:
        model = Meal


class OrderFactory(DjangoModelFactory):
    table_number = Faker('random_int', min=1, max=MAX_TABLES_NUMBER)
    created_at = None

    class Meta:
        model = Order

    @post_generation
    def items(self, create: bool, extracted: list, **kwargs) -> None:
        if not create:
            return
        if extracted:
            self.items.set(*extracted)
        else:
            self.items.add(MealFactory())
